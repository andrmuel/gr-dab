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
#include "unpuncture_ff_impl.h"

namespace gr {
  namespace dab {

    unpuncture_ff::sptr
    unpuncture_ff::make(const std::vector<unsigned char> &puncturing_vector, float fillval)
    {
      return gnuradio::get_initial_sptr
              (new unpuncture_ff_impl(puncturing_vector, fillval));
    }

    unsigned int unpuncture_ff_impl::ones(const std::vector<unsigned char> &puncturing_vector)
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
    unpuncture_ff_impl::unpuncture_ff_impl(const std::vector<unsigned char> &puncturing_vector, float fillval)
            : gr::block("unpuncture_ff",
                        gr::io_signature::make(1, 1, sizeof(float)),
                        gr::io_signature::make(1, 1, sizeof(float))),
              d_puncturing_vector(puncturing_vector), d_fillval(fillval)
    {
      d_vlen_in = ones(puncturing_vector);
      d_vlen_out = puncturing_vector.size();
      set_output_multiple(d_vlen_out);
      set_relative_rate(d_vlen_out / d_vlen_in);
    }

    /*
     * Our virtual destructor.
     */
    unpuncture_ff_impl::~unpuncture_ff_impl()
    {
    }

    void
    unpuncture_ff_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items * d_vlen_in / d_vlen_out;
    }

    int
    unpuncture_ff_impl::general_work(int noutput_items,
                                     gr_vector_int &ninput_items,
                                     gr_vector_const_void_star &input_items,
                                     gr_vector_void_star &output_items)
    {
      int i;
      unsigned int j;

      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      for (i = 0; i < noutput_items; i++) {
        if (d_puncturing_vector[i % d_vlen_out] == 1)
          *out++ = *in++;
        else
          *out++ = d_fillval;
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(noutput_items * d_vlen_in / d_vlen_out);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab */
} /* namespace gr */

