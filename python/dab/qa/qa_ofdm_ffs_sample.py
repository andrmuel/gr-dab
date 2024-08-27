#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_ofdm_ffs_sample(gr_unittest.TestCase):
	"""
	@brief Module test for the OFDM ffs sampler.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_ofdm_ffs_sample(self):
		symbol_length = 3
		num_symbols = 2
		fft_length = 2
		alpha = 0.1
		src_data0       = (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0)
		src_data1       = (0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
		a = (11./2) / fft_length
		b = 0.9*a + (0.1*15./2) / fft_length
		expected_result = (0,0,0,0,0,0,0,a,a,a,a,a,a,a,a,a,a,a,a,b,b)
		src0 = blocks.vector_source_f(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		ofdm_ffs_sample = grdab.ofdm_ffs_sample(symbol_length, fft_length, num_symbols, alpha, 10)
		dst0 = blocks.vector_sink_f()
		self.tb.connect(src0, (ofdm_ffs_sample,0))
		self.tb.connect(src1, (ofdm_ffs_sample,1))
		self.tb.connect(ofdm_ffs_sample, dst0)
		self.tb.run()
		result_data0 = dst0.data()
		# print expected_result
		# print result_data0
		self.assertFloatTuplesAlmostEqual(expected_result, result_data0, 6)

if __name__ == '__main__':
	gr_unittest.main()

