/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "crc16_bb_impl.h"
#include "crc16.h"

namespace gr {
  namespace dab {

    crc16_bb::sptr
    crc16_bb::make(int length = 32, uint16_t generator = 0x1021, uint16_t initial_state = 0xFF)
    {
      return gnuradio::get_initial_sptr
        (new crc16_bb_impl(length, generator, initial_state));
    }

    crc16_bb_impl::crc16_bb_impl(int length, uint16_t generator, uint16_t initial_state)
      : gr::block("crc16_bb",
              gr::io_signature::make(1, 1, length*sizeof(char)), //FIB without CRC (zeros instead)
              gr::io_signature::make(1, 1, length*sizeof(char))) //FIB with CRC (+2 byte)
    {
        len = length;
        gen = generator;
        init_state = initial_state;
    }

    crc16_bb_impl::~crc16_bb_impl()
    {
    }

    void
    crc16_bb_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    int
    crc16_bb_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const char *in = (const char *) input_items[0];
      char *out = (char *) output_items[0];

      //push bytes through
      for(int i = 0; i < len; i++) {
          out[i] = in[i];
      }
      //calculate crc16 word
      crc = crc16(in, len, gen, init_state);

      //write calculated crc to vector (overwrite last 2 bytes)
      out[len-2] = (char) (crc>>8);//add MSByte first to FIB
      out[len-1] = (char)(out[len-2]<<8)^crc; //add LSByte second to FIB
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (1);

      // Tell runtime system how many output items we produced.
      return 1;
    }

  } /* namespace dab */
} /* namespace gr */

