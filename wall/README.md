# Content Summary

## lines_controler

Connect to n led strips lines (vertical horizontal or rings is only one define change at the beginning of the file).
Receive commands from the 1-wire PJON network and show them on the strip.
See Lines protocol for network commands.


# 1-Wire protocol

## Color 1 led

Set 1 led to a RGB value.

6 Bytes:
* Command: 'L' char (1 Byte)
* Line coordinate (1 Byte)
* Led coordinate (1 Byte)
* Colors \[R, G, B\] (3 Bytes)

## Color 1 segment

Set 1 color in between two pixels (included)

7 Bytes:
* Command: 'S' char (1 Byte)
* Line coordinate (1 Byte)
* Start led coordinate (1 Byte)
* Stop led coordinate (1 Byte)
* Colors \[R, G, B\] (3 Bytes)

## Multi-packet (3 + ... Bytes)

* Command: 'M' (1 Byte)
* Destination: Id of the arduino to reach on the 1-Wire (1 Byte)
* Number of encapsulated packets: 0 to 255 (1 Byte)
* Content: Concatenated packets (Variable size)