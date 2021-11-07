#include <PJONSoftwareBitBang.h>


#define NET_PIN 12
#define NET_ID 'M' /* As Main address on this 1-wire network */


PJONSoftwareBitBang bus;


void cmd_handler(uint8_t * payload, uint16_t length, const PJON_Packet_Info &info);
void read_serial();

void setup() {
  // Serial Init
  Serial.begin(115200);

  // Led init
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  // Bus init
  bus.strategy.set_pin(NET_PIN);
  bus.set_id(NET_ID);
  // TODO: from 1-wire to serial
  bus.set_receiver(cmd_handler);
} 

void loop() {
    if (Serial.available())
      read_serial();
    delay(1);
}


void debug_print(uint8_t length, uint8_t * msg) {
  Serial.write(length);
  for (int i=0 ; i<length ; i++)
    Serial.write(msg[i]);
  Serial.flush();
}


uint8_t buffer[254];
uint8_t msg[16];

void read_serial() {
  int val = Serial.read();
  // If no data return
  if (val == -1)
    return;

  // Synchronisation data arrays (in case of packet loss)
  //if (val == 255) {
  //  while (val == 255)
  //    val = Serial.read();
  //  // TODO: Notify synch on serial
  //  digitalWrite(LED_BUILTIN,HIGH);
  //  return;
  //}

  // Read the packet
  buffer[0] = (uint8_t)val;
  uint8_t idx=1;
  while (val > 0) {
    // TODO: Add a timeout
    if (Serial.available()) {
      buffer[idx++] = (uint8_t)Serial.read();
      val -= 1;
    } else {
      delay(1);
    }
  }

  // Modify the packet for line coordinates
  if (buffer[1] == 'L') {
    msg[0] = 6;
    msg[1] = 'L';
    msg[2] = buffer[3]; // Line coordinate
    msg[3] = buffer[4] * (buffer[2] == 'R' ? 12 : 24) + buffer[5]; // Led coordinate
    msg[4] = buffer[6];
    msg[5] = buffer[7];
    msg[6] = buffer[8];
  }
  // Modify packet for segment command
  else if (buffer[1] == 'S') {
    msg[0] = 7;
    msg[1] = 'S';
    msg[2] = buffer[3]; // Line coordinate
    msg[3] = buffer[4] * (buffer[2] == 'R' ? 12 : 24) + buffer[5]; // Led start coordinate
    msg[4] = buffer[4] * (buffer[2] == 'R' ? 12 : 24) + buffer[6]; // Led stop coordinate
    msg[5] = buffer[7];
    msg[6] = buffer[8];
    msg[7] = buffer[9];
  }

  // Send the packet on the 1-Wire
  uint16_t status = bus.send_packet_blocking(buffer[2], msg+1, msg[0]);
  //if (status == PJON_ACK) {
    Serial.write(1);
    Serial.write(0xFF);
    Serial.flush();
  //}
}

void cmd_handler(uint8_t * payload, uint16_t length, const PJON_Packet_Info &info) {
  // TODO  
}
