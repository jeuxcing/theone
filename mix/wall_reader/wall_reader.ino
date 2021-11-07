#include <PJONSoftwareBitBang.h>


#define ROW_ID 0
#define NB_ROWS 5

int plug_pins[] = {3, 5, 7, 9, 11};
bool plugged[] = {false, false, false, false, false};

int network_pins[] = {4, 6, 8, 10, 12};
PJONSoftwareBitBang bus;

void setup() {
  Serial.begin(115200);
  
  bus.set_communication_mode(PJON_SIMPLEX);
  bus.set_id(ROW_ID);
  
  for (int i=0 ; i<NB_ROWS ; i++) {
    pinMode(plug_pins[i], INPUT_PULLUP);
  }
}


#define DELAY 20
unsigned long last_send = 0;

void loop() {
  // Read the plugs
  for (int i=0 ; i<NB_ROWS ; i++) {
    plugged[i] = (digitalRead(plug_pins[i]) == LOW);
  }

  if ((millis() - last_send) > DELAY) {
    for (unsigned int i=0 ; i<NB_ROWS ; i++) {
      if (plugged[i]) {
        uint8_t myid = ROW_ID * NB_ROWS + i;
        bus.strategy.set_pin(network_pins[i]);
        // bus.set_id(ROW_ID * NB_ROWS + i);
        
        uint16_t result = bus.send_packet(100, &myid, 1);
        //if (result != 65535)
          //Serial.println(result);
      }
    }
    
    last_send = millis();    
  }
}
