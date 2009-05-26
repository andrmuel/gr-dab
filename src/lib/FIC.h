#ifndef _FIC_H
#define _FIC_H 

#define FIB_LENGTH 32
#define FIB_CRC_LENGTH 2
#define FIB_CRC_POLY 0x1021
#define FIB_CRC_INITSTATE 0xffff
#define FIB_ENDMARKER 0xff

#define FIB_FIG_TYPE_MCI    0
#define FIB_FIG_TYPE_LABEL1 1
#define FIB_FIG_TYPE_LABEL2 2
#define FIB_FIG_TYPE_FIDC   5
#define FIB_FIG_TYPE_CA     6

#define FIB_FIDC_EXTENSION_PAGING 0
#define FIB_FIDC_EXTENSION_TMC    1
#define FIB_FIDC_EXTENSION_EWS    2

#endif /* _FIC_H */
