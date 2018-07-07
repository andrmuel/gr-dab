/* -*- c++ -*- */
/* 
 * Copyright 2018 <+YOU OR YOUR COMPANY+>.
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
#include "control_stream_to_tag_cc_impl.h"

namespace gr {
  namespace dab {

    control_stream_to_tag_cc::sptr
    control_stream_to_tag_cc::make(const std::string &tag_str, int vlen)
    {
      return gnuradio::get_initial_sptr
        (new control_stream_to_tag_cc_impl(tag_str, vlen));
    }

    /*
     * The private constructor
     */
    control_stream_to_tag_cc_impl::control_stream_to_tag_cc_impl(const std::string &tag_str, int vlen)
      : gr::sync_block("control_stream_to_tag_cc",
              gr::io_signature::make2(2, 2, sizeof(gr_complex)*vlen, sizeof(char)),
              gr::io_signature::make (1, 1, sizeof(gr_complex)*vlen))
    {
        d_vlen = vlen;
        d_stream_tag = pmt::intern(tag_str);
    }

    /*
     * Our virtual destructor.
     */
    control_stream_to_tag_cc_impl::~control_stream_to_tag_cc_impl()
    {
    }

    int
    control_stream_to_tag_cc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      const char *in_control = (const char *) input_items[1];
      gr_complex *out = (gr_complex *) output_items[0];

      for(int i=0;i<noutput_items;i++) {
        if(in_control[i] == 1) {
          add_item_tag(0, nitems_written(0) + i, d_stream_tag, pmt::intern(""), pmt::intern("control_stream_to_tag_cc"));
        }
      }
      memcpy(out, in, sizeof(gr_complex)*d_vlen*noutput_items);
      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab */
} /* namespace gr */

