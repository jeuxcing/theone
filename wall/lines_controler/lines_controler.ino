#include <PJONSoftwareBitBang.h>
#include <Adafruit_NeoPixel.h>

// #define NET_ID 'R'
// #define NET_ID 'V'
#define NET_ID 'H'

#define REFRESH_DELAY 5
#define NB_LINES 5

#if NET_ID == 'R'
  #define NB_SEGMENTS 5
  #define NB_LED_SEGMENT (12)
#else
  #define NB_SEGMENTS 4
  #define NB_LED_SEGMENT (24)
#endif

#define NB_LEDS_LINE (NB_SEGMENTS * NB_LED_SEGMENT)


int pins[5] = {2, 3, 5, 6, 7};
Adafruit_NeoPixel lines[NB_LINES];

#define NET 12
PJONSoftwareBitBang bus;


bool modified[NB_LINES];


void modify_led(uint8_t * payload, uint8_t length) {
  uint8_t line_idx = payload[1];
  uint8_t led_idx = payload[2];
  uint8_t red = payload[3];
  uint8_t green = payload[4];
  uint8_t blue = payload[5];

  lines[line_idx].setPixelColor(led_idx, red, green, blue);
  modified[line_idx] = true;
}


void modify_segment(uint8_t * payload, uint8_t length) {
  uint8_t line_idx = payload[1];
  uint8_t start_led_idx = payload[2];
  uint8_t stop_led_idx = payload[3];
  uint8_t red = payload[4];
  uint8_t green = payload[5];
  uint8_t blue = payload[6];

  for (uint8_t i=start_led_idx ; i<= stop_led_idx ; i++) {
    lines[line_idx].setPixelColor(i, red, green, blue);
  }
  modified[line_idx] = true;
}


void receiver_function(uint8_t * payload, uint16_t length, const PJON_Packet_Info &info) {
  //Serial.println("Packet received");
  for (int i=0 ; i<length ; i++) {
    Serial.print('[');
    Serial.print(payload[i]);
    Serial.print(']');
  }
  Serial.println();
  
  uint8_t command = payload[0];
  switch(command) {
    case 'L':
      modify_led(payload, length);
      break;
    case 'S':
      modify_segment(payload, length);
      break;
  }
};


void setup() {
  // Init led strips
  for (int lines_idx=0 ; lines_idx<NB_LINES ; lines_idx++) {
    //lines[lines_idx] = Adafruit_NeoPixel(NB_LEDS_LINE, pins[lines_idx]);
    lines[lines_idx].updateLength(NB_LEDS_LINE);
    lines[lines_idx].setPin(pins[lines_idx]);
    lines[lines_idx].begin();
    lines[lines_idx].clear();
    lines[lines_idx].show();
  }

  // Init network
  // Set the pin 12 as the communication pin
  bus.strategy.set_pin(NET);
  bus.set_id(NET_ID);
  
  // Define network callback
  bus.set_receiver(receiver_function);

  Serial.begin(115200);
}

unsigned long previous_show = 0;

void loop() {
  for (int i=0 ; i<10 ; i++)
    bus.receive();

  unsigned long current_time = millis();
  if (current_time - previous_show > REFRESH_DELAY) {
    for (int line_idx=0 ; line_idx<NB_LINES ; line_idx++) {
      if (modified[line_idx]) {
        lines[line_idx].show();
        modified[line_idx] = false;
      }
    }
    previous_show = millis();
  }
}
