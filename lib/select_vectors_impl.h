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
#ifndef INCLUDED_DAB_SELECT_VECTORS_IMPL_H
#define INCLUDED_DAB_SELECT_VECTORS_IMPL_H

#include <dab/select_vectors.h>

namespace gr {
  namespace dab {

/*! \brief select a row of vectors
 *
 * input1: vector of size length*itemsize
 * input2: char stream with triggers for start of transmission frame
 *
 * output1: vector of size length*itemsize
 * output2: same as input2
 *
 * selects a row of vectors of the transmission frame; start of a transmission frame is triggerd by input2
 *
 * @param itemsize sizeof input and outputstream of port 0
 * @param length vector length
 * @param num_select number of vectors to select
 * @param num_skip number of vectors to skip before selection of num_select vectors
 *
 */
        class select_vectors_impl : public select_vectors {
        private:
            size_t d_itemsize;
            unsigned int d_length;
            unsigned int d_num_select;
            unsigned int d_num_skip;
            unsigned int d_index;

        public:
            select_vectors_impl(size_t itemsize, unsigned int length, unsigned int num_select, unsigned int num_skip);

            void forecast(int noutput_items, gr_vector_int &ninput_items_required);

            int general_work(int noutput_items,
                             gr_vector_int &ninput_items,
                             gr_vector_const_void_star &input_items,
                             gr_vector_void_star &output_items);
        };

    }
}

#endif /* INCLUDED_DAB_SELECT_VECTORS_H */
