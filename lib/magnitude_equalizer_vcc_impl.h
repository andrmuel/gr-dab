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

#ifndef INCLUDED_DAB_MAGNITUDE_EQUALIZER_VCC_IMPL_H
#define INCLUDED_DAB_MAGNITUDE_EQUALIZER_VCC_IMPL_H

#include <dab/magnitude_equalizer_vcc.h>

namespace gr {
  namespace dab {

class magnitude_equalizer_vcc_impl : public magnitude_equalizer_vcc
{
  private:
    void update_equalizer(const gr_complex *in);

    unsigned int d_vlen;
    unsigned int d_num_symbols;
    float *d_equalizer;
    int d_add_item_tag_at;

  public:
    magnitude_equalizer_vcc_impl(unsigned int vlen, unsigned int num_symbols);
    ~magnitude_equalizer_vcc_impl(void);
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

}
}

#endif /* INCLUDED_DAB_MAGNITUDE_EQUALIZER_VCC_H */
