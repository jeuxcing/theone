# Mixer

## addresses (uint8_t)

* Main bus listener: 'M'
* Rotary encoders: 'R'
* Potentiometers: 'P'
* Vertical Linear Potentiometers 'V'
* Horizontal Linear Potentiometers 'H'
* Buttons: 'B'
* Control (Start/pause/...): 'C'

## Commands

### Link/Unlink (3 Bytes)

* Command Link/Unlink: 'L'/'U' (1 Byte)
* Object id: 0->7 (3 bits packed)
* Object type: ascii code (5 last bits)
* Wall coordinate: 0->25 (1 Byte)


# Wall

## Addresses (uint8_t)

* Main bus listener: 'M'
* Vertical addresser: 'V'
* Horizontal addresser: 'H'
* Rings addressers: 'R'

## Commands

### Declare link to the wall (4 Bytes)

* Serder type (see 1-Wire address for types) (1 Byte)
* Link command 'L' (1 Byte)
* Mixer coordinate (1 Byte)
* Wall coordinate (1 Byte)


### Break link to the wall (4 Bytes)

* Serder type (see 1-Wire address for types) (1 Byte)
* Unlink command 'U' (1 Byte)
* Mixer coordinate (1 Byte)
* Wall coordinate (1 Byte)


### Send controler value (4 Bytes)

* Serder type (see 1-Wire address for types) (1 Byte)
* Value command 'V' (1 Byte)
if rotary type, 32 for "-1", 64 for "+1"
* Mixer coordinate (1 Byte)
* Value (1 Byte)
