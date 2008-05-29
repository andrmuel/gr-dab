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
#ifndef INCLUDED_DAB_QPSK_MAPPER_VBC_H
#define INCLUDED_DAB_QPSK_MAPPER_VBC_H

#include <gr_sync_block.h>

#define I_SQRT2 0.707106781187

class dab_qpsk_mapper_vbc;

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
typedef boost::shared_ptr<dab_qpsk_mapper_vbc> dab_qpsk_mapper_vbc_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dab_qpsk_mapper_vbc.
 *
 * To avoid accidental use of raw pointers, dab_qpsk_mapper_vbc's
 * constructor is private.  dab_make_qpsk_mapper_vbc is the public
 * interface for creating new instances.
 */
dab_qpsk_mapper_vbc_sptr 
dab_make_qpsk_mapper_vbc (int symbol_length);

/*!
 * \brief Maps byte vectors to complex symbol vectors.
 * \ingroup DAB
 * \param symbol_length length of the symbol vector (i.e. number of occupied carriers)
 *
 * input: byte vectors
 * output: symbol vectors
 */
class dab_qpsk_mapper_vbc : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_qpsk_mapper_vbc to
    // access the private constructor.

    friend dab_qpsk_mapper_vbc_sptr
    dab_make_qpsk_mapper_vbc (int symbol_length);

    dab_qpsk_mapper_vbc (int symbol_length);    // private constructor

    int d_symbol_length;

  public:
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_QPSK_MAPPER_VBC_H */
