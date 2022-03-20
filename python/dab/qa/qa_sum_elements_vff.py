#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_sum_elements_vff(gr_unittest.TestCase):
	"""
	@brief QA for the vector element adder block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_sum_elements_vff(self):
		a = [1,2,3,4,5]
		b = [-1000,1000,0,-1000,1000]
		src_data        = a+b
		expected_result = [sum(a),sum(b)]
		src = blocks.vector_source_f(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_float, 5)
		sum_elements_vff = grdab.sum_elements_vff(5)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, sum_elements_vff, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 8)
	
	def test_002_sum_elements_vff(self):
		a = range(-1000,3096)
		b = range(10000,14096)
		src_data        = a+b
		expected_result = [sum(a),sum(b)]
		src = blocks.vector_source_f(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_float, 4096)
		sum_elements_vff = grdab.sum_elements_vff(4096)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, sum_elements_vff, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 8)

if __name__ == '__main__':
	gr_unittest.main()

