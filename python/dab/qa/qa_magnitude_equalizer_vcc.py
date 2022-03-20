#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from math import pi
import gnuradio.dab as grdab

class qa_magnitude_equalizer_vcc(gr_unittest.TestCase):
	"""
	@brief QA for the magnitude equalizer.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_magnitude_equalizer_vcc(self):
		src_data        = (7j,1j,2j,1j,2j,3j,3j,3j,3j,4j,5j,6j,4j+8,2j,4j)
		expected_result = (7j,1j,2j,1j,1j,1j,3j,3j/2.,1j,4j,5j/2.,2j,0.4472135955j+0.894427191,1j,1j)
		trigger         = (0,1,0,0,1)
		src0 = blocks.vector_source_c(src_data)
		src1 = blocks.vector_source_b(trigger)
		s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, 3)
		equ = grdab.magnitude_equalizer_vcc(3, 1)
		v2s = blocks.vector_to_stream(gr.sizeof_gr_complex, 3)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, s2v, equ, v2s, dst0)
		self.tb.connect(src1, (equ,1), dst1)
		self.tb.run()
		result_data = dst0.data()
		result_trigger = dst1.data()
		# print expected_result
		# print result_data
		# print result_trigger
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 5)
		self.assertEqual(trigger, result_trigger)

	def test_002_magnitude_equalizer_vcc(self):
		src_data        = (7j,7j,1j,2j,2j,4j,3j,6j,1j,1j) + (0j,0j,0j,0j)
		trigger         = (0,1,0,0,0) + (0,0)
		# scale: 1/2, 1/4
		expected_result = (0j,0j,0j,0j) + (7j,7j,1j/2,1j/2,1j,1j,3j/2,3j/2,1j/2,1j/4)
		expected_trigger = (0,0) + (0,1,0,0,0)
		src0 = blocks.vector_source_c(src_data)
		src1 = blocks.vector_source_b(trigger)
		s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, 2)
		equ = grdab.magnitude_equalizer_vcc(2, 3)
		v2s = blocks.vector_to_stream(gr.sizeof_gr_complex, 2)
		dst0 = blocks.vector_sink_c()
		dst1 = blocks.vector_sink_b()
		self.tb.connect(src0, s2v, equ, v2s, dst0)
		self.tb.connect(src1, (equ,1), dst1)
		self.tb.run()
		result_data = dst0.data()
		result_trigger = dst1.data()
		# print expected_result
		# print result_data
		# print result_trigger
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 5)
		self.assertEqual(expected_trigger, result_trigger)

if __name__ == '__main__':
	gr_unittest.main()

