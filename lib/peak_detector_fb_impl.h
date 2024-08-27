/* -*- c++ -*- */
/* This is a version of the GNU Radio peak_detector_fb block before commit 9d9ea63c45b5f314eb344a69340ef49e8edafdfa.
 *
 * Copyright 2007,2010,2013 Free Software Foundation, Inc.
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

#ifndef INCLUDED_DAB_PEAK_DETECTOR_FB_IMPL_H
#define INCLUDED_DAB_PEAK_DETECTOR_FB_IMPL_H

#include <dab/peak_detector_fb.h>

namespace gr {
  namespace dab {

    class peak_detector_fb_impl : public peak_detector_fb
    {
     private:
      float d_threshold_factor_rise;
      float d_threshold_factor_fall;
      int d_look_ahead;
      float d_avg_alpha;
      float d_avg;
      unsigned char d_found;
      unsigned char d_state;
      float d_peak_val;

     public:
      peak_detector_fb_impl(float threshold_factor_rise, float threshold_factor_fall, int look_ahead, float alpha);
      ~peak_detector_fb_impl();

      void set_threshold_factor_rise(float thr) { d_threshold_factor_rise = thr; }
      void set_threshold_factor_fall(float thr) { d_threshold_factor_fall = thr; }
      void set_look_ahead(int look) { d_look_ahead = look; }
      void set_alpha(float alpha) { d_avg_alpha = alpha; }
      float threshold_factor_rise() { return d_threshold_factor_rise; }
      float threshold_factor_fall() { return d_threshold_factor_fall; }
      int look_ahead() { return d_look_ahead; }
      float alpha() { return d_avg_alpha; }

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_PEAK_DETECTOR_FB_IMPL_H */

