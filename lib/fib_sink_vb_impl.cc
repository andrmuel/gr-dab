/* -*- c++ -*- */
/*
 * Copyright 2004,2006,2007 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdio.h>

#include <gnuradio/io_signature.h>
#include "fib_sink_vb_impl.h"
#include <stdexcept>
#include "crc16.h"
#include "FIC.h"

namespace gr {
  namespace dab {

fib_sink_vb::sptr
fib_sink_vb::make()
{
  return gnuradio::get_initial_sptr
    (new fib_sink_vb_impl());
}


fib_sink_vb_impl::fib_sink_vb_impl()
  : gr::sync_block("fib_sink_vb",
		   gr::io_signature::make(1, 1, sizeof(char)*32),
		   gr::io_signature::make(0, 0, 0))
{
}

void
fib_sink_vb_impl::dump_fib(const char *fib) {
  printf("FIB dump: ");
  for (int i=0; i<FIB_LENGTH; i++)
    printf("%.2x ",(uint8_t)fib[i]);
  printf("\n");
}

int 
fib_sink_vb_impl::process_fib(const char *fib) {
  uint8_t type, length, pos;
  if (crc16(fib,FIB_LENGTH,FIB_CRC_POLY,FIB_CRC_INITSTATE)!=0) {
    fprintf(stderr,"FIB CRC error\n");
    return 1;
  }
  pos = 0;
  while (pos<FIB_LENGTH-FIB_CRC_LENGTH && (uint8_t)fib[pos]!=FIB_ENDMARKER && (uint8_t)fib[pos]!=0) { //TODO correct?
    type = fib[pos]>>5;
    length = fib[pos] & 0x1f;
    assert(pos+length<=FIB_LENGTH-FIB_CRC_LENGTH);
    assert(length!=0);
    process_fig(type,&fib[pos],length);
    pos += length+1;
  }
  return 0;
}

int
fib_sink_vb_impl::process_fig(uint8_t type, const char *data, uint8_t length) {
  char label[17];
  uint8_t label_charset;
  uint8_t label_other_ensemble;
  uint8_t label_extension;
  uint8_t fidc_extension;
  // fprintf(stderr,"processing FIG, type %d, length %d\n", type, length);
  switch (type) {
    case FIB_FIG_TYPE_MCI:
      break;
    case FIB_FIG_TYPE_LABEL1:
    case FIB_FIG_TYPE_LABEL2:
      label_charset = (uint8_t)(data[0]>>4);
      label_other_ensemble = (uint8_t)((data[0]>>3) & 1);
      label_extension = (uint8_t)(data[0]&0x7);
      memcpy(label,&data[4],16);
      label[16]=0;
      printf("Label: %s\n",label);
      break;
    case FIB_FIG_TYPE_FIDC:
      fidc_extension = (uint8_t)(data[0]&0x7);
      switch (fidc_extension) {
        case FIB_FIDC_EXTENSION_PAGING:
          printf("got FIB with FIDC extension: paging - not supported yet\n");
          break;
        case FIB_FIDC_EXTENSION_TMC:
          printf("got FIB with FIDC extension TMC (traffic message channel) - not supported yet\n");
          break;
        case FIB_FIDC_EXTENSION_EWS:
          printf("got FIB with FIDC extension EWS (emergency warning service) - not supported yet\n");
          break;
        default:
          printf("unknown FIB FIDC extension\n");
      }
      break;
    case FIB_FIG_TYPE_CA:
      printf("FIB type CA (conditional access) not supported yet\n");
      break;
    default:
      printf("unsupported FIB type\n");
      break;
  }
  return 0;
}

int 
fib_sink_vb_impl::work(int noutput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items)
{
  const char *in = (const char *) input_items[0];
  
  for (int i=0; i<noutput_items; i++) {
    // dump_fib(in);
    process_fib(in);
    in+=32;
  }

  return noutput_items;
}

}
}
