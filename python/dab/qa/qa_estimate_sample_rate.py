#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_estimate_sample_rate(gr_unittest.TestCase):
	"""
	@brief Module test for the sample rate estimation block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_estimate_sample_rate_ff(self):
		src_data =                           [0,1,0,1,0,0,0,0,1,0,1,1]
		expected_result = [ 7./3.*x for x in [3,3,3,2,2,2,2,2,5,5,2,1]]
		src = blocks.vector_source_b(src_data)
		estimate_sample_rate = grdab.estimate_sample_rate_bf(7,3)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, estimate_sample_rate)
		self.tb.connect(estimate_sample_rate, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 5)


if __name__ == '__main__':
	gr_unittest.main()

