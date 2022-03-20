#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_ofdm_insert_pilot_vcc(gr_unittest.TestCase):
	"""
	@brief Module test for the class that inserts the pilot symbol.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_ofdm_insert_pilot_vcc(self):
		pilot = [1j,2]
		src_data0        = (0,1,2,3,4,5,6,7,8,9,0,1,2,3)
		src_data1        = (1,0,0,1,0,1,0)
		expected_result0 = (1j,2,0,1,2,3,4,5,1j,2,6,7,8,9,1j,2,0,1,2,3)
		expected_result0 = [x+0j for x in expected_result0]
		expected_result1 = (1,0,0,0,1,0,0,1,0,0)
		src0 = blocks.vector_source_c(src_data0)
		src1 = blocks.vector_source_b(src_data1)
		s2v0 = blocks.stream_to_vector(gr.sizeof_gr_complex,2)
		ofdm_insert_pilot = grdab.ofdm_insert_pilot_vcc(pilot)
		v2s0 = blocks.vector_to_stream(gr.sizeof_gr_complex,2)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, s2v0, (ofdm_insert_pilot,0))
		self.tb.connect(src1, (ofdm_insert_pilot,1))
		self.tb.connect((ofdm_insert_pilot,0), v2s0, dst0)
		self.tb.connect((ofdm_insert_pilot,1), dst1)
		self.tb.run()
		result_data0 = dst0.data()
		result_data1 = dst1.data()
		self.assertComplexTuplesAlmostEqual(expected_result0, result_data0, 6)
		self.assertEqual(result_data1, expected_result1)

if __name__ == '__main__':
	gr_unittest.main()

