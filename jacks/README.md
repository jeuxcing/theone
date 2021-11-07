# 1-Wire addresses (uint8_t)

* Main bus listener: 'M'
* Rotary encoders: 'R'
* Potentiometers: 'P'
* Vertical Linear Potentiometers 'V'
* Horizontal Linear Potentiometers 'H'
* Buttons: 'B'
* Control (Start/pause/...): 'C'


# 1-Wire Mixer commands

## Declare link to the wall \[4 Bytes\]

* Serder type (see 1-Wire address for types) \[1 Byte\]
* Link command 'L' \[1 Byte\]
* Mixer coordinate \[1 Byte\]
* Wall coordinate \[1 Byte\]


## Break link to the wall \[4 Bytes\]

* Serder type (see 1-Wire address for types) \[1 Byte\]
* Unlink command 'U' \[1 Byte\]
* Mixer coordinate \[1 Byte\]
* Wall coordinate \[1 Byte\]


## Send controler value \[4 Bytes\]

* Serder type (see 1-Wire address for types) \[1 Byte\]
* Value command 'V' \[1 Byte\]
if rotary type, 32 for "-1", 64 for "+1"
* Mixer coordinate \[1 Byte\]
* Value \[1 Byte\]
