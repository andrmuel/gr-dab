/* -*- c++ -*- */
/* 
 * Copyright 2018 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_DAB_CONTROL_STREAM_TO_TAG_CC_IMPL_H
#define INCLUDED_DAB_CONTROL_STREAM_TO_TAG_CC_IMPL_H

#include <dab/control_stream_to_tag_cc.h>

namespace gr {
  namespace dab {

    class control_stream_to_tag_cc_impl : public control_stream_to_tag_cc
    {
     private:
      // Nothing to declare in this block.
      pmt::pmt_t d_stream_tag;
      int d_vlen;

     public:
      control_stream_to_tag_cc_impl(const std::string &tag_str, int vlen);
      ~control_stream_to_tag_cc_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_CONTROL_STREAM_TO_TAG_CC_IMPL_H */

