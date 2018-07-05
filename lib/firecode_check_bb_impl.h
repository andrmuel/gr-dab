/* -*- c++ -*- */
/* 
 * Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
 * The class firecode_checker is adapted from the Qt-DAB software, Copyright Jan van Katwijk (Lazy Chair Computing J.vanKatwijk@gmail.com)
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

#ifndef INCLUDED_DAB_FIRECODE_CHECK_BB_IMPL_H
#define INCLUDED_DAB_FIRECODE_CHECK_BB_IMPL_H

#include <dab/firecode_check_bb.h>
#include "firecode-checker.h"

namespace gr {
  namespace dab {
/*! \brief checks firecode of logical frames
 *
 * checks firecode of each logical frame as a qa test for the msc_decoder.
 * According to ETSI TS 102 563 every fifth logical frame starts with 16 bit firecode
 *
 *
 */
    class firecode_check_bb_impl : public firecode_check_bb {
    private:
      int d_frame_size;
      int d_bit_rate_n;
      int d_nproduced, d_nconsumed;
      bool d_firecode_passed;
      firecode_checker fc;

    public:
      firecode_check_bb_impl(int bit_rate_n);

      ~firecode_check_bb_impl();

      virtual bool get_firecode_passed()
      { return d_firecode_passed; }

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_FIRECODE_CHECK_BB_IMPL_H */
