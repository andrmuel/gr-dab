#!/usr/bin/env python

import os
from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_concatenate_signals(gr_unittest.TestCase):
	"""
	@brief QA for signal concatenation block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()
		os.environ['GR_SCHEDULER'] = "STS" # need single threaded scheduler for use with concatenate_signals

	def tearDown(self):
		self.tb = None

	def test_001_concatenate_signals(self):
		src_data0       = [1j,2j,3j,4j,5j]
		src_data1       = [6j,7j,8j]
		src_data2       = [9j,10j,11j,12j,13j,14j]
		expected_result = src_data0 + src_data1 + src_data2
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_c(src_data1)
		src2 = blocks.vector_source_c(src_data2)
		concatenate_signals = grdab.concatenate_signals(gr.sizeof_gr_complex)
		dst = blocks.vector_sink_c()
		self.tb.connect(src0, (concatenate_signals,0))
		self.tb.connect(src1, (concatenate_signals,1))
		self.tb.connect(src2, (concatenate_signals,2))
		self.tb.connect(concatenate_signals, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)

	def test_002_concatenate_signals(self):
		src_data0       = [6j]
		src_data1       = [1j,2j,3j,4j,5j]*3000
		src_data2       = [7j]
		src_data3       = [8j,9j,10j,11j]*3000
		expected_result = src_data0 + src_data1 + src_data2 + src_data3
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_c(src_data1)
		src2 = blocks.vector_source_c(src_data2)
		src3 = blocks.vector_source_c(src_data3)
		concatenate_signals = grdab.concatenate_signals(gr.sizeof_gr_complex)
		dst = blocks.vector_sink_c()
		self.tb.connect(src0, (concatenate_signals,0))
		self.tb.connect(src1, (concatenate_signals,1))
		self.tb.connect(src2, (concatenate_signals,2))
		self.tb.connect(src3, (concatenate_signals,3))
		self.tb.connect(concatenate_signals, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)

	def test_003_concatenate_signals(self):
		src_data0       = [6]
		src_data1       = [1,2,3,4,5]
		src_data2       = [7]
		src_data3       = [8,9,10,11]
		expected_result = src_data0 + src_data1 + src_data2 + src_data3
		src0 = blocks.vector_source_b(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		src2 = blocks.vector_source_b(src_data2)
		src3 = blocks.vector_source_b(src_data3)
		concatenate_signals = grdab.concatenate_signals(gr.sizeof_char)
		dst = blocks.vector_sink_b()
		self.tb.connect(src0, (concatenate_signals,0))
		self.tb.connect(src1, (concatenate_signals,1))
		self.tb.connect(src2, (concatenate_signals,2))
		self.tb.connect(src3, (concatenate_signals,3))
		self.tb.connect(concatenate_signals, dst)
		self.tb.run()
		result_data = list(dst.data())
		self.assertEqual(expected_result, result_data)

if __name__ == '__main__':
	gr_unittest.main()

