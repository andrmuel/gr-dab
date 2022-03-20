/* -*- c++ -*- */
/* 
 * Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
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

#ifndef INCLUDED_DAB_UNPUNCTURE_FF_IMPL_H
#define INCLUDED_DAB_UNPUNCTURE_FF_IMPL_H

#include <dab/unpuncture_ff.h>

namespace gr {
  namespace dab {
/*! \brief unpuncturing of a stream sequence
 *
 * unpuncturing of a stream sequence according to the puncturing_vector (writing a stream element at a '1' and writing the fillval at a '0')
 *
 * @param puncturing_vector vector with puncturing sequence, length of puncturing_vector is length of a stream sequence
 * @param fillval value to fill in for a zero of the puncturing vector
 *
 */
    class unpuncture_ff_impl : public unpuncture_ff {
    private:
      unsigned int ones(const std::vector<unsigned char> &puncturing_vector);

      std::vector<unsigned char> d_puncturing_vector;
      float d_fillval;
      unsigned int d_vlen_in;
      unsigned int d_vlen_out;

    public:
      unpuncture_ff_impl(const std::vector<unsigned char> &puncturing_vector, float fillval);

      ~unpuncture_ff_impl();

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_UNPUNCTURE_FF_IMPL_H */

