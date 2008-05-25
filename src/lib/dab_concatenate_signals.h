/* -*- c++ -*- */
/*
 * Copyright 2008 Free Software Foundation, Inc.
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

#ifndef INCLUDED_DAB_CONCATENATE_SIGNALS_CC_H
#define INCLUDED_DAB_CONCATENATE_SIGNALS_CC_H

#include <gr_block.h>

class dab_concatenate_signals;
typedef boost::shared_ptr<dab_concatenate_signals> dab_concatenate_signals_sptr;

dab_concatenate_signals_sptr dab_make_concatenate_signals ();

/*!
 * \brief Concatenate all input signals in time
 *
 * Output first signal, as long as it has samples, then second signal, etc...
 */
class dab_concatenate_signals : public gr_block
{
  private:
    friend dab_concatenate_signals_sptr dab_make_concatenate_signals ();

    dab_concatenate_signals ();

    unsigned int d_current_signal;
    unsigned int d_callmetwice;

  public:

    void forecast (int noutput_items, gr_vector_int &ninput_items_required);
    int general_work(int noutput_items,
                     gr_vector_int &ninput_items,
                     gr_vector_const_void_star &input_items,
                     gr_vector_void_star &output_items);
};

#endif
