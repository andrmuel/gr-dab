#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_moving_sum(gr_unittest.TestCase):
	"""
	@brief Module test for the moving sum class.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_moving_sum_ff(self):
		src_data = (0,1,3,3,-3.5,-7.7,2,2,3)
		expected_result = (0,1,4,7,2.5,-8.2,-9.2,-3.7,7)
		src = blocks.vector_source_f(src_data)
		moving_sum = grdab.moving_sum_ff(3)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, moving_sum)
		self.tb.connect(moving_sum, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)

	def test_002_moving_sum_ff(self):
		src_data = [float(i**3)*(7**-2) for i in range(-20,20)]
		expected_result = [src_data[0]]+[src_data[i]+src_data[i-1] for i in range(1,40)]
		src = blocks.vector_source_f(src_data)
		moving_sum = grdab.moving_sum_ff(2)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, moving_sum)
		self.tb.connect(moving_sum, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 4)

	def test_001_moving_sum_cc(self):
		src_data = (0j,1+0j,1j,-1+0j,0j,0j,0j,1+0j,1j,2+0j)
		expected_result = (0j,1+0j,1+1j,1j,1j,1j,-1+1j,0j,1+1j,3+1j)
		src = blocks.vector_source_c(src_data)
		moving_sum = grdab.moving_sum_cc(5)
		dst = blocks.vector_sink_c()
		self.tb.connect(src, moving_sum)
		self.tb.connect(moving_sum, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)

	def test_002_moving_sum_cc(self):
		src_data = [float(i**3)*(7**-2)+0.5j*i for i in range(-20,20)]
		expected_result = [src_data[0]]+[src_data[i]+src_data[i-1] for i in range(1,40)]
		src = blocks.vector_source_c(src_data)
		moving_sum = grdab.moving_sum_cc(2)
		dst = blocks.vector_sink_c()
		self.tb.connect(src, moving_sum)
		self.tb.connect(moving_sum, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 4)

if __name__ == '__main__':
	gr_unittest.main()

