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
#ifndef INCLUDED_DAB_MODULO_FF_H
#define INCLUDED_DAB_MODULO_FF_H

#include <gr_sync_block.h>

class dab_modulo_ff;

typedef boost::shared_ptr<dab_modulo_ff> dab_modulo_ff_sptr;

dab_modulo_ff_sptr dab_make_modulo_ff (float div);

/*!
 * \brief Modulo operation: y[i] = x[i] mod div
 * \ingroup math
 * \param div divisor
 *
 * input: float
 * output: float
 */
class dab_modulo_ff : public gr_sync_block
{
private:
  // The friend declaration allows dab_make_modulo_ff to
  // access the private constructor.

  friend dab_modulo_ff_sptr dab_make_modulo_ff (float div);

  dab_modulo_ff (float div);    // private constructor

  float d_div;

 public:
  ~dab_modulo_ff ();  // public destructor

  // Where all the action really happens
  int work (int noutput_items,
            gr_vector_const_void_star &input_items,
            gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_MODULO_FF_H */
