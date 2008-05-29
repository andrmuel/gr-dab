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

#ifndef INCLUDED_DAB_MEASURE_PROCESSING_RATE_H
#define INCLUDED_DAB_MEASURE_PROCESSING_RATE_H

#include <gr_sync_block.h>

class dab_measure_processing_rate;
typedef boost::shared_ptr<dab_measure_processing_rate> dab_measure_processing_rate_sptr;

dab_measure_processing_rate_sptr dab_make_measure_processing_rate(size_t itemsize, int samples_to_count);

/*!
 * \brief Measure processing rate of a stream
 *
 * \param itemsize size of items (gr.sizeof_foo)
 * \param samples_to_count number of samples until updating the value - for good estimations, use at least the number of samples expected in one second
 *
 * input: sample stream
 *
 * \ingroup sink
 */
class dab_measure_processing_rate : public gr_sync_block
{
  friend dab_measure_processing_rate_sptr dab_make_measure_processing_rate(size_t itemsize, int samples_to_count);

 private:
  size_t	d_itemsize;
  int d_samples_to_count;
  int d_count;
  struct timeval d_time;
  float d_processing_rate;

 protected:
  dab_measure_processing_rate(size_t itemsize, int samples_to_count);

 public:
  void set_samples_to_count(int samples_to_count) { d_samples_to_count=samples_to_count; }
  float processing_rate() { return d_processing_rate; }

  int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_MEASURE_PROCESSING_RATE_H */
