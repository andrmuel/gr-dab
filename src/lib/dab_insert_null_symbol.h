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
#ifndef INCLUDED_DAB_INSERT_NULL_SYMBOL_H
#define INCLUDED_DAB_INSERT_NULL_SYMBOL_H

#include <gr_block.h>

class dab_insert_null_symbol;

typedef boost::shared_ptr<dab_insert_null_symbol> dab_insert_null_symbol_sptr;

dab_insert_null_symbol_sptr dab_make_insert_null_symbol (int ns_length, int symbol_length);

/*!
 * \brief Inserts a Null symbol at the start of the frame.
 * \ingroup DAB
 * \param ns_length number of samples that makes a Null symbol
 * \param symbol_length number of samples in an ordinary symbol_length
 *
 * input: port 0: complex vector stream with the actual data; port 1: trigger signal indicating the start of a frame
 * output: complex stream
 */
class dab_insert_null_symbol : public gr_block
{
  private:
    // The friend declaration allows dab_make_insert_null_symbol to
    // access the private constructor.

    friend dab_insert_null_symbol_sptr dab_make_insert_null_symbol (int ns_length, int symbol_length);

    dab_insert_null_symbol (int ns_length, int symbol_length);    // private constructor

    int d_ns_length;
    int d_symbol_length;
    int d_ns_added;

  public:
    void forecast (int noutput_items, gr_vector_int &ninput_items_required);

    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_INSERT_NULL_SYMBOL_H */
