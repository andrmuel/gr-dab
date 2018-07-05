/* -*- c++ -*- */
/* 
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

#include <gnuradio/io_signature.h>
#include "puncture_bb_impl.h"

namespace gr {
  namespace dab {

    puncture_bb::sptr
    puncture_bb::make(const std::vector<unsigned char> &puncturing_vector)
    {
      return gnuradio::get_initial_sptr
              (new puncture_bb_impl(puncturing_vector));
    }

    unsigned int puncture_bb_impl::ones(const std::vector<unsigned char> &puncturing_vector)
    {
      unsigned int onescount = 0;
      for (unsigned int i = 0; i < puncturing_vector.size(); i++) {
        if (puncturing_vector[i] == 1)
          onescount++;
      }
      return onescount;
    }

    /*
     * The private constructor
     */
    puncture_bb_impl::puncture_bb_impl(const std::vector<unsigned char> &puncturing_vector)
            : gr::block("puncture_bb",
                        gr::io_signature::make(1, 1, sizeof(unsigned char)),
                        gr::io_signature::make(1, 1, sizeof(unsigned char))),
              d_puncturing_vector(puncturing_vector)
    {
      d_vlen_in = puncturing_vector.size();
      d_vlen_out = ones(puncturing_vector);
      set_output_multiple(d_vlen_out);
      set_relative_rate(d_vlen_out / d_vlen_in);
    }

    /*
     * Our virtual destructor.
     */
    puncture_bb_impl::~puncture_bb_impl()
    {
    }

    void
    puncture_bb_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items * d_vlen_in / d_vlen_out;
    }

    int
    puncture_bb_impl::general_work(int noutput_items,
                                   gr_vector_int &ninput_items,
                                   gr_vector_const_void_star &input_items,
                                   gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      for (int i = 0; i < noutput_items * d_vlen_in / d_vlen_out; i++) {
        if (d_puncturing_vector[i % d_vlen_in] == 1)
          *out++ = *in++;
        else
          in++;
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(noutput_items * d_vlen_in / d_vlen_out);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab */
} /* namespace gr */

