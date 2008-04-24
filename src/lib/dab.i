/* -*- c++ -*- */

%feature("autodoc", "1");		// generate python docstrings

%include "exception.i"
%import "gnuradio.i"			// the common stuff

%{
#include "gnuradio_swig_bug_workaround.h"	// mandatory bug fix
#include "dab_moving_sum_ff.h"
#include <stdexcept>
%}

// ----------------------------------------------------------------

/*
 * First arg is the package prefix.
 * Second arg is the name of the class minus the prefix.
 *
 * This does some behind-the-scenes magic so we can
 * access howto_square_ff from python as howto.square_ff
 */
GR_SWIG_BLOCK_MAGIC(dab,moving_sum_ff);

dab_moving_sum_ff_sptr dab_make_moving_sum_ff (int length);

class dab_moving_sum_ff : public gr_sync_block
{
 private:
  dab_moving_sum_ff (int length);

 public:
  int length() const {return history();}
  void set_length(int length) {set_history(length);}
};
