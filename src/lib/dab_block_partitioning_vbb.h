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
#ifndef INCLUDED_DAB_BLOCK_PARTITIONING_VBB_H
#define INCLUDED_DAB_BLOCK_PARTITIONING_VBB_H

#include <gr_block.h>

class dab_block_partitioning_vbb;

typedef boost::shared_ptr<dab_block_partitioning_vbb> dab_block_partitioning_vbb_sptr;

dab_block_partitioning_vbb_sptr 
dab_make_block_partitioning_vbb (unsigned int vlen_in, unsigned int vlen_out, unsigned int multiply, unsigned int divide);

/*!
 * \brief regroup vector elements
 * \ingroup DAB
 * 
 * \param vlen_in input vector length
 * \param vlen_out output vector length
 * \param multiply how many input vectors to concatenate
 * \param divide how many output vectors to cut concatenated vector into
 *
 * input: port 0: byte vectors; port 1: new trigger signal (char)
 * output: port 0: selected byte vectors; port 1: new trigger signal (char)
 *
 * first, m input vectors are concatenated, then the concatenated vector is cut
 * into d pieces (m: multiply, d: divide) - the output vector size is therefore
 *
 * vlen_out = vlen_in * multiply / divide
 *
 * the blocks are always aligned to the trigger signal
 */
class dab_block_partitioning_vbb : public gr_block
{
  private:
    // The friend declaration allows dab_make_block_partitioning_vbb to
    // access the private constructor.

    friend dab_block_partitioning_vbb_sptr
    dab_make_block_partitioning_vbb (unsigned int vlen_in, unsigned int vlen_out, unsigned int multiply, unsigned int divide);

    dab_block_partitioning_vbb (unsigned int vlen_in, unsigned int vlen_out, unsigned int multiply, unsigned int divide);    // private constructor

    unsigned int d_vlen_in;
    unsigned int d_vlen_out;
    unsigned int d_multiply;
    unsigned int d_divide;
    unsigned int d_synced;

  public:
    void forecast (int noutput_items, gr_vector_int &ninput_items_required);
    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_BLOCK_PARTITIONING_VBB_H */
