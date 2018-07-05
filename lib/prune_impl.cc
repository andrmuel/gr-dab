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
#include "prune_impl.h"
#include <stdexcept>
#include <stdio.h>
#include <sstream>
#include <boost/format.hpp>

namespace gr {
  namespace dab {

    prune::sptr
    prune::make(size_t itemsize, unsigned int length, unsigned int prune_start, unsigned int prune_end)
    {
      return gnuradio::get_initial_sptr
              (new prune_impl(itemsize, length, prune_start, prune_end));
    }

    /*
     * The private constructor
     */
    prune_impl::prune_impl(size_t itemsize, unsigned int length, unsigned int prune_start, unsigned int prune_end)
            : gr::block("prune",
                        gr::io_signature::make(1, 1, sizeof(char)),
                        gr::io_signature::make(1, 1, sizeof(char))),
              d_itemsize(itemsize), d_length(length), d_prune_start(prune_start), d_prune_end(prune_end)
    {
      if (prune_start + prune_end > length)
        throw std::out_of_range((boost::format("want to cut %d more items than stream is long") % (prune_start + prune_end - length)).str());

      set_output_multiple(length - prune_start - prune_end);
      set_relative_rate((length - prune_start - prune_end) / length);
    }

    /*
     * Our virtual destructor.
     */
    prune_impl::~prune_impl()
    {
    }

    void
    prune_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = (noutput_items / (d_length - d_prune_start - d_prune_end)) * d_length;
    }

    int
    prune_impl::general_work(int noutput_items,
                             gr_vector_int &ninput_items,
                             gr_vector_const_void_star &input_items,
                             gr_vector_void_star &output_items)
    {
      const char *in = (const char *) input_items[0];
      char *out = (char *) output_items[0];
      for (int i = 0; i < noutput_items / (d_length - d_prune_start - d_prune_end); i++) {
        memcpy(out, in + d_prune_start * d_itemsize, (d_length - d_prune_start - d_prune_end) * d_itemsize);
        in += d_length * d_itemsize;
        out += (d_length - d_prune_start - d_prune_end) * d_itemsize;
      }
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each((noutput_items / (d_length - d_prune_start - d_prune_end)) * d_length);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace dab */
} /* namespace gr */

