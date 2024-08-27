#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_ofdm_remove_first_symbol_vcc(gr_unittest.TestCase):
	"""
	@brief Module test for the class that removes the pilot symbol.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_ofdm_remove_first_symbol_vcc(self):
		src_data0        = (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9)
		src_data1        = (0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0)
		expected_result0 = (0,1,  3,4,5,6,  8,9,0,1,2,3,  5,6,  8,9)
		expected_result0 = [x+0j for x in expected_result0]
		expected_result1 = (0,0,  1,0,0,0,  1,0,0,0,0,0,  1,0,  1,0)
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		ofdm_remove_first_symbol = grdab.ofdm_remove_first_symbol_vcc(1)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,1)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, (ofdm_remove_first_symbol,0))
		self.tb.connect(src1, (ofdm_remove_first_symbol,1))
		self.tb.connect((ofdm_remove_first_symbol,0), v2s0, dst0)
		self.tb.connect((ofdm_remove_first_symbol,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, expected_result1)

	def test_002_ofdm_remove_first_symbol_vcc(self):
		src_data0        = (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7)
		src_data1        = (1,0,0,1,0,0)
		expected_result0 = (3,4,5,6,7,8,2,3,4,5,6,7)
		expected_result0 = [x+0j for x in expected_result0]
		expected_result1 = (1,0,1,0)
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		s2v0 = blocks.stream_to_vector(gr.sizeof_gr_complex,3)
		ofdm_remove_first_symbol = grdab.ofdm_remove_first_symbol_vcc(3)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,3)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, s2v0, (ofdm_remove_first_symbol,0))
		self.tb.connect(src1, (ofdm_remove_first_symbol,1))
		self.tb.connect((ofdm_remove_first_symbol,0), v2s0, dst0)
		self.tb.connect((ofdm_remove_first_symbol,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		# print src_data0
		# print expected_result0
		# print result_data0
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, expected_result1)

if __name__ == '__main__':
	gr_unittest.main()

