#include <iostream>
#include <assert.h>
#include <inttypes.h>
#include <stdio.h>
#include "crc16.h"

char packet[] = {0x05,0x00,0x10,0x08,0x0E,0x3C,0x17,0x01,0x2C,0x00,0x88,0x30,0x3C,0x30,0x23,0x40,0x90,0x23,0x44,0xF0,0x2D,0x49,0x7C,0x1A,0x4D,0xC2,0x10,0x51,0xF2,0x23,0x7B,0xFA};

int main(void) {
  uint16_t actual;
  printf("actual CRC: %x\n",(uint8_t)packet[30]*256+(uint8_t)packet[31]);
  actual = (uint8_t)packet[30]*256+(uint8_t)packet[31];
  printf("CRC of whole packet (should be zero): %x\n",crc16(packet,32,0x1021,0xffff));
  assert(crc16(packet,32,0x1021,0xffff)==0);
  packet[10]=0;
  printf("CRC of whole packet withe error (should not be zero): %x\n",crc16(packet,32,0x1021,0xffff));
  assert(crc16(packet,32,0x1021,0xffff)!=0);
  packet[10] = 0x88;
  packet[30]=0;
  packet[31]=0;
  printf("calculated CRC: %x\n",crc16(packet,32,0x1021,0xffff));
  assert(actual==crc16(packet,32,0x1021,0xffff));
  printf("ALL TESTS OK\n");
}
