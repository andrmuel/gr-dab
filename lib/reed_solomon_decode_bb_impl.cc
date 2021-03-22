/* -*- c++ -*- */
/* 
 * Reed-Solomon decoder for DAB+
 * Copyright 2002 Phil Karn, KA9Q
 * May be used under the terms of the GNU General Public License (GPL)
 *
 * Rewritten into a GNU Radio block for gr-dab
 * Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).

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

#include <stdexcept>
#include <stdio.h>
#include <sstream>
#include <boost/format.hpp>
#include <gnuradio/io_signature.h>
#include "reed_solomon_decode_bb_impl.h"

using namespace boost;

namespace gr {
  namespace dab {

    reed_solomon_decode_bb::sptr
    reed_solomon_decode_bb::make(int bit_rate_n)
    {
      return gnuradio::get_initial_sptr
              (new reed_solomon_decode_bb_impl(bit_rate_n));
    }

    /*
     * The private constructor
     */
    reed_solomon_decode_bb_impl::reed_solomon_decode_bb_impl(int bit_rate_n)
            : gr::block("reed_solomon_decode_bb",
                        gr::io_signature::make(1, 1, sizeof(unsigned char)),
                        gr::io_signature::make(1, 1, sizeof(unsigned char))),
              d_bit_rate_n(bit_rate_n)
    {
      rs_handle = init_rs_char(8, 0x11D, 0, 1, 10, 135);
      if (!rs_handle) {
        GR_LOG_DEBUG(d_logger, "RS init failed");
      } else {
        GR_LOG_DEBUG(d_logger, "RS init succeeded");
      }
      d_superframe_size = bit_rate_n * 120;
      d_superframe_size_rs = bit_rate_n * 110;
      set_output_multiple(d_superframe_size_rs);
      d_corrected_errors = 0;
    }

    /*
     * Our virtual destructor.
     */
    reed_solomon_decode_bb_impl::~reed_solomon_decode_bb_impl()
    {
      free_rs_char(rs_handle);
    }

    void reed_solomon_decode_bb_impl::DecodeSuperframe(uint8_t *sf, size_t sf_len)
    {
//	// insert errors for test
//	sf[0] ^= 0xFF;
//	sf[10] ^= 0xFF;
//	sf[20] ^= 0xFF;

      int subch_index = sf_len / 120;
      int total_corr_count = 0;
      bool uncorr_errors = false;

      // process all RS packets
      for (int i = 0; i < subch_index; i++) {
        for (int pos = 0; pos < 120; pos++) {
          rs_packet[pos] = sf[pos * subch_index + i];
        }
        // detect errors
        int corr_count = decode_rs_char(rs_handle, rs_packet, corr_pos, 0);
        if (corr_count == -1) {
          uncorr_errors = true;
          GR_LOG_DEBUG(d_logger, "uncorrectable error");
        } else
          total_corr_count += corr_count;

        // correct errors
        for (int j = 0; j < corr_count; j++) {

          int pos = corr_pos[j] - 135;
          if (pos < 0)
            continue;
          sf[pos * subch_index + i] = rs_packet[pos];
        }
      }
      //GR_LOG_DEBUG(d_logger, format("RS corrected %d errors in superframe") % total_corr_count);
      d_corrected_errors = total_corr_count;
    }


    void
    reed_solomon_decode_bb_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items*120/110;
    }

    int
    reed_solomon_decode_bb_impl::general_work(int noutput_items,
                                              gr_vector_int &ninput_items,
                                              gr_vector_const_void_star &input_items,
                                              gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      for (int n = 0; n < noutput_items / d_superframe_size_rs; n++) {
        uint8_t superframe[d_superframe_size];
        memcpy(superframe, &in[n * d_superframe_size], d_superframe_size);
        DecodeSuperframe(superframe, d_superframe_size);
        memcpy(&out[n * d_superframe_size_rs], superframe, d_superframe_size_rs);
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(noutput_items * 120 / 110);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab */
} /* namespace gr */

