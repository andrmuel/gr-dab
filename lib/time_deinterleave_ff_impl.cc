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
#include "time_deinterleave_ff_impl.h"

namespace gr {
  namespace dab {

    time_deinterleave_ff::sptr
    time_deinterleave_ff::make(int vector_length, const std::vector<unsigned char> &scrambling_vector)
    {
      return gnuradio::get_initial_sptr
              (new time_deinterleave_ff_impl(vector_length, scrambling_vector));
    }

    /*
     * The private constructor
     */
    time_deinterleave_ff_impl::time_deinterleave_ff_impl(int vector_length,
                                                         const std::vector<unsigned char> &scrambling_vector)
            : gr::sync_block("time_deinterleave_ff",
                             gr::io_signature::make(1, 1, sizeof(float)),
                             gr::io_signature::make(1, 1, sizeof(float))),
              d_vector_length(vector_length), d_scrambling_vector(scrambling_vector)
    {
      d_scrambling_length = scrambling_vector.size(); // size of the scrambling vector
      set_output_multiple(d_vector_length);
      set_history((d_scrambling_length-1)*d_vector_length + 1); //need for max delay of (scrambling_length-1) * 24ms
    }

    /*
     * Our virtual destructor.
     */
    time_deinterleave_ff_impl::~time_deinterleave_ff_impl()
    {
    }

    int
    time_deinterleave_ff_impl::work(int noutput_items,
                                    gr_vector_const_void_star &input_items,
                                    gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      for (int i = 0; i < noutput_items/d_vector_length; i++) {
        // produce output vectors
        for (int j = 0; j < d_vector_length; j++) {
          *out++ = in[d_vector_length * (i + (d_scrambling_length - 1) - ((d_scrambling_length - 1) - d_scrambling_vector[j % d_scrambling_length])) + j];
          //*out++ = in[i*d_vector_length + d_scrambling_vector[j%d_scrambling_length]*d_vector_length + j - (j%d_scrambling_length) + d_scrambling_vector[j%d_scrambling_length]];
        }
      }
      // Tell runtime system how many output items we produced.
      return noutput_items;
    }
  } /* namespace dab */
} /* namespace gr */
