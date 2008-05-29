/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
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
#ifndef INCLUDED_DAB_ESTIMATE_SAMPLE_RATE_BF_H
#define INCLUDED_DAB_ESTIMATE_SAMPLE_RATE_BF_H

#include <gr_sync_block.h>

class dab_estimate_sample_rate_bf;

/*
 * We use boost::shared_ptr's instead of raw pointers for all access
 * to gr_blocks (and many other data structures).  The shared_ptr gets
 * us transparent reference counting, which greatly simplifies storage
 * management issues.  This is especially helpful in our hybrid
 * C++ / Python system.
 *
 * See http://www.boost.org/libs/smart_ptr/smart_ptr.htm
 *
 * As a convention, the _sptr suffix indicates a boost::shared_ptr
 */
typedef boost::shared_ptr<dab_estimate_sample_rate_bf> dab_estimate_sample_rate_bf_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dab_estimate_sample_rate_bf.
 *
 * To avoid accidental use of raw pointers, dab_estimate_sample_rate_bf's
 * constructor is private.  dab_make_estimate_sample_rate_bf is the public
 * interface for creating new instances.
 */
dab_estimate_sample_rate_bf_sptr dab_make_estimate_sample_rate_bf (float expected_sample_rate, int frame_length);

/*!
 * \brief Estimate the sample rate of a DAB stream from the detected frame starts
 * \ingroup DAB
 *
 * \param expected_sample_rate exact value of the sample rate if there are no inaccuracies
 * \param frame_length length of a DAB frame in samples
 */
class dab_estimate_sample_rate_bf : public gr_sync_block
{
private:
  // The friend declaration allows dab_make_estimate_sample_rate_bf to
  // access the private constructor.

  friend dab_estimate_sample_rate_bf_sptr dab_make_estimate_sample_rate_bf (float expected_sample_rate, int frame_length);

  dab_estimate_sample_rate_bf (float expected_sample_rate, int frame_length);    // private constructor

  int d_zeros;
  float d_expected_sample_rate;
  float d_real_sample_rate;
  char d_found_first_frame;
  int d_frame_length;

 public:
  ~dab_estimate_sample_rate_bf ();  // public destructor

  // Where all the action really happens

  int work (int noutput_items,
            gr_vector_const_void_star &input_items,
            gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_ESTIMATE_SAMPLE_RATE_BF_H */
