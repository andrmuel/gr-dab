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
typedef boost::shared_ptr<dab_moving_sum_cc> dab_moving_sum_cc_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dab_moving_sum_cc.
 *
 * To avoid accidental use of raw pointers, dab_moving_sum_cc's
 * constructor is private.  dab_make_moving_sum_cc is the public
 * interface for creating new instances.
 */
dab_moving_sum_cc_sptr dab_make_moving_sum_cc (int length);

/*!
 * \brief Moving sum over a stream of complex floats.
 * \ingroup misc
 *
 * This uses the preferred technique: subclassing gr_sync_block.
 */
class dab_moving_sum_cc : public gr_sync_block
{
private:
  // The friend declaration allows dab_make_moving_sum_cc to
  // access the private constructor.

  friend dab_moving_sum_cc_sptr dab_make_moving_sum_cc (int length);

  dab_moving_sum_cc (int length);  	// private constructor

  gr_complexd d_sum;
  int d_length;

 public:
  ~dab_moving_sum_cc ();	// public destructor
  int length() const {return d_length;}
  void set_length(int length) {set_history(length+1); d_length=length;}

  // Where all the action really happens

  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_MOVING_SUM_CC_H */
