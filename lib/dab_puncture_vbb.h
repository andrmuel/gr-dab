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

#ifndef INCLUDED_DAB_PUNCTURE_VBB_H
#define INCLUDED_DAB_PUNCTURE_VBB_H

#include <gr_sync_block.h>

class dab_puncture_vbb;

typedef std::shared_ptr <dab_puncture_vbb> dab_puncture_vbb_sptr;

dab_puncture_vbb_sptr
dab_make_puncture_vbb(const std::vector<unsigned char> &puncturing_vector);

/*!
 * \brief Puncturing - remove bits, where the puncturing sequence is zero
 * \ingroup DAB
 * \param puncturing_vector describes, which bits are removed (1=keep, 0=remove)
 *
 * input: byte vector whose length equals the length of the puncturing vector
 * output: byte vector whose length equeals the number of ones in the puncturing vector
 */
class dab_puncture_vbb : public gr_sync_block {
private:
  friend dab_puncture_vbb_sptr
  dab_make_puncture_vbb(const std::vector<unsigned char> &puncturing_vector);

  unsigned int ones(const std::vector<unsigned char> &puncturing_vector);

  dab_puncture_vbb(const std::vector<unsigned char> &puncturing_vector);    // private constructor

  std::vector<unsigned char> d_puncturing_vector;
  unsigned int d_vlen_in;
  unsigned int d_vlen_out;

public:
  int work(int noutput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_PUNCTURE_VBB_H */
