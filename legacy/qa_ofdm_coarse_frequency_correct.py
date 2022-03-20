#!/usr/bin/env python

from gnuradio import gr, gr_unittest
import dab_python

class qa_ofdm_coarse_frequency_correct(gr_unittest.TestCase):
	"""
	@brief QA for the coarse frequency correction class.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_ofdm_coarse_frequency_correct(self):
		src_data0        = [0,1,2,3,4,5,6,7,8,9,1,2,0,5,7,6,0,4,0,6,1,1,1,0.8,0.1,1.3,1,0.7,1,1,0,1,2,3,4,5,6,7,8,9]
		expected_result0 = [7,9,5,6,0.8,1.3,3,5]
		expected_result0 = [complex(x) for x in expected_result0]
		src_data1 = [1,1,1,0]
		expected_result1 = (1,1,1,0)
		src0 = gr.vector_source_c(src_data0)
		src1 = gr.vector_source_b(src_data1)
		s2v0 = gr.stream_to_vector(gr.sizeof_gr_complex, 10)
		ofdm_coarse_frequency_correct = dab_python.ofdm_coarse_frequency_correct(10,2)
		v2s0 = gr.vector_to_stream(gr.sizeof_gr_complex, 2)
		dst0 = gr.vector_sink_c()
		dst1 = gr.vector_sink_b()
		self.tb.connect(src0, s2v0, (ofdm_coarse_frequency_correct,0))
		self.tb.connect(src1, (ofdm_coarse_frequency_correct,1))
		self.tb.connect((ofdm_coarse_frequency_correct,0), v2s0, dst0)
		self.tb.connect((ofdm_coarse_frequency_correct,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		# print expected_result0
		# print result_data0
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, expected_result1)

if __name__ == '__main__':
	gr_unittest.main()

