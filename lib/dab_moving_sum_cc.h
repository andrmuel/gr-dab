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
#ifndef INCLUDED_DAB_MOVING_SUM_CC_H
#define INCLUDED_DAB_MOVING_SUM_CC_H

#include <gr_sync_block.h>

class dab_moving_sum_cc;

typedef std::shared_ptr<dab_moving_sum_cc> dab_moving_sum_cc_sptr;

dab_moving_sum_cc_sptr dab_make_moving_sum_cc (int length);

/*!
 * \brief Moving sum over a stream of complex floats.
 * \ingroup filter
 * \param length length of the moving sum (=number of taps)
 *
 * input: complex
 * output: complex
 *
 * This is the same as an FIR filter with length taps 1, but much faster
 * (linear time instead of O(n*m)). On the other hand, since only the diff is
 * calculated for each sample, there is some chance of an accumulating error.
 */
class dab_moving_sum_cc : public gr_sync_block
{
private:
  // The friend declaration allows dab_make_moving_sum_cc to
  // access the private constructor.

  friend dab_moving_sum_cc_sptr dab_make_moving_sum_cc (int length);

  dab_moving_sum_cc (int length);    // private constructor

  gr_complexd d_sum;
  int d_length;

 public:
  ~dab_moving_sum_cc ();  // public destructor
  int length() const {return d_length;}
  void reset() {d_sum=0;}

  // Where all the action really happens

  int work (int noutput_items,
            gr_vector_const_void_star &input_items,
            gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_MOVING_SUM_CC_H */
