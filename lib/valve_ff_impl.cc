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
#include "valve_ff_impl.h"

namespace gr {
  namespace dab {

    valve_ff::sptr
    valve_ff::make(bool closed, bool feed_with_zeros)
    {
      return gnuradio::get_initial_sptr
        (new valve_ff_impl(closed, feed_with_zeros));
    }

    /*
     * The private constructor
     */
    valve_ff_impl::valve_ff_impl(bool closed, bool feed_with_zeros)
      : gr::block("valve_ff",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(float))),
        d_feed_with_zeros(feed_with_zeros), d_closed(closed)
    {}

    /*
     * Our virtual destructor.
     */
    valve_ff_impl::~valve_ff_impl()
    {
    }

    void
    valve_ff_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    int
    valve_ff_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      if (d_closed){
        if (d_feed_with_zeros){
          // send zeros instead of the incoming floats as idle state
          memset(out, 0, noutput_items * sizeof(float));
          consume_each (noutput_items);
          return noutput_items;
        }
        else{
          // dump incoming frames and send nothing
          consume_each (noutput_items);
          return 0;
        }
      }
      else{
        // valve opened, simply pass through the floats
        memcpy(out, in, noutput_items * sizeof(float));
        consume_each (noutput_items);
        return noutput_items;
      }
    }

  } /* namespace dab */
} /* namespace gr */

