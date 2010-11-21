/* -*- c++ -*- */

%include "gnuradio.i"      // the common stuff

%{
#include "dab_moving_sum_ff.h"
#include "dab_moving_sum_cc.h"
#include "dab_ofdm_sampler.h"
#include "dab_ofdm_coarse_frequency_correct.h"
#include "dab_diff_phasor_vcc.h"
#include "dab_correct_individual_phase_offset_vff.h"
#include "dab_ofdm_remove_first_symbol_vcc.h"
#include "dab_estimate_sample_rate_bf.h"
#include "dab_ofdm_ffs_sample.h"
#include "dab_ofdm_ffe_all_in_one.h"
#include "dab_fractional_interpolator_triggered_update_cc.h"
#include "dab_frequency_interleaver_vcc.h"
#include "dab_qpsk_mapper_vbc.h"
#include "dab_qpsk_demapper_vcb.h"
#include "dab_ofdm_insert_pilot_vcc.h"
#include "dab_sum_phasor_trig_vcc.h"
#include "dab_ofdm_move_and_insert_zero.h"
#include "dab_insert_null_symbol.h"
#include "dab_concatenate_signals.h"
#include "dab_measure_processing_rate.h"
#include "dab_sum_elements_vff.h"
#include "dab_modulo_ff.h"
#include "dab_measure_ber_b.h"
#include "dab_select_vectors.h"
#include "dab_repartition_vectors.h"
#include "dab_puncture_vbb.h"
#include "dab_unpuncture_vff.h"
#include "dab_magnitude_equalizer_vcc.h"
#include "dab_complex_to_interleaved_float_vcf.h"
#include "dab_prune_vectors.h"
#include "dab_fib_sink_vb.h"
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
    int length() const {return d_length;}
    void reset() {d_sum=0;}
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,moving_sum_cc);

dab_moving_sum_cc_sptr dab_make_moving_sum_cc (int length);

class dab_moving_sum_cc : public gr_sync_block
{
  private:
    dab_moving_sum_cc (int length);

  public:
    int length() const {return d_length;}
    void reset() {d_sum=0;}
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,ofdm_sampler);

dab_ofdm_sampler_sptr dab_make_ofdm_sampler (unsigned int fft_length, unsigned int cp_length, unsigned int symbols_per_frame, unsigned int gap);

class dab_ofdm_sampler : public gr_block
{
  private:
    dab_ofdm_sampler (unsigned int fft_length, unsigned int cp_length, unsigned int symbols_per_frame, unsigned int gap);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,ofdm_coarse_frequency_correct);

dab_ofdm_coarse_frequency_correct_sptr dab_make_ofdm_coarse_frequency_correct (unsigned int fft_length, unsigned int num_carriers, unsigned int cp_length);

class dab_ofdm_coarse_frequency_correct : public gr_sync_block
{
  private:
    dab_ofdm_coarse_frequency_correct (unsigned int fft_length, unsigned int num_carriers, unsigned int cp_length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,diff_phasor_vcc);

dab_diff_phasor_vcc_sptr dab_make_diff_phasor_vcc (unsigned int length);

class dab_diff_phasor_vcc : public gr_sync_block
{
  private:
    dab_diff_phasor_vcc (unsigned int length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,correct_individual_phase_offset_vff);

dab_correct_individual_phase_offset_vff_sptr dab_make_correct_individual_phase_offset_vff (unsigned int vlen, float alpha);

class dab_correct_individual_phase_offset_vff : public gr_sync_block
{
  private:
    dab_correct_individual_phase_offset_vff (unsigned int vlen, float alpha);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,ofdm_remove_first_symbol_vcc);

dab_ofdm_remove_first_symbol_vcc_sptr dab_make_ofdm_remove_first_symbol_vcc (unsigned int vlen);

class dab_ofdm_remove_first_symbol_vcc : public gr_block
{
  private:
    dab_ofdm_remove_first_symbol_vcc (unsigned int vlen);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab, estimate_sample_rate_bf);

dab_estimate_sample_rate_bf_sptr dab_make_estimate_sample_rate_bf (float expected_sample_rate, int frame_length);

class dab_estimate_sample_rate_bf : public gr_sync_block
{
  private:
    dab_estimate_sample_rate_bf (float expected_sample_rate, int frame_length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab, ofdm_ffs_sample);

dab_ofdm_ffs_sample_sptr dab_make_ofdm_ffs_sample (unsigned int symbol_length, unsigned int fft_length, unsigned int num_symbols, float alpha, unsigned int sample_rate);

class dab_ofdm_ffs_sample : public gr_sync_block
{
  private:
    dab_ofdm_ffs_sample (unsigned int symbol_length, unsigned int fft_length, unsigned int num_symbols, float alpha, unsigned int sample_rate);
  public:
    float ffe_estimate() { return d_estimated_error_per_sample*d_sample_rate/(2*M_PI); }
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab, ofdm_ffe_all_in_one);

dab_ofdm_ffe_all_in_one_sptr dab_make_ofdm_ffe_all_in_one (unsigned int symbol_length, unsigned int fft_length, unsigned int num_symbols, float alpha, unsigned int sample_rate);

class dab_ofdm_ffe_all_in_one : public gr_sync_block
{
  private:
    dab_ofdm_ffe_all_in_one (unsigned int symbol_length, unsigned int fft_length, unsigned int num_symbols, float alpha, unsigned int sample_rate);
  public:
    float ffe_estimate() { return d_estimated_error_per_sample*d_sample_rate/(2*M_PI); }
};

// ----------------------------------------------------------------
// adapted from GNU Radio codebase:

GR_SWIG_BLOCK_MAGIC(dab, fractional_interpolator_triggered_update_cc);

dab_fractional_interpolator_triggered_update_cc_sptr dab_make_fractional_interpolator_triggered_update_cc (float phase_shift, float interp_ratio);

class dab_fractional_interpolator_triggered_update_cc : public gr_block
{
    private:
     dab_fractional_interpolator_triggered_update_cc (float phase_shift, float interp_ratio);

    public:
     float mu() const;
     float interp_ratio() const;
     void set_mu (float mu);
     void set_interp_ratio (float interp_ratio);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,frequency_interleaver_vcc);

dab_frequency_interleaver_vcc_sptr dab_make_frequency_interleaver_vcc (const std::vector<short> &interleaving_sequence);

class dab_frequency_interleaver_vcc : public gr_sync_block
{
    private:
     dab_frequency_interleaver_vcc (const std::vector<short> &interleaving_sequence);

    public:
     void set_sequence(const std::vector<short> &interleaving_sequence) { d_interleaving_sequence = interleaving_sequence; }
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,qpsk_mapper_vbc);

dab_qpsk_mapper_vbc_sptr dab_make_qpsk_mapper_vbc (int symbol_length);

class dab_qpsk_mapper_vbc : public gr_sync_block
{
    private:
     dab_qpsk_mapper_vbc (int symbol_length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,qpsk_demapper_vcb);

dab_qpsk_demapper_vcb_sptr dab_make_qpsk_demapper_vcb (int symbol_length);

class dab_qpsk_demapper_vcb : public gr_sync_block
{
    private:
     dab_qpsk_demapper_vcb (int symbol_length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,ofdm_insert_pilot_vcc);

dab_ofdm_insert_pilot_vcc_sptr dab_make_ofdm_insert_pilot_vcc (const std::vector<gr_complex> &pilot);

class dab_ofdm_insert_pilot_vcc : public gr_block
{
  private:
    dab_ofdm_insert_pilot_vcc (const std::vector<gr_complex> &pilot);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,sum_phasor_trig_vcc);

dab_sum_phasor_trig_vcc_sptr dab_make_sum_phasor_trig_vcc (unsigned int length);

class dab_sum_phasor_trig_vcc : public gr_sync_block
{
  private:
    dab_sum_phasor_trig_vcc (unsigned int length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,ofdm_move_and_insert_zero);

dab_ofdm_move_and_insert_zero_sptr dab_make_ofdm_move_and_insert_zero (unsigned int fft_length, unsigned int num_carriers);

class dab_ofdm_move_and_insert_zero : public gr_sync_block
{
  private:
    dab_ofdm_move_and_insert_zero (unsigned int fft_length, unsigned int num_carriers);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,insert_null_symbol);

dab_insert_null_symbol_sptr dab_make_insert_null_symbol (int ns_length, int symbol_length);

class dab_insert_null_symbol : public gr_block
{
  private:
    dab_insert_null_symbol (int ns_length, int symbol_length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,concatenate_signals);

dab_concatenate_signals_sptr dab_make_concatenate_signals (size_t itemsize);

class dab_concatenate_signals : public gr_block
{
  private:
    dab_concatenate_signals (size_t itemsize);
  public:
    void reset() { d_current_signal=0; }
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,measure_processing_rate);

dab_measure_processing_rate_sptr dab_make_measure_processing_rate (size_t itemsize, int samples_to_count);

class dab_measure_processing_rate : public gr_sync_block
{
  private:
    dab_measure_processing_rate (size_t itemsize, int samples_to_count);
  public:
    void set_samples_to_count(int samples_to_count) { d_samples_to_count=samples_to_count; }
    float processing_rate() { return d_processing_rate; }
    float bitrate() { return d_itemsize*8*d_processing_rate; }
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,sum_elements_vff);

dab_sum_elements_vff_sptr dab_make_sum_elements_vff (unsigned int length);

class dab_sum_elements_vff : public gr_sync_block
{
  private:
    dab_sum_elements_vff (unsigned int length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,modulo_ff);

dab_modulo_ff_sptr dab_make_modulo_ff (float div);

class dab_modulo_ff : public gr_sync_block
{
  private:
    dab_modulo_ff (float div);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,measure_ber_b);

dab_measure_ber_b_sptr dab_make_measure_ber_b ();

class dab_measure_ber_b : public gr_sync_block
{
  private:
    dab_measure_ber_b ();
  public:
    void clear() { d_errors=0; d_bytes=0; }
    float ber() { return (float)d_errors/(float)d_bytes; }
    unsigned int bytecount() { return d_bytes; }
    unsigned int bitcount() { return 8*d_bytes; }
    unsigned int errorcount() { return d_errors; }
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,select_vectors);

dab_select_vectors_sptr dab_make_select_vectors (size_t itemsize, unsigned int length, unsigned int num_select, unsigned int num_skip);

class dab_select_vectors : public gr_block
{
  private:
    dab_select_vectors (size_t itemsize, unsigned int length, unsigned int num_select, unsigned int num_skip);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,repartition_vectors);

dab_repartition_vectors_sptr dab_make_repartition_vectors (size_t d_itemsize, unsigned int vlen_in, unsigned int vlen_out, unsigned int multiply, unsigned int divide);

class dab_repartition_vectors : public gr_block
{
  private:
    dab_repartition_vectors (size_t d_itemsize, unsigned int vlen_in, unsigned int vlen_out, unsigned int multiply, unsigned int divide);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,puncture_vbb);

dab_puncture_vbb_sptr dab_make_puncture_vbb (const std::vector<unsigned char> &puncturing_vector);

class dab_puncture_vbb : public gr_sync_block
{
  private:
    dab_puncture_vbb (const std::vector<unsigned char> &puncturing_vector);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,unpuncture_vff);

dab_unpuncture_vff_sptr dab_make_unpuncture_vff (const std::vector<unsigned char> &puncturing_vector, float fillval = 0);

class dab_unpuncture_vff : public gr_sync_block
{
  private:
    dab_unpuncture_vff (const std::vector<unsigned char> &puncturing_vector, float fillval);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,magnitude_equalizer_vcc);

dab_magnitude_equalizer_vcc_sptr dab_make_magnitude_equalizer_vcc (unsigned int vlen, unsigned int num_symbols);

class dab_magnitude_equalizer_vcc : public gr_sync_block
{
  private:
    dab_magnitude_equalizer_vcc (unsigned int vlen, unsigned int num_symbols);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,complex_to_interleaved_float_vcf);

dab_complex_to_interleaved_float_vcf_sptr dab_make_complex_to_interleaved_float_vcf (unsigned int length);

class dab_complex_to_interleaved_float_vcf : public gr_sync_block
{
  private:
    dab_complex_to_interleaved_float_vcf (unsigned int length);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,prune_vectors);

dab_prune_vectors_sptr dab_make_prune_vectors (size_t itemsize, unsigned int length, unsigned int prune_start, unsigned int prune_end);

class dab_prune_vectors : public gr_sync_block
{
  private:
    dab_prune_vectors (size_t itemsize, unsigned int length, unsigned int prune_start, unsigned int prune_end);
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(dab,fib_sink_vb);

dab_fib_sink_vb_sptr dab_make_fib_sink_vb ();

class dab_fib_sink_vb : public gr_sync_block
{
  private:
    dab_fib_sink_vb ();
};

