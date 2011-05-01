#include <inttypes.h>
#include <stdio.h>
#include <iostream>

uint16_t crc16(const char *bytestream, int length, uint16_t generator, uint16_t initial_state) {
  uint16_t state;
  char byte;
  
  state = bytestream[0]*256+bytestream[1];
  state = ~state;
  for (int i=2; i<length; i++) {
    byte = bytestream[i];
    for (int j=7; j>=0; j--) {
      if (((state>>15)&1) == 1)
        state = (((state<<1) + ((byte>>j)&1)) ^ generator);
      else
        state = (state<<1) + ((byte>>j)&1);
    }
  }
  return ~state;
}
