/* -*- c++ -*- */
/* 
 * Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
 * The class firecode_checker is adapted from the Qt-DAB software, Copyright Jan van Katwijk (Lazy Chair Computing J.vanKatwijk@gmail.com)
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
#include "firecode_check_bb_impl.h"
#include <stdio.h>
#include <stdexcept>
#include <sstream>
#include <boost/format.hpp>

using namespace boost;

namespace gr {
  namespace dab {

    firecode_check_bb::sptr
    firecode_check_bb::make(int bit_rate_n)
    {
      return gnuradio::get_initial_sptr
              (new firecode_check_bb_impl(bit_rate_n));
    }

    /*
     * The private constructor
     */
    firecode_check_bb_impl::firecode_check_bb_impl(int bit_rate_n)
            : gr::block("firecode_check_bb",
                        gr::io_signature::make(1, 1, sizeof(unsigned char)),
                        gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
      d_frame_size = 24 * bit_rate_n;
      set_output_multiple(d_frame_size * 5); //logical frame
    }

    /*
     * Our virtual destructor.
     */
    firecode_check_bb_impl::~firecode_check_bb_impl()
    {
    }

    void
    firecode_check_bb_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    int
    firecode_check_bb_impl::general_work(int noutput_items,
                                         gr_vector_int &ninput_items,
                                         gr_vector_const_void_star &input_items,
                                         gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];
      d_nproduced = 0;
      d_nconsumed = 0;

      while (d_nconsumed < noutput_items / d_frame_size - 4) {
        if (fc.check(&in[d_nconsumed * d_frame_size])) {
          GR_LOG_DEBUG(d_logger, format("fire code (%d %d) OK at frame %d") %(int)in[d_nconsumed*d_frame_size] %(int)in[d_nconsumed*d_frame_size+1] % (nitems_read(0) / d_frame_size));
          // fire code OK, copy superframe to output
          memcpy(out + d_nproduced * d_frame_size, in + d_nconsumed * d_frame_size, d_frame_size * 5);
          d_nproduced += 5;
          d_nconsumed += 5;
          d_firecode_passed = true;
        } else {
          GR_LOG_DEBUG(d_logger, format("fire code failed at frame %d") % (nitems_read(0) / d_frame_size));
          // shift of one logical frame
          d_nconsumed++;
          d_firecode_passed = false;
        }
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(d_nconsumed * d_frame_size);
      // Tell runtime system how many output items we produced.
      return d_nproduced * d_frame_size;
    }

  } /* namespace dab */
} /* namespace gr */

