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
#ifndef INCLUDED_DAB_UNPUNCTURE_VFF_IMPL_H
#define INCLUDED_DAB_UNPUNCTURE_VFF_IMPL_H

#include <dab/unpuncture_vff.h>

namespace gr {
  namespace dab {

class unpuncture_vff_impl : public unpuncture_vff
{
  private:
    unsigned int ones (const std::vector<unsigned char> &puncturing_vector);

    std::vector<unsigned char> d_puncturing_vector;
    float d_fillval;
    unsigned int d_vlen_in;
    unsigned int d_vlen_out;

  public:
    unpuncture_vff_impl(const std::vector<unsigned char> &puncturing_vector, float fillval);
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

}
}

#endif /* INCLUDED_DAB_UNPUNCTURE_VFF_H */
