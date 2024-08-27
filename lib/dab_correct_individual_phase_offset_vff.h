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
#ifndef INCLUDED_DAB_CORRECT_INDIVIDUAL_PHASE_OFFSET_VFF_H
#define INCLUDED_DAB_CORRECT_INDIVIDUAL_PHASE_OFFSET_VFF_H

#include <gr_sync_block.h>

class dab_correct_individual_phase_offset_vff;

/*
 * We use std::shared_ptr's instead of raw pointers for all access
 * to gr_blocks (and many other data structures).  The shared_ptr gets
 * us transparent reference counting, which greatly simplifies storage
 * management issues.  This is especially helpful in our hybrid
 * C++ / Python system.
 *
 * See http://www.boost.org/libs/smart_ptr/smart_ptr.htm
 *
 * As a convention, the _sptr suffix indicates a std::shared_ptr
 */
typedef std::shared_ptr<dab_correct_individual_phase_offset_vff> dab_correct_individual_phase_offset_vff_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of dab_correct_individual_phase_offset_vff.
 *
 * To avoid accidental use of raw pointers, dab_correct_individual_phase_offset_vff's
 * constructor is private.  dab_make_correct_individual_phase_offset_vff is the public
 * interface for creating new instances.
 */
dab_correct_individual_phase_offset_vff_sptr 
dab_make_correct_individual_phase_offset_vff (unsigned int vlen, float alpha);

/*!
 * \brief Corrects the individual phase offset of each subcarrier by doing an estimation of the error.
 * \ingroup DAB
 * 
 * \param vlen length of the vector
 * \param alpha adaptation speed fatcor: corr = (1-alpha)*corr + alpha*new_val)
 *
 * input: float vector stream with phase vectors of symbols
 * output: float vector stream with corrected phases
 *
 * Note: This block only makes sense as long as the offset of the majority of
 * the samples is smaller than pi/4
 */
class dab_correct_individual_phase_offset_vff : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_correct_individual_phase_offset_vff to
    // access the private constructor.

    friend dab_correct_individual_phase_offset_vff_sptr
    dab_make_correct_individual_phase_offset_vff (unsigned int vlen, float alpha);

    dab_correct_individual_phase_offset_vff (unsigned int vlen, float alpha);    // private constructor

    unsigned int d_vlen;
    float d_alpha;
    float * d_offset_estimation;
    unsigned int d_debug;

  public:
    ~dab_correct_individual_phase_offset_vff (void);
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_CORRECT_INDIVIDUAL_PHASE_OFFSET_VFF_H */
