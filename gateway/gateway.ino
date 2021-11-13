#define SWBB_MODE 4
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
  while (1)
    if (Serial.available())
      read_serial();
}


void debug_print(uint8_t length, uint8_t * msg) {
  Serial.write(length);
  for (int i=0 ; i<length ; i++)
    Serial.write(msg[i]);
  Serial.flush();
}


uint8_t buffer[254];
void modify_light(uint8_t * src, uint8_t * dest);
void modify_segment(uint8_t * src, uint8_t * dest);

void read_serial() {
  int val = Serial.read();
  // If no data return
  if (val == -1)
    return;

  // Read the packet
  buffer[0] = (uint8_t)val;
  uint8_t global_size = val;
  uint8_t idx=1;
  while (val > 1) {
    // TODO: Add a timeout
    if (Serial.available()) {
      buffer[idx++] = (uint8_t)Serial.read();
      val -= 1;
    } else {
      delay(1);
    }
  }

  // Register global variables
  uint8_t dest = buffer[2];
  uint8_t * src = buffer;
  uint8_t * msg = buffer;
  uint8_t msg_size = 0;

  //debug_print(global_size, buffer);
  do {
    //debug_print(1, &global_size);
    // Modify the packet for line coordinates
    if (src[1] == 'L') {
      modify_light(src, msg);
      src += 9; global_size -= 9;
      msg += 7; msg_size += 7;
    }
    // Modify packet for segment command
    else if (src[1] == 'S') {
      modify_segment(src, msg);
      src += 10; global_size -= 10;
      msg += 8; msg_size += 8;
    } else if (src[1] == 'M') {
      msg[1] = 'M';
      msg[2] = src[3];
      src += 4; global_size -= 4;
      msg += 3; msg_size += 3;
    }
  } while (global_size > 0);
  buffer[0] = msg_size;

  // Send the packet on the 1-Wire
  uint16_t status = 0xFFFF;
  status = bus.send_packet_blocking(dest, buffer+1, msg_size-1);
  Serial.write(1);
  Serial.write(0xFF);
  Serial.flush();
}

// Translate the segment command
void modify_segment(uint8_t * src, uint8_t * dest) {
  uint8_t nb_leds = src[2] == 'R' ? 12 : 24;
  
  dest[0] = 7;
  dest[1] = 'S';
  dest[2] = src[3]; // Line coordinate
  dest[3] = src[4] * nb_leds + src[5]; // Led start coordinate
  dest[4] = src[4] * nb_leds + src[6]; // Led stop coordinate
  dest[5] = src[7];
  dest[6] = src[8];
  dest[7] = src[9];
}

// Translate the light command
void modify_light(uint8_t * src, uint8_t * dest) {
  uint8_t nb_leds = src[2] == 'R' ? 12 : 24;

  dest[0] = 6;
  dest[1] = 'L';
  dest[2] = src[3]; // Line coordinate
  dest[3] = src[4] * nb_leds + src[5]; // Led coordinate
  dest[4] = src[6];
  dest[5] = src[7];
  dest[6] = src[8];
  //debug_print(5, &dest[2]);
}


void cmd_handler(uint8_t * payload, uint16_t length, const PJON_Packet_Info &info) {
  // TODO  
}
