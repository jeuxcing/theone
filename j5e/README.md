# j5e

Python engine for jeuxcinq


# Grid protocol

## Light 1 Led \[8 Byte\]

* Command: 'L' \[1 Byte\]
* Strip: 'V' (vertical) or 'H' (horizontal) or 'R' (ring) \[1 Byte\]
* Segment coordinates: line (0 -> 4) \[1 Byte\], segment (0 -> 3) \[1 Byte\]
* Led: (0 -> 23 or 11) \[1 Byte\]
* Color RGB \[3 Byte\] 


## Light wall segment \[9 Byte\]

* Command: 'S' \[1 Byte\]
* Strip: 'V' (vertical) or 'H' (horizontal) or 'R' (ring) \[1 Byte\]
* Start segment coordinates : line (0 -> 4) \[1 Byte\], segment (0 -> 3) \[1 Byte\]
* Start/stop leds: (0 -> 23 or 11) * 2 \[2 Byte\]
* Color RGB \[3 Byte\]

## Multi-packet \[3 + ... Bytes\]

* Command: 'M' \[1 Byte\]
* Destination: Id of the arduino to reach on the 1-Wire \[1 Byte\]
* Number of encapsulated packets: 0 to 255 \[1 Byte\]
* Content: Concatenated packets \[Variable size\]
