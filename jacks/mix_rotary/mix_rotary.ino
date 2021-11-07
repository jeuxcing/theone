#include <PJONSoftwareBitBang.h>

#define TYPE 'R' /* Rotary /**/
//#define TYPE 'P' /* Potard /**/
//#define TYPE 'L' /* Linear /**/
//#define TYPE 'B' /* Button /**/

#define NB_JACKS 5
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

int laststate[5];
int state[5];

int current_pin = 100;

PJONSoftwareBitBang jack_bus;
PJONSoftwareBitBang main_bus;

void jack_receiver(uint8_t *payload, uint16_t length, const PJON_Packet_Info &info) {
  if (pairs[current_pin] != *payload) {
    Serial.print(current_pin);
    Serial.print(" <---> ");
    Serial.println(*payload);

    // Send the connection
    unsigned int packet[4];
    // Wich part of the controller
    packet[0] = TYPE;
    // Link command
    packet[1] = 'L';
    // Link coordinates
    packet[2] = current_pin;
    packet[3] = *payload;
    //main_bus.send_packet_blocking('M', packet, 4);
  }
  // Register pair
  pairs[current_pin] = *payload;
  last_contact[current_pin] = millis();
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

  laststate[0] = digitalRead(A0);
  laststate[1] = digitalRead(A1);
  laststate[2] = digitalRead(A2);
  laststate[3] = digitalRead(A3);
  laststate[4] = digitalRead(A4);
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
        uint8_t value;
        switch (TYPE) {
          case 'V':
          case 'H':
          case 'P':
            value = analogRead(measure_pins[i]) / 4;
            break;
          case 'B':
            value = digitalRead(measure_pins[i]) == LOW ? 255 : 0;
            break;
          case 'R':
            value = 0;
            state[i] = digitalRead(measure_pins[i]);
            if (state[i] != laststate[i]){
              if (digitalRead(measure_pinsB[i])!=state[i]){
                value = 64;
              }
              else {
                value = 32;
              }
            }
            laststate[i]=state[i];
            
            break;
        }

        if (((TYPE == 'R') and (value != 0)) or ((TYPE != 'R') and ( abs(((int16_t)value) - ((int16_t)values[i])) > 3))) {
          values[i] = value;

          unsigned int packet[4];
          // Wich part of the controller
          packet[0] = TYPE;
          // Unlink command
          packet[1] = 'V';
          // Link coordinates
          packet[2] = i;
          packet[3] = pairs[i];
          //main_bus.send_packet_blocking('M', packet, 4);

          Serial.print(TYPE);
          Serial.print(" [");
          Serial.print(i);
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
      packet[2] = i;
      packet[3] = pairs[i];
      //main_bus.send_packet_blocking('M', packet, 4);

      Serial.print(i);
      Serial.print("   X   ");
      Serial.println(pairs[i]);

      // Locally register the disconnection
      pairs[i] = 255;
    }
  }
}
