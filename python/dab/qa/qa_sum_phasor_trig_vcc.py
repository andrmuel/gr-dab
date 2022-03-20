#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_sum_phasor_trig_vcc(gr_unittest.TestCase):
	"""
	@brief QA for the phase summation class.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_sum_phasor_trig_vcc(self):
		src_data0        = (1,1j,1,1j,1j,1j,-1, 1j, 1,1j,1,1j)
		src_data1        = (0,   1,   0,     0,     1,   0)
		expected_result0 = (0,0, 1,1j,1j,-1,-1j,-1j,1,1j,1,-1)
		expected_result0 = [x+0j for x in expected_result0]
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		s2v0 = blocks.stream_to_vector(gr.sizeof_gr_complex,2)
		sum_phasor_trig_vcc = grdab.sum_phasor_trig_vcc(2)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,2)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, s2v0, (sum_phasor_trig_vcc,0))
		self.tb.connect(src1, (sum_phasor_trig_vcc,1))
		self.tb.connect((sum_phasor_trig_vcc,0), v2s0, dst0)
		self.tb.connect((sum_phasor_trig_vcc,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		# print expected_result0
		# print result_data0
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, src_data1)

	def test_002_sum_phasor_trig_vcc(self):
		src_data0        = (1,1j,-1,1,1)*50 # try it multiple times to decect problems when leaving the function in between
		src_data1        = (1,0,0,1,0)*50
		expected_result0 = (1,1j,-1j,1,1)*50
		expected_result0 = [x+0j for x in expected_result0]
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		s2v0 = blocks.stream_to_vector(gr.sizeof_gr_complex,1)
		sum_phasor_trig_vcc = grdab.sum_phasor_trig_vcc(1)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,1)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, s2v0, (sum_phasor_trig_vcc,0))
		self.tb.connect(src1, (sum_phasor_trig_vcc,1))
		self.tb.connect((sum_phasor_trig_vcc,0), v2s0, dst0)
		self.tb.connect((sum_phasor_trig_vcc,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, src_data1)

if __name__ == '__main__':
	gr_unittest.main()

