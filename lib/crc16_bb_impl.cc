/* -*- c++ -*- */
/*
 * Copyright 2017 by Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
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
                        gr::io_signature::make(1, 1, length * sizeof(char)), /*FIB without CRC (zeros instead)*/
                        gr::io_signature::make(1, 1, length * sizeof(char))), /*FIB with CRC16*/
              d_length(length), d_generator(generator), d_initial_state(initial_state)
    {
    }

    crc16_bb_impl::~crc16_bb_impl()
    {
    }

    void
    crc16_bb_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    int
    crc16_bb_impl::general_work(int noutput_items,
                                gr_vector_int &ninput_items,
                                gr_vector_const_void_star &input_items,
                                gr_vector_void_star &output_items)
    {
      const char *in = (const char *) input_items[0];
      char *out = (char *) output_items[0];

      for (int n = 0; n < noutput_items; n++) {
        //push bytes through
        for (int i = 0; i < d_length; i++) {
          out[i + n * d_length] = in[i + n * d_length];
        }
        //calculate crc16 word
        d_crc = crc16(in + n * d_length, d_length, d_generator, d_initial_state);

        //sanity check (last 2 bytes should be zeros)
        if (in[30 + n * d_length] != 0 || in[31 + n * d_length] != 0) {
          GR_LOG_DEBUG(d_logger, "CRC16 overwrites data (zeros expected)");
        }

        //write calculated crc to vector (overwrite last 2 bytes)
        out[d_length - 2 + n * d_length] = (char) (d_crc >> 8);//add MSByte first to FIB
        out[d_length - 1 + n * d_length] =
                (char) (out[d_length - 2 + n * d_length] << 8) ^ d_crc; //add LSByte second to FIB
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab */
} /* namespace gr */
