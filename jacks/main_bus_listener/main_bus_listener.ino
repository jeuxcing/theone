#include <PJONSoftwareBitBang.h>

#define NET_PIN 2


PJONSoftwareBitBang main_bus;


void wire_receiver(uint8_t *payload, uint16_t length, const PJON_Packet_Info &info) {
  Serial.write((uint8_t)length);
  Serial.write(payload, length);
  Serial.flush();
}

uint8_t buffer[255];

void serial_receiver() {
  uint8_t nb_bytes = Serial.read();

  uint8_t i = 0;
  
  while (i< nb_bytes) {
    if (Serial.available() > 0) {
      buffer[i++] = Serial.read();
    }
  }

  main_bus.send_packet_blocking(buffer[0], buffer, nb_bytes);
}

void setup() {
  Serial.begin(115200);

  main_bus.strategy.set_pin(NET_PIN);
  main_bus.set_id('M');
  main_bus.set_receiver(wire_receiver);
  main_bus.begin();
}

void loop() {
  if (Serial.available() > 0)
    serial_receiver();
  main_bus.receive();
}
