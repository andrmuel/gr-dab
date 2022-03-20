#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab
import cmath
from math import pi

class qa_ofdm_ffs_sample(gr_unittest.TestCase):
	"""
	@brief Module test for the OFDM ffs sampler with phase calculation.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_ofdm_ffe_all_in_one(self):
		symbol_length = 5
		num_symbols = 2
		fft_length = 3
		alpha = 0.1
		src_data0 = [77*cmath.exp(2j*pi*x/20) for x in range(0,20)]
		src_data0[4] = 100 # should not matter, as this area of the symbol is not evaluated
		src_data0[12:19] = [100] * 7 # should not matter, as only the first two symbols are evaluated
		src_data1 =       (0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
		d = -2*pi/20 # phase diff between two consective samples
		expected_result = (0,0,0,0,0,0,0,0,0,0,0,0,d,d,d,d,d,d,d,d)
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		ffe = grdab.ofdm_ffe_all_in_one(symbol_length, fft_length, num_symbols, alpha, 10)
		dst0 = blocks.vector_sink_f()
		self.tb.connect(src0, (ffe,0))
		self.tb.connect(src1, (ffe,1))
		self.tb.connect(ffe, dst0)
		self.tb.run()
		result_data0 = dst0.data()
		# print expected_result
		# print result_data0
		self.assertFloatTuplesAlmostEqual(expected_result, result_data0, 3)

if __name__ == '__main__':
	gr_unittest.main()

