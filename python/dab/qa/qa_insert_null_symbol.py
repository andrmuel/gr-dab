#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_insert_null_symbol(gr_unittest.TestCase):
	"""
	@brief QA for Null symbol insertion.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_insert_null_symbol(self):
		src_data0       = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
		src_data1       = [0,1,0,1,0]
		expected_result = [1,2,3,0,0,0,0,0,4,5,6,7,8,9,0,0,0,0,0,10,11,12,13,14,15]
		expected_result = [complex(x) for x in expected_result]
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, 3)
		insert_null_symbol = grdab.insert_null_symbol(5,3)
		dst = blocks.vector_sink_c()
		self.tb.connect(src0, s2v, insert_null_symbol, dst)
		self.tb.connect(src1, (insert_null_symbol,1))
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)

if __name__ == '__main__':
	gr_unittest.main()

