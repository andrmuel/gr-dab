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
#include "select_subch_vfvf_impl.h"

namespace gr {
  namespace dab {

    select_subch_vfvf::sptr
    select_subch_vfvf::make(unsigned int vlen_in, unsigned int vlen_out, unsigned int address,
                            unsigned int total_size)
    {
      return gnuradio::get_initial_sptr
              (new select_subch_vfvf_impl(vlen_in, vlen_out, address, total_size));
    }

    /*
     * The private constructor
     */
    select_subch_vfvf_impl::select_subch_vfvf_impl(unsigned int vlen_in, unsigned int vlen_out,
                                                   unsigned int address, unsigned int total_size)
            : gr::block("select_subch_vfvf",
                        gr::io_signature::make(1, 1, sizeof(float) * vlen_in),
                        gr::io_signature::make(1, 1, sizeof(float) * vlen_out)),
              d_vlen_in(vlen_in), d_vlen_out(vlen_out), d_address(address), d_total_size(total_size)
    {
      //sanity check
      if (vlen_out % vlen_in != 0)
        throw std::invalid_argument("vlen_out no multiple of vlen_in");
      if (address * vlen_in + vlen_out > total_size * vlen_in)
        throw std::out_of_range("vlen_out too long or address wrong");

      set_relative_rate(1 / total_size);
    }

    /*
     * Our virtual destructor.
     */
    select_subch_vfvf_impl::~select_subch_vfvf_impl()
    {
    }

    void
    select_subch_vfvf_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items * d_total_size;
    }

    int
    select_subch_vfvf_impl::general_work(int noutput_items,
                                         gr_vector_int &ninput_items,
                                         gr_vector_const_void_star &input_items,
                                         gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      for (int i = 0; i < noutput_items; i++) {
        memcpy(&out[i * d_vlen_out], &in[d_vlen_in * (i * d_total_size + d_address)],
               d_vlen_out * sizeof(float));
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(noutput_items * d_total_size);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab */
} /* namespace gr */

