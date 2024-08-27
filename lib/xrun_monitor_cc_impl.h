/* -*- c++ -*- */
/* 
 * Copyright 2018 Ruben Undheim <ruben.undheim@gmail.com>
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_CAPTURE_TOOLS_XRUN_MONITOR_CC_IMPL_H
#define INCLUDED_CAPTURE_TOOLS_XRUN_MONITOR_CC_IMPL_H

#include <dab/xrun_monitor_cc.h>

namespace gr {
  namespace dab {

    class xrun_monitor_cc_impl : public xrun_monitor_cc
    {
     private:
      // Nothing to declare in this block.
      int d_n;
      int d_produce_per;
      gr_complex *d_buffer;
      int d_write_index;
      int d_read_index;
      int d_length;
      bool d_first;
      bool d_starting;
      bool d_drop_when_full;
      bool d_stop_until_tag;
      bool d_report_fill;

      boost::mutex common_mutex;

     public:
      xrun_monitor_cc_impl(int length);
      ~xrun_monitor_cc_impl();

      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
         gr_vector_int &ninpnut_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);

      void set_drop_when_full(bool val);
      void stop_until_tag();
      void set_report_fill(bool val);

    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_CAPTURE_TOOLS_XRUN_MONITOR_CC_IMPL_H */

