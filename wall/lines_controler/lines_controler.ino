#include <PJONSoftwareBitBang.h>
#define FASTLED_INTERNAL
#include <FastLED.h>


// --- Change here to define the led strip type ---

// #define NET_ID 'R' /* Rings */
#define NET_ID 'V' /* Columns */
// #define NET_ID 'H' /* Rows */

// ------------------------------------------------


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
//#define NB_LEDS_LINE 1


//int pins[5] = {2, 3, 5, 6, 7};
#define PIN0 2
#define PIN1 3
#define PIN2 5
#define PIN3 6
#define PIN4 7

CRGB lines[NB_LINES][NB_LEDS_LINE];

#define NET 12
PJONSoftwareBitBang bus;


bool modified[NB_LINES];


void modify_led(uint8_t * payload, uint8_t length) {
  uint8_t line_idx = payload[1];
  uint8_t led_idx = payload[2];
  uint8_t red = payload[3];
  uint8_t green = payload[4];
  uint8_t blue = payload[5];

  lines[line_idx][led_idx].setRGB(red, green, blue);
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
    lines[line_idx][i].setRGB(red, green, blue);
  }
  modified[line_idx] = true;
}


void receiver_function(uint8_t * payload, uint16_t length, const PJON_Packet_Info &info) {
  //Serial.println("Packet received");

  int remaining_msgs = 1;

  while (remaining_msgs > 0) {
    uint8_t command = payload[0];
    switch(command) {
      case 'L':
        modify_led(payload, length);
        break;
      case 'S':
        modify_segment(payload, length);
        break;
      case 'M':
        remaining_msgs = payload[1] + 1;
        length = 2;
        break;
    }
    
    remaining_msgs--;
    payload += length;
    length = payload[0];
    payload += 1;
  }
};


void setup() {
  // Init led strips
  FastLED.addLeds<NEOPIXEL, PIN0>(lines[0], NB_LEDS_LINE);
  FastLED.addLeds<NEOPIXEL, PIN1>(lines[1], NB_LEDS_LINE);
  FastLED.addLeds<NEOPIXEL, PIN2>(lines[2], NB_LEDS_LINE);
  FastLED.addLeds<NEOPIXEL, PIN3>(lines[3], NB_LEDS_LINE);
  FastLED.addLeds<NEOPIXEL, PIN4>(lines[4], NB_LEDS_LINE);

  // Init network
  // Set the pin 12 as the communication pin
  bus.strategy.set_pin(NET);
  bus.set_id(NET_ID);
  
  // Define network callback
  bus.set_receiver(receiver_function);

}

unsigned long previous_show = 0;

void loop() {
  for (int i=0 ; i<10 ; i++)
    bus.receive();

  unsigned long current_time = millis();
  if (current_time - previous_show > REFRESH_DELAY) {
    for (int line_idx=0 ; line_idx<NB_LINES ; line_idx++) {
      if (modified[line_idx]) {
        FastLED.show();
        modified[line_idx] = false;
      }
    }
    previous_show = millis();
  }
}
