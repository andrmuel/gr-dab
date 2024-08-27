#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from math import pi
import gnuradio.dab as grdab

class qa_correct_individual_phase_offset_vff(gr_unittest.TestCase):
	"""
	@brief QA for the individual carrier phase equalisation block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_correct_individual_phase_offset_vff(self):
		expected_result = [x*pi/2+pi/4 for x in [1,-2,-1,0,1,-2]]
		src_data        = map(lambda x,y: x+y, expected_result,[0.1,0.3,-0.2,0.2,0.4,0.1])
		src = blocks.vector_source_f(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_float, 3)
		mut = grdab.correct_individual_phase_offset_vff(3, 1)
		v2s = blocks.vector_to_stream(gr.sizeof_float, 3)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, mut, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 5)

	def test_002_correct_individual_phase_offset_vff(self):
		data = [x*pi/2+pi/4 for x in [1,-2,-1,0,1,-2]]
		src_data        = map(lambda x,y: x+y, data, [0.1,0.3,-0.4,0.2,0.4,0.1])
		expected_result = map(lambda x,y: x+y, data, [0.05,0.15,-0.2,0.075,0.125,0.15])
		src = blocks.vector_source_f(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_float, 3)
		mut = grdab.correct_individual_phase_offset_vff(3, 0.5)
		v2s = blocks.vector_to_stream(gr.sizeof_float, 3)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, mut, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print src_data
		# print expected_result
		# print result_data
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 5)

if __name__ == '__main__':
	gr_unittest.main()

