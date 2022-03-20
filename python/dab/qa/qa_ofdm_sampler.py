#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_ofdm_sampler(gr_unittest.TestCase):
	"""
	@brief Module test for the OFDM sampler.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_ofdm_sampler(self):
		fft_len = 3
		src_data0 = (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0)
		src_data1 = (0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
		expected_result0 = (4,5,6,9,0,1,6,7,8)
		expected_result0 = [x+0j for x in expected_result0]
		expected_result1 = (1,0,1)
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		ofdm_sampler = grdab.ofdm_sampler(fft_len,2,2,0)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,fft_len)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, (ofdm_sampler,0))
		self.tb.connect(src1, (ofdm_sampler,1))
		self.tb.connect((ofdm_sampler,0), v2s0, dst0)
		self.tb.connect((ofdm_sampler,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, expected_result1)

	def test_002_ofdm_sampler(self):
		fft_len = 3
		src_data0 = (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0)
		src_data1 = (0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
		expected_result0 = (3,4,5,8,9,0,5,6,7)
		expected_result0 = [x+0j for x in expected_result0]
		expected_result1 = (1,0,1)
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		ofdm_sampler = grdab.ofdm_sampler(fft_len,2,2,1)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,fft_len)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, (ofdm_sampler,0))
		self.tb.connect(src1, (ofdm_sampler,1))
		self.tb.connect((ofdm_sampler,0), v2s0, dst0)
		self.tb.connect((ofdm_sampler,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, expected_result1)

	def test_003_ofdm_sampler(self):
		fft_len = 4
		src_data0 = (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0)
		src_data1 = (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
		expected_result0 = (0,1,2,3,7,8,9,0,4,5,6,7)
		expected_result0 = [x+0j for x in expected_result0]
		expected_result1 = (1,0,0)
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		ofdm_sampler = grdab.ofdm_sampler(fft_len,3,5,3)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,fft_len)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, (ofdm_sampler,0))
		self.tb.connect(src1, (ofdm_sampler,1))
		self.tb.connect((ofdm_sampler,0), v2s0, dst0)
		self.tb.connect((ofdm_sampler,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, expected_result1)

if __name__ == '__main__':
	gr_unittest.main()

