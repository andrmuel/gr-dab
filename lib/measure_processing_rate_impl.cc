/* -*- c++ -*- */
/*
 * Copyright 2004,2006,2007 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdio.h>

#include <gnuradio/io_signature.h>
#include "measure_processing_rate_impl.h"
#include <stdexcept>
#include <sys/time.h>

namespace gr {
  namespace dab {

measure_processing_rate::sptr
measure_processing_rate::make(size_t itemsize, int samples_to_count)
{
  return gnuradio::get_initial_sptr
    (new measure_processing_rate_impl(itemsize, samples_to_count));
}

measure_processing_rate_impl::measure_processing_rate_impl(size_t itemsize, int samples_to_count)
  : gr::sync_block("measure_processing_rate",
		   gr::io_signature::make(1, 1, itemsize),
		   gr::io_signature::make(0, 0, 0)),
    d_itemsize(itemsize), d_samples_to_count(samples_to_count), d_count(0), d_processing_rate(0)
{
  if (gettimeofday(&d_time, NULL) != 0) {
    perror("dab_measure_processing_rate: gettimeofday");
    exit(-1);
  }
}

int 
measure_processing_rate_impl::work(int noutput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items)
{
  d_count+=noutput_items;

  struct timeval cur_time;

  if (d_count >= d_samples_to_count) {
    d_count -= d_samples_to_count;
    if (gettimeofday(&cur_time, NULL) != 0) {
      perror("dab_measure_processing_rate: gettimeofday");
      exit(-1);
    }
    d_processing_rate = (float)d_samples_to_count/((float)(cur_time.tv_sec - d_time.tv_sec) + (float)(cur_time.tv_usec - d_time.tv_usec)/1000000);
    d_time = cur_time;
    // printf("processing rate: %f\n", d_processing_rate);
  }
  
  return noutput_items;
}

}
}
