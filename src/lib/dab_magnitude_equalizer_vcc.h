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

dab_magnitude_equalizer_vcc_sptr 
dab_make_magnitude_equalizer_vcc (unsigned int vlen, float alpha = 0.01, unsigned int decimate = 1, float magnitude = 1);

/*!
 * \brief Individual magnitude equalisation for each frequency (i.e. vector element)
 * \ingroup DAB
 * 
 * \param vlen length of the vector
 * \param alpha adaptation speed fatcor: equalisation factor = (1-alpha) * old factor + alpha * new factor
 * \param decimate if you don't want to update the equalisation factors for every new vector, set this > 1, to use only every n-th vector (this helps to reclaim some CPU cycles; be sure to adjust alpha accordingly)
 * \float magnitude target magnitude for equalisation
 *
 * input: complex vector stream
 * output: complex vector stream with equalized magnitudes
 */
class dab_magnitude_equalizer_vcc : public gr_sync_block
{
  private:
    friend dab_magnitude_equalizer_vcc_sptr
    dab_make_magnitude_equalizer_vcc (unsigned int vlen, float alpha, unsigned int decimate, float magnitude);

    dab_magnitude_equalizer_vcc (unsigned int vlen, float alpha, unsigned int decimate, float magnitude);    // private constructor

    unsigned int d_vlen;
    float d_alpha;
    unsigned int d_decimate;
    float d_magnitude;
    float * d_equalisation_factors;
    unsigned int d_count;

  public:
    ~dab_magnitude_equalizer_vcc (void);
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_MAGNITUDE_EQUALIZER_VCC_H */
