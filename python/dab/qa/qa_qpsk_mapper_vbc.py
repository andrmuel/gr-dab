#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab
import math

class qa_qpsk_mapper_vbc(gr_unittest.TestCase):
	"""
	@brief QA for the QPSK mapper.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_qpsk_mapper_vbc(self):
		src_data        = [10,128]
		expected_result = [1+1j,1+1j,-1+1j,-1+1j,-1+1j,1+1j,1+1j,1+1j]
		expected_result = [x/math.sqrt(2) for x in expected_result]
		src = blocks.vector_source_b(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_char, 1)
		qpsk_mapper_vbc = grdab.qpsk_mapper_vbc(4)
		v2s = blocks.vector_to_stream(gr.sizeof_gr_complex, 4)
		dst = blocks.vector_sink_c()
		self.tb.connect(src, s2v, qpsk_mapper_vbc, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)

if __name__ == '__main__':
	gr_unittest.main()

