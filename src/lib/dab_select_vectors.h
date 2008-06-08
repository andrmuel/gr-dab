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
#ifndef INCLUDED_DAB_SELECT_VECTORS_H
#define INCLUDED_DAB_SELECT_VECTORS_H

#include <gr_block.h>

class dab_select_vectors;

typedef boost::shared_ptr<dab_select_vectors> dab_select_vectors_sptr;

dab_select_vectors_sptr 
dab_make_select_vectors (size_t itemsize, unsigned int length, unsigned int num_select, unsigned int num_skip);

/*!
 * \brief select some vectors from a vector stream
 * \ingroup DAB
 *
 * \param itemsize size of vector elements
 * \param length vector length
 * \param num_select number of vectors to select
 * \param num_skip number of vectors to skip at the start
 *
 * select some vectors depending on their position relative to the frame start, which is indicatied by the trigger signal
 *
 * input: port 0: byte vectors; port 1: new trigger signal (char)
 * output: port 0: selected byte vectors; port 1: new trigger signal (char)
 */
class dab_select_vectors : public gr_block
{
  private:
    // The friend declaration allows dab_make_select_vectors to
    // access the private constructor.

    friend dab_select_vectors_sptr
    dab_make_select_vectors (size_t itemsize, unsigned int length, unsigned int num_select, unsigned int num_skip);

    dab_select_vectors (size_t itemsize, unsigned int length, unsigned int num_select, unsigned int num_skip);    // private constructor

    size_t       d_itemsize;
    unsigned int d_length;
    unsigned int d_num_select;
    unsigned int d_num_skip;
    unsigned int d_index;

  public:
    void forecast (int noutput_items, gr_vector_int &ninput_items_required);
    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_SELECT_VECTORS_H */
