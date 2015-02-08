/* -*- c++ -*- */
/*
 * Copyright 2004,2007 Free Software Foundation, Inc.
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
#ifndef INCLUDED_DAB_MEASURE_PROCESSING_RATE_IMPL_H
#define INCLUDED_DAB_MEASURE_PROCESSING_RATE_IMPL_H

#include <dab/measure_processing_rate.h>

namespace gr {
  namespace dab {

class measure_processing_rate_impl : public measure_processing_rate
{

 private:
  size_t	d_itemsize;
  int d_samples_to_count;
  int d_count;
  struct timeval d_time;
  float d_processing_rate;

 public:
  measure_processing_rate_impl(size_t itemsize, int samples_to_count);
  void set_samples_to_count(int samples_to_count) { d_samples_to_count=samples_to_count; }
  /*! \return processing rate in samples per second */
  float processing_rate() { return d_processing_rate; }
  /*! \return processing rate in bits per second */
  float bitrate() { return d_itemsize*8*d_processing_rate; }

  int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);
};

}
}

#endif /* INCLUDED_DAB_MEASURE_PROCESSING_RATE_H */
