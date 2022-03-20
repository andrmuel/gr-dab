#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_prune_vectors(gr_unittest.TestCase):
	"""
	@brief QA for the vector pruning block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_prune_vectors(self):
		src_data        = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] 
		expected_result = [3,4,8,9,13,14]
		src = blocks.vector_source_f(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_float, 5)
		prune_vectors = grdab.prune_vectors(gr.sizeof_float,5,2,1)
		v2s = blocks.vector_to_stream(gr.sizeof_float, 2)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, prune_vectors, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)

	def test_002_prune_vectors(self):
		src_data        = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] 
		expected_result = [3,4,8,9,13,14]
		src = blocks.vector_source_b(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_char, 5)
		prune_vectors = grdab.prune_vectors(gr.sizeof_char,5,2,1)
		v2s = blocks.vector_to_stream(gr.sizeof_char, 2)
		dst = blocks.vector_sink_b()
		self.tb.connect(src, s2v, prune_vectors, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)

if __name__ == '__main__':
	gr_unittest.main()

