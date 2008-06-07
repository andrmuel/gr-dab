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
#ifndef INCLUDED_DAB_MAGNITUDE_EQUALIZER_VCC_H
#define INCLUDED_DAB_MAGNITUDE_EQUALIZER_VCC_H

#include <gr_sync_block.h>

class dab_magnitude_equalizer_vcc;

typedef boost::shared_ptr<dab_magnitude_equalizer_vcc> dab_magnitude_equalizer_vcc_sptr;

dab_magnitude_equalizer_vcc_sptr dab_make_magnitude_equalizer_vcc (unsigned int vlen, unsigned int num_symbols);

/*!
 * \brief Removes the first symbol of each frame
 * \ingroup DAB
 * \param vlen length of the symbol vectors
 *
 * input: port 0: complex vectors; port 1: byte stream - trigger signal indicating the start of a frame
 * output: port 0: complex vectors; port 1: byte stream - trigger signal indicating the start of a frame
 *
 *
 * this block introduces a delay of num_symbols-1 on both the data and trigger signal
 */
class dab_magnitude_equalizer_vcc : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_magnitude_equalizer_vcc to
    // access the private constructor.

    friend dab_magnitude_equalizer_vcc_sptr dab_make_magnitude_equalizer_vcc (unsigned int vlen, unsigned int num_symbols);

    dab_magnitude_equalizer_vcc (unsigned int vlen, unsigned int num_symbols);    // private constructor
    void update_equalizer(const gr_complex *in);

    unsigned int d_vlen;
    unsigned int d_num_symbols;
    float *d_equalizer;

  public:
    ~dab_magnitude_equalizer_vcc (void);
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_MAGNITUDE_EQUALIZER_VCC_H */
