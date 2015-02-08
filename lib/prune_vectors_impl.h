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
#ifndef INCLUDED_DAB_PRUNE_VECTORS_H
#define INCLUDED_DAB_PRUNE_VECTORS_H

#include <gr_sync_block.h>

class dab_prune_vectors;

typedef boost::shared_ptr<dab_prune_vectors> dab_prune_vectors_sptr;

dab_prune_vectors_sptr 
dab_make_prune_vectors (size_t itemsize, unsigned int length, unsigned int prune_start, unsigned int prune_end);

/*!
 * \brief Cuts away elements at the top and bottom of the vectors 
 * \ingroup misc
 *
 * input: vectors
 * output: pruned vectors
 * 
 * \param itemsize vector element size
 * \param length length of the vector
 * \param prune_start how many elements to cut away at the beginning of the vector
 * \param prune_end how many elements to cut away at the end of the vector
 *
 * constraint: prune_start + prune_end < length
 */
class dab_prune_vectors : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_prune_vectors to
    // access the private constructor.

    friend dab_prune_vectors_sptr
    dab_make_prune_vectors (size_t itemsize, unsigned int length, unsigned int prune_start, unsigned int prune_end);

    dab_prune_vectors (size_t itemsize, unsigned int length, unsigned int prune_start, unsigned int prune_end);    // private constructor

    size_t       d_itemsize;
    unsigned int d_length;
    unsigned int d_prune_start;
    unsigned int d_prune_end;

  public:
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_PRUNE_VECTORS_H */
