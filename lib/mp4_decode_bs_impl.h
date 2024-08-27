/* -*- c++ -*- */
/*
 *
 * Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
 *
 * GNU Radio block written for gr-dab including the following third party elements:
 * -QT-DAB: classes mp4Processor and faad-decoder except the reed-solomon class
 *  Copyright (C) 2013
 *  Jan van Katwijk (J.vanKatwijk@gmail.com)
 *  Lazy Chair Computing
 * -KA9Q: the char-sized Reed-Solomon encoder and decoder of the libfec library
 *  (details on the license see /fec/LICENCE)
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

#ifndef INCLUDED_DAB_MP4_DECODE_BS_IMPL_H
#define INCLUDED_DAB_MP4_DECODE_BS_IMPL_H

#include <dab/mp4_decode_bs.h>
#include "neaacdec.h"

namespace gr {
  namespace dab {
/*! \brief DAB+ Audio frame decoder
 * according to ETSI TS 102 563
 */
    class mp4_decode_bs_impl : public mp4_decode_bs {
    private:
      int d_nsamples_produced;
      int d_bit_rate_n;
      int d_sample_rate;
      int d_superframe_size;
      bool d_aacInitialized;
      int32_t baudRate;
      uint8_t d_dac_rate, d_sbr_flag, d_aac_channel_mode, d_ps_flag, d_mpeg_surround, d_num_aus;
      int16_t d_au_start[10];
      bool d_first;

      NeAACDecHandle aacHandle;

      bool crc16(const uint8_t *msg, int16_t len);

      uint16_t BinToDec(const uint8_t *data, size_t offset, size_t length);

      int get_aac_channel_configuration(int16_t m_mpeg_surround_config, uint8_t aacChannelMode);

      bool initialize(uint8_t dacRate,
                      uint8_t sbrFlag,
                      int16_t mpegSurround,
                      uint8_t aacChannelMode);

      void handle_aac_frame(const uint8_t *v,
                            int16_t frame_length,
                            uint8_t dacRate,
                            uint8_t sbrFlag,
                            uint8_t mpegSurround,
                            uint8_t aacChannelMode,
                            int16_t *out_sample1,
                            int16_t *out_sample2);

      int16_t MP42PCM(uint8_t dacRate,
                      uint8_t sbrFlag,
                      int16_t mpegSurround,
                      uint8_t aacChannelMode,
                      uint8_t buffer[],
                      int16_t bufferLength,
                      int16_t *out_sample1,
                      int16_t *out_sample2);

    public:
      mp4_decode_bs_impl(int bit_rate_n);

      ~mp4_decode_bs_impl();

      virtual int get_sample_rate()
      { return d_sample_rate; }

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_MP4_DECODE_BS_IMPL_H */
