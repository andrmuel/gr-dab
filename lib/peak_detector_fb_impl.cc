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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "peak_detector_fb_impl.h"
#include <string.h>

namespace gr {
  namespace dab {

    peak_detector_fb::sptr
    peak_detector_fb::make(float threshold_factor_rise, float threshold_factor_fall, int look_ahead, float alpha)
    {
      return gnuradio::get_initial_sptr
        (new peak_detector_fb_impl(threshold_factor_rise, threshold_factor_fall, look_ahead, alpha));
    }

    /*
     * The private constructor
     */
    peak_detector_fb_impl::peak_detector_fb_impl(float threshold_factor_rise, float threshold_factor_fall, int look_ahead, float alpha)
      : gr::sync_block("peak_detector_fb",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(char))),
        d_threshold_factor_rise(threshold_factor_rise),
        d_threshold_factor_fall(threshold_factor_fall),
        d_look_ahead(look_ahead), d_avg_alpha(alpha), d_avg(0), d_found(0)
    {d_state = 0;
     d_peak_val = -(float)INFINITY;
    d_peak_add_next = 0;
    }

    /*
     * Our virtual destructor.
     */
    peak_detector_fb_impl::~peak_detector_fb_impl()
    {
    }

    int
    peak_detector_fb_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      float *iptr = (float*)input_items[0];
      char *optr = (char*)output_items[0];

      memset(optr, 0, noutput_items*sizeof(char));

      int peak_ind = 0;
      int i = 0;

      //printf("noutput_items %d\n",noutput_items);
      while(i < noutput_items) {
        if(d_state == 0) {  // below threshold
          if(iptr[i] > d_avg*d_threshold_factor_rise) {
            d_state = 1;
          }
          else {
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
            i++;
          }
        }
        else if(d_state == 1) {  // above threshold, have not found peak
          //printf("Entered State 1: %f  i: %d  noutput_items: %d\n", iptr[i], i, noutput_items);
          if(iptr[i] > d_peak_val) {
            d_peak_val = iptr[i];
            peak_ind = i;
            d_peak_add_next = 1;
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
            i++;
          }
          else if(iptr[i] > d_avg*d_threshold_factor_fall) {
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
            i++;
          }
          else {
            if (d_peak_add_next) { 
              if (i > 0)
                optr[i-1] = 1;
              else
                optr[i] = 1;
              d_peak_add_next = 0;
              printf("Peak add at %d\n", nitems_written(0) + i);
            }
            d_state = 0;
            d_peak_val = -(float)INFINITY;
            //printf("Leaving  State 1: Peak: %f  Peak Ind: %d   i: %d  noutput_items: %d\n",
            //peak_val, peak_ind, i, noutput_items);
          }
        }
      }

      //if(d_state == 0) {
        //printf("Leave in State 0, produced %d\n",noutput_items);
        return noutput_items;
      //}
      //else {   // only return up to passing the threshold
      //  //printf("Leave in State 1, only produced %d of %d\n",peak_ind,noutput_items);
      //  return outc;
      //}
    }

  } /* namespace dab */
} /* namespace gr */

