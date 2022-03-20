#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab
import cmath

class qa_unpuncture_vff(gr_unittest.TestCase):
	"""
	@brief QA for the unpuncturing block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_unpuncture_vff(self):
		src_data = (0,1,2,3,4,5,6,7,8,9)
		punc_seq = (1,0,0,0,1,0,1,1,1)
		exp_res  = (0,77,77,77,1,77,2,3,4,5,77,77,77,6,77,7,8,9)
		src = blocks.vector_source_f(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_float, 5)
		unpuncture_vff = grdab.unpuncture_vff(punc_seq, 77)
		v2s = blocks.vector_to_stream(gr.sizeof_float, 9)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, unpuncture_vff, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertFloatTuplesAlmostEqual(exp_res, result_data)
	
	def test_002_unpuncture_vff(self):
		src_data = (0,1,2,3,4,5,6,7,8,9)
		punc_seq = (1,0,0,0,1,0,1,1,1)
		exp_res  = (0,0,0,0,1,0,2,3,4,5,0,0,0,6,0,7,8,9)
		src = blocks.vector_source_f(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_float, 5)
		unpuncture_vff = grdab.unpuncture_vff(punc_seq)
		v2s = blocks.vector_to_stream(gr.sizeof_float, 9)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, unpuncture_vff, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertFloatTuplesAlmostEqual(exp_res, result_data)

if __name__ == '__main__':
	gr_unittest.main()

