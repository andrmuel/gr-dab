/* -*- c++ -*- */
/*
 * Copyright 2004,2007 Free Software Foundation, Inc.
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

#ifndef INCLUDED_DAB_FRACTIONAL_INTERPOLATOR_TRIGGERED_UPDATE_CC_H
#define INCLUDED_DAB_FRACTIONAL_INTERPOLATOR_TRIGGERED_UPDATE_CC_H

#include <gr_block.h>

class gri_mmse_fir_interpolator_cc;

class dab_fractional_interpolator_triggered_update_cc;
typedef boost::shared_ptr<dab_fractional_interpolator_triggered_update_cc> dab_fractional_interpolator_triggered_update_cc_sptr;

// public constructor
dab_fractional_interpolator_triggered_update_cc_sptr dab_make_fractional_interpolator_triggered_update_cc (float phase_shift, float interp_ratio);

/*!
 * \brief Interpolating mmse filter with gr_complex input, gr_complex output
 *
 * Taken from the GNU Radio code base and adapted to allow updating of the interpolation ratio at triggered instants.
 * (subclassing gr_fractional_interpolator_cc gets me into a mess ..)
 *
 * This is most probably overkill, as the changes in the sample rate are usually very small.
 *
 * \ingroup filter
 */
class dab_fractional_interpolator_triggered_update_cc : public gr_block
{
  public:
    ~dab_fractional_interpolator_triggered_update_cc ();
    void forecast(int noutput_items, gr_vector_int &ninput_items_required);
    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);

    float mu() const { return d_mu;}
    float interp_ratio() const { return d_mu_inc;}
    void set_mu (float mu) { d_mu = mu; }
    void set_interp_ratio (float interp_ratio) { d_next_mu_inc = interp_ratio; }

  protected:
    dab_fractional_interpolator_triggered_update_cc (float phase_shift, float interp_ratio);

  private:
    float d_mu;
    float d_mu_inc;
    float d_next_mu_inc;
    gri_mmse_fir_interpolator_cc *d_interp;

    friend dab_fractional_interpolator_triggered_update_cc_sptr
    dab_make_fractional_interpolator_triggered_update_cc (float phase_shift, float interp_ratio);
};

#endif
