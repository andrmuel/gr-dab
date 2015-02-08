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
#ifndef INCLUDED_DAB_OFDM_REMOVE_FIRST_SYMBOL_VCC_IMPL_H
#define INCLUDED_DAB_OFDM_REMOVE_FIRST_SYMBOL_VCC_IMPL_H

#include <dab/ofdm_remove_first_symbol_vcc.h>

namespace gr {
  namespace dab {
class ofdm_remove_first_symbol_vcc_impl : public ofdm_remove_first_symbol_vcc
{
  private:

    unsigned int d_vlen;
    char d_start;

  public:
    ofdm_remove_first_symbol_vcc_impl(unsigned int vlen);
    void forecast (int noutput_items, gr_vector_int &ninput_items_required);

    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);
};

}
}
#endif /* INCLUDED_DAB_OFDM_REMOVE_FIRST_SYMBOL_VCC_H */

