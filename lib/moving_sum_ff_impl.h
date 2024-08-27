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
#ifndef INCLUDED_DAB_MOVING_SUM_FF_IMPL_H
#define INCLUDED_DAB_MOVING_SUM_FF_IMPL_H

#include <dab/moving_sum_ff.h>

namespace gr {
  namespace dab {

class moving_sum_ff_impl : public moving_sum_ff
{
private:


  double d_sum;
  int d_length;

 public:
  moving_sum_ff_impl(int length);
  ~moving_sum_ff_impl();
  int length() const {return d_length;}
  void reset() {d_sum=0;}

  // Where all the action really happens

  int work (int noutput_items,
            gr_vector_const_void_star &input_items,
            gr_vector_void_star &output_items);

    bool stop();
};

}
}

#endif /* INCLUDED_DAB_MOVING_SUM_FF_H */
