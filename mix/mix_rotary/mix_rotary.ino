#include <PJONSoftwareBitBang.h>

#define TYPE 'R' /* Rotary /**/
//#define TYPE 'P' /* Potard /**/
//#define TYPE 'L' /* Linear /**/
//#define TYPE 'B' /* Button /**/
//#define TYPE 'H' /* Horizontal Slider /**/
//#define TYPE 'V' /* Vertical Slider /**/

#if TYPE =='V' or TYPE =='H'
  #define NB_JACKS 4 //shall be 6 later
#else
  #define NB_JACKS 5
#endif

#define NET_PIN 2
#define DISCONNECT_DELAY 500

unsigned int plug_pins[] = {3, 5, 7, 9, 11};
bool plugged[] = {false, false, false, false, false};
unsigned int network_pins[] = {4, 6, 8, 10, 12};
uint8_t pairs[] = {255, 255, 255, 255, 255};
unsigned long last_contact[] = {0, 0, 0, 0, 0};
unsigned int measure_pins[] = {A0, A1, A2, A3, A4};
unsigned int measure_pinsB[] = {A3, A4, A5}; //For the rotary, baby

uint16_t values[] = {0, 0, 0, 0, 0};

int rotatyState[5] = {0, 0, 0, 0, 0};
int firstTime;
int averageRotary;

int current_pin = 100;

PJONSoftwareBitBang jack_bus;
PJONSoftwareBitBang main_bus;

uint8_t jack_coordinate(int pin){
  if ((TYPE == 'V') or (TYPE=='H')){
      uint8_t pos,num;
      pos = pin%2<<4;
      num = int(pin/2); 
      return pos | num;
    }
    else{
      return pin;
    }
}

void print_coordinate(int pin){
  if ((TYPE == 'V') or (TYPE == 'H')){
      Serial.print(TYPE);
      Serial.print(pin%2);
      Serial.print('N');
      Serial.print(int(pin/2));
    }
    else{
      Serial.print(pin);
    }
}

void jack_receiver(uint8_t *payload, uint16_t length, const PJON_Packet_Info &info) {
  if (pairs[current_pin] != *payload) {
    print_coordinate(current_pin);
    Serial.print(" <---> ");
    Serial.println(*payload);

    // Send the connection
    uint8_t packet[4];
    // Wich part of the controller
    packet[0] = TYPE;
    // Link command
    packet[1] = 'L';
    // Link coordinates
    packet[2] = jack_coordinate(current_pin);
    Serial.println(byte(packet[2]));
    packet[3] = *payload;
    //main_bus.send_packet_blocking('M', packet, 4);
  }
  // Register pair
  pairs[current_pin] = *payload;
  last_contact[current_pin] = millis();
}

int detectRotation(int pin1, int pin2,int *lastEncoded){
  int MSB = digitalRead(pin1);
  int LSB = digitalRead(pin2); 
  int result = 0;
  int encoded = (MSB << 1) |LSB; 

  int sum = (*lastEncoded << 2) | encoded;
  (*lastEncoded) = encoded; 

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
    result++;
  }
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000){
    result--;
  }

  if(result > 0){
    return 64; //Turn Right
  }else if(result < 0){
    return 128; //Turn Left
  }
  else{
    return 255;//No rotation
  }
}
  
void setup() {
  Serial.begin(115200);

  // Set jack plug readers
  for (int i=0 ; i<NB_JACKS ; i++) {
    pinMode(plug_pins[i], INPUT_PULLUP);  
  }
  
  for (int i=0 ; i<3 ; i++){
    pinMode(measure_pins[i],INPUT_PULLUP);
    if (TYPE == 'R')
      pinMode(measure_pinsB[i],INPUT_PULLUP);
  }

  // Set Jack BitBang bus
  jack_bus.strategy.set_pin(network_pins[0]);
  jack_bus.set_id(100);
  jack_bus.begin();
  jack_bus.set_receiver(jack_receiver);


  // Set 
  main_bus.strategy.set_pin(NET_PIN);
  main_bus.set_id(TYPE);
  main_bus.begin();

  firstTime = millis();

}


void loop() {
  for (int i=0 ; i<NB_JACKS ; i++) {
    bool to_disconnect = false;
    
    bool prev = plugged[i];
    plugged[i] = (digitalRead(plug_pins[i]) == LOW);
    if (prev and not plugged[i] and pairs[i] != 255) {
      to_disconnect = true;
    }

    // Pair jack check
    if (plugged[i] == true) {
      jack_bus.strategy.set_pin(network_pins[i]);
      current_pin = i;
      uint16_t result = jack_bus.receive(50);

      // Check distant jack status and trigger disconnection
      if (pairs[i] != 255 and millis() - last_contact[i] > DISCONNECT_DELAY) {
        to_disconnect = true;
      }
      // Read the value if connected
      else if (pairs[i] != 255) {
        uint8_t value = 255;
        switch (TYPE) {
          case 'V':
            if((i%2==1) and (plugged[i-1] == true) and (pairs[i]%5 == pairs[i-1]%5)){
              value = analogRead(measure_pins[int((i-1)/2)]) / 4;
            }
            break;
          case 'H':
            if((i%2==1) and (plugged[i-1] == true) and (pairs[i]/5 == pairs[i-1]/5)){
              value = analogRead(measure_pins[int((i-1)/2)]) / 4;
            }
            break;
          case 'P':
            value = analogRead(measure_pins[i]) / 4;
            break;
          case 'B':
            value = digitalRead(measure_pins[i]) == LOW ? 254 : 0;
            break;
          case 'R':
            int currentTime = millis();
            int currentValue = detectRotation(measure_pins[i], measure_pinsB[i],&rotatyState[i]); 
            if(currentValue == 255 && currentTime > firstTime + 100){
              if(averageRotary >=96 ){
                value= 128;
              }else{
                value = 64;
              }
            }

            if(currentValue != 255){
              if(currentTime > firstTime + 100){
                firstTime = currentTime;
                averageRotary = currentValue;
              }else{
                averageRotary = (averageRotary + currentValue) / 2;
              }
            }
          
           
            
            break;
        }

        if ((value!=255) and (abs(((int16_t)value) - ((int16_t)values[i])) > 3)) {
          values[i] = value;

          unsigned int packet[4];
          // Wich part of the controller
          packet[0] = TYPE;
          // Unlink command
          packet[1] = 'V';
          // Link coordinates
          packet[2] = jack_coordinate(i);
          packet[3] = pairs[i];
          //main_bus.send_packet_blocking('M', packet, 4);

          Serial.print(TYPE);
          Serial.print(" [");
          print_coordinate(i);
          Serial.print("]: ");
          Serial.println(value);
        }
      }
    }

    // Send disconnection info
    if (to_disconnect) {
      unsigned int packet[4];
      // Wich part of the controller
      packet[0] = TYPE;
      // Unlink command
      packet[1] = 'U';
      // Link coordinates
      packet[2] = jack_coordinate(i);
      packet[3] = pairs[i];
      //main_bus.send_packet_blocking('M', packet, 4);

      print_coordinate(i);
      Serial.print("   X   ");
      Serial.println(pairs[i]);

      // Locally register the disconnection
      pairs[i] = 255;
    }
  }
}
