#ifndef _CRC16_H
#define _CRC16_H 

uint16_t crc16(const char *bitstream, int length, uint16_t generator, uint16_t initial_state);

#endif /* _CRC16_H */
