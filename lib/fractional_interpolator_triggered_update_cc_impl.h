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
#ifndef INCLUDED_DAB_FRACTIONAL_INTERPOLATOR_TRIGGERED_UPDATE_CC_IMPL_H
#define INCLUDED_DAB_FRACTIONAL_INTERPOLATOR_TRIGGERED_UPDATE_CC_IMPL_H

#include <dab/fractional_interpolator_triggered_update_cc.h>
#include <gnuradio/filter/mmse_fir_interpolator_cc.h>

namespace gr {
  namespace dab {

class fractional_interpolator_triggered_update_cc_impl : public fractional_interpolator_triggered_update_cc
{
  public:
    fractional_interpolator_triggered_update_cc_impl(float phase_shift, float interp_ratio);
    ~fractional_interpolator_triggered_update_cc_impl();
    void forecast(int noutput_items, gr_vector_int &ninput_items_required);
    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);

    float mu() const { return d_mu;}
    float interp_ratio() const { return d_mu_inc;}
    void set_mu (float mu) { d_mu = mu; }
    void set_interp_ratio (float interp_ratio) { d_next_mu_inc = interp_ratio; }


  private:
    float d_mu;
    float d_mu_inc;
    float d_next_mu_inc;
    gr::filter::mmse_fir_interpolator_cc *d_interp;

};

}
}

#endif
