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

#ifndef INCLUDED_DAB_MEASURE_BER_B_H
#define INCLUDED_DAB_MEASURE_BER_B_H

#include <gr_sync_block.h>

class dab_measure_ber_b;
typedef std::shared_ptr<dab_measure_ber_b> dab_measure_ber_b_sptr;

dab_measure_ber_b_sptr dab_make_measure_ber_b();

/*!
 * \brief Measure bit error rate of a byte stream
 *
 * input: port 0: actual byte stream
 * input: port 1: expected byte stream
 *
 * \ingroup sink
 */
class dab_measure_ber_b : public gr_sync_block
{
  friend dab_measure_ber_b_sptr dab_make_measure_ber_b();

 private:
  unsigned long d_bytes; 
  unsigned long d_errors; 

 protected:
  unsigned int bits_set(char byte);
  dab_measure_ber_b();

 public:
  /*! clear error and byte count */
  void clear() { d_errors=0; d_bytes=0; }
  /*! \return bit error rate */
  float ber() { return (float)d_errors/(float)(d_bytes*8); }
  /*! \return number of received bytes */
  unsigned long bytecount() { return d_bytes; }
  /*! \return number of received bits */
  unsigned long bitcount() { return 8*d_bytes; }
  /*! \return number of received bits with errors */
  unsigned long errorcount() { return d_errors; }

  int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_MEASURE_BER_B_H */
