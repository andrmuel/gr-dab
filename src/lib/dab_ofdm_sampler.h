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
#ifndef INCLUDED_DAB_OFDM_SAMPLER_H
#define INCLUDED_DAB_OFDM_SAMPLER_H

#include <gr_block.h>

class dab_ofdm_sampler;

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
typedef boost::shared_ptr<dab_ofdm_sampler> dab_ofdm_sampler_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dab_ofdm_sampler.
 *
 * To avoid accidental use of raw pointers, dab_ofdm_sampler's
 * constructor is private.  dab_make_ofdm_sampler is the public
 * interface for creating new instances.
 */
dab_ofdm_sampler_sptr dab_make_ofdm_sampler (unsigned int fft_length, unsigned int cp_length, unsigned int symbols_per_frame);

/*!
 * \brief cuts stream of DAB samples into symbol vectors
 * \ingroup DAB
 *
 * This uses the preferred technique: subclassing gr_block.
 */
class dab_ofdm_sampler : public gr_block
{
	private:
		// The friend declaration allows dab_make_ofdm_sampler to
		// access the private constructor.

		friend dab_ofdm_sampler_sptr dab_make_ofdm_sampler (unsigned int fft_length, unsigned int cp_length, unsigned int symbols_per_frame);

		dab_ofdm_sampler (unsigned int fft_length, unsigned int cp_length, unsigned int symbols_per_frame);  	// private constructor

		enum state_t {STATE_NS, STATE_CP, STATE_SYM};

		state_t d_state;
		unsigned int d_pos;                     // position inside OFDM symbol
		unsigned int d_fft_length;
		unsigned int d_cp_length;
		unsigned int d_symbols_per_frame;       // total number of symbols in a DAB frame
		unsigned int d_sym_nr;                  // number of symbol inside DAB frame

	public:
		void forecast (int noutput_items, gr_vector_int &ninput_items_required);

		int general_work (int noutput_items,
		          gr_vector_int &ninput_items,
		          gr_vector_const_void_star &input_items,
		          gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_OFDM_SAMPLER_H */
