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

#include <dab_measure_processing_rate.h>
#include <gr_io_signature.h>
#include <stdexcept>
#include <sys/time.h>

dab_measure_processing_rate_sptr
dab_make_measure_processing_rate (size_t itemsize, int samples_to_count)
{
  return dab_measure_processing_rate_sptr (new dab_measure_processing_rate (itemsize, samples_to_count));
}

dab_measure_processing_rate::dab_measure_processing_rate(size_t itemsize, int samples_to_count)
  : gr_sync_block ("measure_processing_rate",
		   gr_make_io_signature(1, 1, itemsize),
		   gr_make_io_signature(0, 0, 0)),
    d_itemsize(itemsize), d_samples_to_count(samples_to_count), d_count(0), d_processing_rate(0)
{
  if (gettimeofday(&d_time, NULL) != 0) {
    perror("dab_measure_processing_rate: gettimeofday");
    exit(-1);
  }
}

int 
dab_measure_processing_rate::work (int noutput_items,
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
