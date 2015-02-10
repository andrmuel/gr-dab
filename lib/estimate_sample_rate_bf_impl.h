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

#ifndef INCLUDED_DAB_ESTIMATE_SAMPLE_RATE_BF_IMPL_H
#define INCLUDED_DAB_ESTIMATE_SAMPLE_RATE_BF_IMPL_H

#include <dab/estimate_sample_rate_bf.h>

namespace gr {
  namespace dab {

class estimate_sample_rate_bf_impl : public estimate_sample_rate_bf
{
  private:

    int d_zeros;
    float d_expected_sample_rate;
    float d_real_sample_rate;
    char d_found_first_frame;
    int d_frame_length;

  public:
    estimate_sample_rate_bf_impl(float expected_sample_rate, int frame_length);
    ~estimate_sample_rate_bf_impl ();  // public destructor

    // Where all the action really happens

    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};
}
}
#endif /* INCLUDED_DAB_ESTIMATE_SAMPLE_RATE_BF_H */

