#include <Arduino.h>
#include "Node.hpp"
#include "Network.hpp"

Network* net;
Node* node;

void setup() {
  Serial.begin(115200);
  delay(3000);
  net = new Network();
  node = new Node();
}

void loop() {
 while (not net->is_connected_to_server())
  {
    // Wifi connection
    if (not net->is_connected_on_wifi())
      net->connect_network();
    // server connection
    if (not net->connect_server(1)) {
      delay(5000);
    };
  }
  
  // Get messages from server
  uint8_t * rcv = net->read_message(10);
  int strip, led, color;
  if (rcv != nullptr)
  {
    printf("Message received\n");
    int num_colors, i, color_idx;
    switch (static_cast<char>(rcv[0]))
    {
    case 'C': // Change color map
      num_colors = net->msg_size / 3;
      //node->change_color_map(num_colors, rcv+1);
    break;

    case 'L': // Light the panel leds (all 9)
      strip = rcv[5];
      led = rcv[6];
      color = rcv[7];
      printf("Light %d %d %d \n", strip, led, color);
      node->color_led(strip,led,color);

      node->show();
    break;

    default:
    break;
    }
  }
  

}

