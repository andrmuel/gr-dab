/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
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
#ifndef INCLUDED_DAB_OFDM_MOVE_AND_INSERT_ZERO_H
#define INCLUDED_DAB_OFDM_MOVE_AND_INSERT_ZERO_H

#include <gr_sync_block.h>

class dab_ofdm_move_and_insert_zero;

/*
 * We use boost::shared_ptr's instead of raw pointers for all access
 * to gr_blocks (and many other data structures).  The shared_ptr gets
 * us transparent reference counting, which greatly simplifies storage
 * management issues.  This is especially helpful in our hybrid
 * C++ / Python system.
 *
 * See http://www.boost.org/libs/smart_ptr/smart_ptr.htm
 *
 * As a convention, the _sptr suffix indicates a boost::shared_ptr
 */
typedef boost::shared_ptr<dab_ofdm_move_and_insert_zero> dab_ofdm_move_and_insert_zero_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dab_ofdm_move_and_insert_zero.
 *
 * To avoid accidental use of raw pointers, dab_ofdm_move_and_insert_zero's
 * constructor is private.  dab_make_ofdm_move_and_insert_zero is the public
 * interface for creating new instances.
 */
dab_ofdm_move_and_insert_zero_sptr 
dab_make_ofdm_move_and_insert_zero (unsigned int fft_length, 
                                        unsigned int num_carriers);

/*!
 * \brief Moves the symbols into the middle of a signal of length fft_length and inserts the zero carrier in the middle.
 * \ingroup DAB
 * 
 * \param fft_length total number of fft bins
 * \param num_carriers number of carriers with OFDM symbols, not including the zero carrier
 *
 * This uses the preferred technique: subclassing gr_sync_block.
 */
class dab_ofdm_move_and_insert_zero : public gr_sync_block
{
	private:
		// The friend declaration allows dab_make_ofdm_move_and_insert_zero to
		// access the private constructor.

		friend dab_ofdm_move_and_insert_zero_sptr
    dab_make_ofdm_move_and_insert_zero (unsigned int fft_length, unsigned int num_carriers);

		dab_ofdm_move_and_insert_zero (unsigned int fft_length, unsigned int num_carriers);  	// private constructor

		unsigned int d_fft_length;
		unsigned int d_num_carriers;
		unsigned int d_zeros_on_left;

	public:
		int work (int noutput_items,
		          gr_vector_const_void_star &input_items,
		          gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_OFDM_MOVE_AND_INSERT_ZERO_H */
