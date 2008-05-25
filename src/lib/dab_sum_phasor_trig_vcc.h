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
#ifndef INCLUDED_DAB_SUM_PHASOR_TRIG_VCC_H
#define INCLUDED_DAB_SUM_PHASOR_TRIG_VCC_H

#include <gr_sync_block.h>

class dab_sum_phasor_trig_vcc;

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
typedef boost::shared_ptr<dab_sum_phasor_trig_vcc> dab_sum_phasor_trig_vcc_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dab_sum_phasor_trig_vcc.
 *
 * To avoid accidental use of raw pointers, dab_sum_phasor_trig_vcc's
 * constructor is private.  dab_make_sum_phasor_trig_vcc is the public
 * interface for creating new instances.
 */
dab_sum_phasor_trig_vcc_sptr 
dab_make_sum_phasor_trig_vcc (unsigned int length);

/*!
 * \brief Sums up the phase of consecutive symbol vectors.
 *
 * When a new frame starts (trig == 1), the pilot symbol is produced directly, without any summing up:
 *  y[i] = x[i]
 * 
 * Otherwise:
 *  y[i] = x[i]*y[i-1]
 *
 *  NOTE: This means it's important that the absolute value of the symbols is 1.
 *
 * \ingroup DAB
 * 
 * \param length length of the symbol vector
 */
class dab_sum_phasor_trig_vcc : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_sum_phasor_trig_vcc to
    // access the private constructor.

    friend dab_sum_phasor_trig_vcc_sptr
    dab_make_sum_phasor_trig_vcc (unsigned int length);

    dab_sum_phasor_trig_vcc (unsigned int length);    // private constructor

    unsigned int d_length;
    std::vector<gr_complex> d_last_symbol;


  public:
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_SUM_PHASOR_TRIG_VCC_H */
