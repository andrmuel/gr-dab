/* -*- c++ -*- */
/*
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "mp4_decode_bs_impl.h"
#include <stdexcept>
#include <stdio.h>
#include <sstream>
#include <boost/format.hpp>
#include "neaacdec.h"

using namespace boost;

namespace gr {
  namespace dab {

    mp4_decode_bs::sptr
    mp4_decode_bs::make(int bit_rate_n)
    {
      return gnuradio::get_initial_sptr
              (new mp4_decode_bs_impl(bit_rate_n));
    }

    /*
     * The private constructor
     */
    mp4_decode_bs_impl::mp4_decode_bs_impl(int bit_rate_n)
            : gr::block("mp4_decode_bs",
                        gr::io_signature::make(1, 1, sizeof(unsigned char)),
                        gr::io_signature::make(2, 2, sizeof(int16_t))),
              d_bit_rate_n(bit_rate_n)
    {
      d_superframe_size = bit_rate_n * 110;
      d_aacInitialized = false;
      baudRate = 48000;
      set_output_multiple(960 * 6); //TODO: right? baudRate*0.12 for output of one superframe
      aacHandle = NeAACDecOpen();
      //memset(d_aac_frame, 0, 960);
      d_sample_rate = -1;
      d_first = true;
    }

    /*
     * Our virtual destructor.
     */
    mp4_decode_bs_impl::~mp4_decode_bs_impl()
    {
    }

    void
    mp4_decode_bs_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items; //TODO: how to calculate actual rate?
    }

    // returns aac channel configuration
    int mp4_decode_bs_impl::get_aac_channel_configuration(int16_t m_mpeg_surround_config, uint8_t aacChannelMode)
    {
      switch (m_mpeg_surround_config) {
        case 0:     // no surround
          return aacChannelMode ? 2 : 1;
        case 1:     // 5.1
          return 6;
        case 2:     // 7.1
          return 7;
        default:
          return -1;
      }
    }

    bool mp4_decode_bs_impl::initialize(uint8_t dacRate,
                                        uint8_t sbrFlag,
                                        int16_t mpegSurround,
                                        uint8_t aacChannelMode)
    {
      long unsigned int sample_rate;
      uint8_t channels;
      /* AudioSpecificConfig structure (the only way to select 960 transform here!)
      *
      *  00010 = AudioObjectType 2 (AAC LC)
      *  xxxx  = (core) sample rate index
      *  xxxx  = (core) channel config
      *  100   = GASpecificConfig with 960 transform
      *
      * SBR: implicit signaling sufficient - libfaad2
      * automatically assumes SBR on sample rates <= 24 kHz
      * => explicit signaling works, too, but is not necessary here
      *
      * PS:  implicit signaling sufficient - libfaad2
      * therefore always uses stereo output (if PS support was enabled)
      * => explicit signaling not possible, as libfaad2 does not
      * support AudioObjectType 29 (PS)
      */

      int core_sr_index =
              dacRate ? (sbrFlag ? 6 : 3) :
              (sbrFlag ? 8 : 5);   // 24/48/16/32 kHz
      int core_ch_config = get_aac_channel_configuration(mpegSurround,
                                                         aacChannelMode);
      if (core_ch_config == -1) {
        d_logger->error("Unrecognized mpeg surround config (ignored)");
        return false;
      }
      uint8_t asc[2];
      asc[0] = 0b00010 << 3 | core_sr_index >> 1;
      asc[1] = (core_sr_index & 0x01) << 7 | core_ch_config << 3 | 0b100;
      long int init_result = NeAACDecInit2(aacHandle,
                                           asc,
                                           sizeof(asc),
                                           &sample_rate,
                                           &channels);
      if (init_result != 0) {
/*      If some error initializing occured, skip the file */
        d_logger->error("Error initializing decoding library");
        NeAACDecClose(aacHandle);
        return false;
      }
      return true;
    }

    void mp4_decode_bs_impl::handle_aac_frame(const uint8_t *v,
                                              int16_t frame_length,
                                              uint8_t dacRate,
                                              uint8_t sbrFlag,
                                              uint8_t mpegSurround,
                                              uint8_t aacChannelMode,
                                              int16_t *out_sample1,
                                              int16_t *out_sample2)
    {
      // copy AU to process it
      uint8_t au[2 * 960 + 10]; // sure, large enough
      memcpy(au, v, frame_length);
      memset(&au[frame_length], 0, 10);

      if (((au[0] >> 5) & 07) == 4) {
        int16_t count = au[1];
        uint8_t buffer[count];
        memcpy(buffer, &au[2], count);
        uint8_t L0 = buffer[count - 1];
        uint8_t L1 = buffer[count - 2];
        // TODO: handle PADs
      }

      int tmp = MP42PCM(dacRate,
                        sbrFlag,
                        mpegSurround,
                        aacChannelMode,
                        au,
                        frame_length,
                        out_sample1,
                        out_sample2);
    }

    int16_t mp4_decode_bs_impl::MP42PCM(uint8_t dacRate,
                                        uint8_t sbrFlag,
                                        int16_t mpegSurround,
                                        uint8_t aacChannelMode,
                                        uint8_t buffer[],
                                        int16_t bufferLength,
                                        int16_t *out_sample1,
                                        int16_t *out_sample2)
    {
      int16_t samples;
      long unsigned int sample_rate;
      int16_t *outBuffer;
      NeAACDecFrameInfo hInfo;
      uint8_t dummy[10000];
      uint8_t channels;

      // initialize AAC decoder at the beginning
      if (!d_aacInitialized) {
        if (!initialize(dacRate, sbrFlag, mpegSurround, aacChannelMode))
          return 0;
        d_aacInitialized = true;
        //d_logger->debug("AAC initialized");
      }

      outBuffer = (int16_t *) NeAACDecDecode(aacHandle, &hInfo, buffer, bufferLength);
      sample_rate = hInfo.samplerate;

      samples = hInfo.samples;
      if ((sample_rate == 24000) ||
          (sample_rate == 32000) ||
          (sample_rate == 48000) ||
          (sample_rate != (long unsigned) baudRate)) {
        baudRate = sample_rate;
      }
      d_sample_rate = sample_rate;
      //d_logger->debug(format("bytes consumed %d") % (int) (hInfo.bytesconsumed));
      //GR_LOG_DEBUG(d_logger,
      //             format("sample_rate = %d, samples = %d, channels = %d, error = %d, sbr = %d") % sample_rate %
      //             samples %
      //             (int) (hInfo.channels) % (int) (hInfo.error) % (int) (hInfo.sbr));
      channels = hInfo.channels;
      if (hInfo.error != 0) {
        fprintf(stderr, "Warning: %s\n",
                faacDecGetErrorMessage(hInfo.error));
        return 0;
      }

      // write samples to output buffer
      if (channels == 2) {
        // the 2 channels are transmitted intereleaved; each channel gets samples/2 PCM samples
        for (int n = 0; n < samples / 2; n++) {
          out_sample1[n + d_nsamples_produced] = (int16_t) outBuffer[n * 2];
          out_sample2[n + d_nsamples_produced] = (int16_t) outBuffer[n * 2 + 1];
        }
      } else if (channels == 1) {
        int16_t *buffer = (int16_t *) alloca(2 * samples);
        int16_t i;
        for (int n = 0; n < samples / 2; n++) {
          // only 1 channel -> reproduce each sample to send it to a stereo output anyway
          out_sample1[n + d_nsamples_produced] = (int16_t) outBuffer[n * 2];
          out_sample2[n + d_nsamples_produced] = (int16_t) outBuffer[n * 2 + 1];
        }
      } else
        d_logger->error("Cannot handle these channels -> dump samples");

      //d_logger->debug(format("Produced %d PCM samples (for each channel)") % (samples / 2));
      d_nsamples_produced += samples / 2;
      return samples / 2;
    }

/*! \brief CRC16 check
 * CRC16 check according to ETSI EN 300 401
 * @param msg data to check
 * @param len length of dataword without the 2 bytes crc at the end
 * @return true if CRC passed
 */
    bool mp4_decode_bs_impl::crc16(const uint8_t *msg, int16_t len)
    {
      int i, j;
      uint16_t accumulator = 0xFFFF;
      uint16_t crc;
      uint16_t genpoly = 0x1021;

      for (i = 0; i < len; i++) {
        int16_t data = msg[i] << 8;
        for (j = 8; j > 0; j--) {
          if ((data ^ accumulator) & 0x8000)
            accumulator = ((accumulator << 1) ^ genpoly) & 0xFFFF;
          else
            accumulator = (accumulator << 1) & 0xFFFF;
          data = (data << 1) & 0xFFFF;
        }
      }
      // compare calculated CRC with CRC in the AU
      crc = ~((msg[len] << 8) | msg[len + 1]) & 0xFFFF;
      return (crc ^ accumulator) == 0;
    }

    uint16_t mp4_decode_bs_impl::BinToDec(const uint8_t *data, size_t offset, size_t length)
    {
      uint32_t output = (*(data + offset / 8) << 16) | ((*(data + offset / 8 + 1)) << 8) |
                        (*(data + offset / 8 + 2));      // should be big/little endian save
      output >>= 24 - length - offset % 8;
      output &= (0xFFFF >> (16 - length));
      return static_cast<uint16_t>(output);
    }

    int
    mp4_decode_bs_impl::general_work(int noutput_items,
                                     gr_vector_int &ninput_items,
                                     gr_vector_const_void_star &input_items,
                                     gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0] + d_superframe_size;
      int16_t *out1 = (int16_t *) output_items[0];
      int16_t *out2 = (int16_t *) output_items[1];
      d_nsamples_produced = 0;

      if (d_first) {
        add_item_tag(0, nitems_written(0), pmt::mp("audio_start"), pmt::PMT_NIL);
        d_first = false;
      }
      int frames = 0;

      for (int n = 0; n < 1; n++) {
        // process superframe header
        // bits 0 .. 15 is firecode
        // bit 16 is unused
        d_dac_rate = (in[n * d_superframe_size + 2] >> 6) & 01; // bit 17
        d_sbr_flag = (in[n * d_superframe_size + 2] >> 5) & 01; // bit 18
        d_aac_channel_mode = (in[n * d_superframe_size + 2] >> 4) & 01; // bit 19
        d_ps_flag = (in[n * d_superframe_size + 2] >> 3) & 01; // bit 20
        d_mpeg_surround = (in[n * d_superframe_size + 2] & 07); // bits 21 .. 23
        // log header information
        //GR_LOG_DEBUG(d_logger,
        //             format("superframe header: dac_rate %d, sbr_flag %d, aac_mode %d, ps_flag %d, surround %d") %
        //             (int) d_dac_rate % (int) d_sbr_flag % (int) d_aac_channel_mode % (int) d_ps_flag %
        //             (int) d_mpeg_surround);

        switch (2 * d_dac_rate + d_sbr_flag) {
          default:    // cannot happen
          case 0:
            d_num_aus = 4;
            d_au_start[0] = 8;
            d_au_start[1] = in[n * d_superframe_size + 3] * 16 + (in[n * d_superframe_size + 4] >> 4);
            d_au_start[2] = (in[n * d_superframe_size + 4] & 0xf) * 256 + in[n * d_superframe_size + 5];
            d_au_start[3] = in[n * d_superframe_size + 6] * 16 + (in[n * d_superframe_size + 7] >> 4);
            d_au_start[4] = d_superframe_size;
            break;

          case 1:
            d_num_aus = 2;
            d_au_start[n * d_superframe_size + 0] = 5;
            d_au_start[1] = in[n * d_superframe_size + 3] * 16 + (in[n * d_superframe_size + 4] >> 4);
            d_au_start[2] = d_superframe_size;
            break;

          case 2:
            d_num_aus = 6;
            d_au_start[0] = 11;
            d_au_start[1] = in[n * d_superframe_size + 3] * 16 + (in[n * d_superframe_size + 4] >> 4);
            d_au_start[2] = (in[n * d_superframe_size + 4] & 0xf) * 256 + in[n * d_superframe_size + 5];
            d_au_start[3] = in[n * d_superframe_size + 6] * 16 + (in[n * d_superframe_size + 7] >> 4);
            d_au_start[4] = (in[n * d_superframe_size + 7] & 0xf) * 256 + in[8];
            d_au_start[5] = in[n * d_superframe_size + 9] * 16 + (in[n * d_superframe_size + 10] >> 4);
            d_au_start[6] = d_superframe_size;
            break;

          case 3:
            d_num_aus = 3;
            d_au_start[0] = 6;
            d_au_start[1] = in[n * d_superframe_size + 3] * 16 + (in[n * d_superframe_size + 4] >> 4);
            d_au_start[2] = (in[n * d_superframe_size + 4] & 0xf) * 256 + in[n * d_superframe_size + 5];
            d_au_start[3] = d_superframe_size;
            break;
        }

        // each of the d_num_aus AUs of each superframe (110 * d_bit_rate_n packed bytes) is now processed separately

        for (int i = 0; i < d_num_aus; i++) {
          int16_t aac_frame_length;

          // sanity check for the address
          if (d_au_start[i + 1] < d_au_start[i]) {
            throw std::runtime_error("AU start address invalid");
            // should not happen, the header is firecode checked
          }
          aac_frame_length = d_au_start[i + 1] - d_au_start[i] - 2;

          // sanity check for the aac_frame_length // FIXME: Causes crash after running for a long time. Ignore and continue instead of throwing exception
          if ((aac_frame_length >= 960) || (aac_frame_length < 0)) {
            throw std::out_of_range((boost::format("aac frame length not in range (%d)") % aac_frame_length).str());
          }

          // CRC check of each AU (the 2 byte (16 bit) CRC word is excluded in aac_frame_length)
          if (crc16(&in[n * d_superframe_size + d_au_start[i]], aac_frame_length)) {
            //d_logger->debug(format("CRC check of AU %d successful") % i);
            // handle proper AU
            handle_aac_frame(&in[n * d_superframe_size + d_au_start[i]],
                             aac_frame_length,
                             d_dac_rate,
                             d_sbr_flag,
                             d_mpeg_surround,
                             d_aac_channel_mode,
                             out1,
                             out2);
          } else {
            // dump corrupted AU
            d_logger->debug("CRC failure with dab+ frame");
          }
        }
        frames ++;
      }

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(frames * d_superframe_size);

      // Tell runtime system how many output items we produced.
      return d_nsamples_produced;
    }

  } /* namespace dab */
} /* namespace gr */
