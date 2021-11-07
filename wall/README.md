# Content Summary

## lines_controler

Connect to n led strips lines (vertical horizontal of rings does not matter).
Receive commands from the 1-wire PJON network and show them on the strip.
See Lines protocol for network commands.

## network_writer

ESP demo code that writes commands on the PJON network.
Will be transformed into a Raspberry Pi C++ code soon.

# Grid protocol

## Allumer wall 1 Led \[8 Byte\]

* Command: 'L' \[1 Byte\]
* Strip: 'V' (vertical) or 'H' (horizontal) or 'R' (ring) \[1 Byte\]
* Segment coordinates: line (0 -> 4) \[1 Byte\], segment (0 -> 3) \[1 Byte\]
* Led: (0 -> 23 or 11) \[1 Byte\]
* Color RGB \[3 Byte\] 


## Allumer wall segment \[9 Byte\]

* Command: 'S' \[1 Byte\]
* Strip: 'V' (vertical) or 'H' (horizontal) or 'R' (ring) \[1 Byte\]
* Start segment coordinates : line (0 -> 4) \[1 Byte\], segment (0 -> 3) \[1 Byte\]
* Start/stop leds: (0 -> 23 or 11) * 2 \[2 Byte\]
* Color RGB \[3 Byte\] 


# Lines protocol

## 1-Wire led control

Set 1 led to a RGB value.

6 Bytes:
* Command: 'L' char (1 Byte)
* Line coordinate (1 Byte)
* Led coordinate (1 Byte)
* Colors \[R, G, B\] (3 Bytes)
