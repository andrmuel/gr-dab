/* -*- c++ -*- */
/* 
 * Reed-Solomon decoder for DAB+
 * Copyright 2002 Phil Karn, KA9Q
 * May be used under the terms of the GNU General Public License (GPL)
 *
 * Rewritten into a GNU Radio block for gr-dab
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

#ifndef INCLUDED_DAB_REED_SOLOMON_DECODE_BB_IMPL_H
#define INCLUDED_DAB_REED_SOLOMON_DECODE_BB_IMPL_H

#include <dab/reed_solomon_decode_bb.h>

extern "C" {
#include "./fec/fec.h"
}

namespace gr {
  namespace dab {
/*! \brief Reed-Solomon decoder configured for DAB+
 *
 * Reed Solomon RS(120, 110, t=5) with virtual interleaving; derived from RS(255, 245, t=5). Details see ETSI TS 102 563 clause 6.0 and 6.1.
 *
 * @param bit_rate_n data rate in multiples of 8kbit/s
 *
 */
    class reed_solomon_decode_bb_impl : public reed_solomon_decode_bb {
    private:
      int d_bit_rate_n;
      int d_superframe_size;
      int d_superframe_size_rs;
      void *rs_handle;
      uint8_t rs_packet[120];
      int corr_pos[10];
      int d_corrected_errors;

      void DecodeSuperframe(uint8_t *sf, size_t sf_len);

    public:
      reed_solomon_decode_bb_impl(int bit_rate_n);

      ~reed_solomon_decode_bb_impl();

      virtual int get_corrected_errors()
      { return d_corrected_errors; }

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_REED_SOLOMON_DECODE_BB_IMPL_H */

