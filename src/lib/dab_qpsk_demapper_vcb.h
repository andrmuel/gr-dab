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
#ifndef INCLUDED_DAB_QPSK_DEMAPPER_VCB_H
#define INCLUDED_DAB_QPSK_DEMAPPER_VCB_H

#include <gr_sync_block.h>

class dab_qpsk_demapper_vcb;

typedef boost::shared_ptr<dab_qpsk_demapper_vcb> dab_qpsk_demapper_vcb_sptr;

dab_qpsk_demapper_vcb_sptr 
dab_make_qpsk_demapper_vcb (int symbol_length);

/*!
 * \brief QPSK demapper - maps QPSK symbol vectors to byte vectors.
 *
 * value < 0 -> bit=1
 *
 * \ingroup DAB
 * 
 * \param symbol_length length of the symbol vector (i.e. number of occupied carriers)
 *
 * input: symbol vectors
 * output: byte vectors
 */
class dab_qpsk_demapper_vcb : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_qpsk_demapper_vcb to
    // access the private constructor.

    friend dab_qpsk_demapper_vcb_sptr
    dab_make_qpsk_demapper_vcb (int symbol_length);

    dab_qpsk_demapper_vcb (int symbol_length);    // private constructor

    int d_symbol_length;

  public:
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_QPSK_DEMAPPER_VCB_H */
