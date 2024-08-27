#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_ofdm_move_and_insert_zero(gr_unittest.TestCase):
	"""
	@brief QA for the block that moves the signal to the middle of the band and inserts the zero carrier in the middle.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_ofdm_move_and_insert_zero(self):
		num_carriers = 4
		fft_length   = 10
		d_zeros_on_left = 3
		src_data0        = range(0,8)
		expected_result0 = [0,0,0]+[0,1]+[0]+[2,3]+[0,0]+[0,0,0]+[4,5]+[0]+[6,7]+[0,0]
		expected_result0 = [complex(x) for x in expected_result0]
		src0 = blocks.vector_source_c(src_data0)
		s2v0 = blocks.stream_to_vector(gr.sizeof_gr_complex, num_carriers)
		ofdm_move_and_insert_zero = grdab.ofdm_move_and_insert_zero(fft_length,num_carriers)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex, fft_length)
		dst0 = blocks.vector_sink_c()
		self.tb.connect(src0, s2v0, ofdm_move_and_insert_zero, v2s0, dst0)
		self.tb.run()
		result_data0 = dst0.data()
		# print expected_result0
		# print result_data0
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)

if __name__ == '__main__':
	gr_unittest.main()

