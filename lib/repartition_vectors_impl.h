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
#ifndef INCLUDED_DAB_REPARTITION_VECTORS_IMPL_H
#define INCLUDED_DAB_REPARTITION_VECTORS_IMPL_H

#include <dab/repartition_vectors.h>

namespace gr {
  namespace dab {
/*! \brief reorder vectors to new vector size in order to organize
 *
 * input1: vector stream with vector length vlen_in
 * input2: trigger stream
 *
 * output1: vector streasm with vector length vlen_out
 * output2: trigger stream
 *
 * @param itemsize sizeof input and outputstream of port 0
 * @param vlen_in vector length of inputstream
 * @param vlen_out vector length of outputstream (repartitioned)
 * @param multiply number of input items which form one logical unit
 * @param divide number of input elements of size vlen_out which are passed through
 *
 */

class repartition_vectors_impl : public repartition_vectors
{
  private:

    size_t       d_itemsize;
    unsigned int d_vlen_in;
    unsigned int d_vlen_out;
    unsigned int d_multiply;
    unsigned int d_divide;
    unsigned int d_synced;

  public:
    repartition_vectors_impl(size_t itemsize, unsigned int vlen_in, unsigned int vlen_out, unsigned int multiply, unsigned int divide);
    void forecast (int noutput_items, gr_vector_int &ninput_items_required);
    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);
};

}
}

#endif /* INCLUDED_DAB_BLOCK_PARTITIONING_VBB_H */
