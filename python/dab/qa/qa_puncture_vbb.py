#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab
import cmath

class qa_puncture_vbb(gr_unittest.TestCase):
	"""
	@brief QA for the puncturing block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_puncture_vbb(self):
		src_data = (0,77,78,78,1,80,2,3,4,5,81,82,83,6,84,7,8,9)
		punc_seq = (1,0,0,0,1,0,1,1,1)
		exp_res  = (0,1,2,3,4,5,6,7,8,9)
		src = blocks.vector_source_b(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_char, 9)
		puncture_vbb = grdab.puncture_vbb(punc_seq)
		v2s = blocks.vector_to_stream(gr.sizeof_char, 5)
		dst = blocks.vector_sink_b()
		self.tb.connect(src, s2v, puncture_vbb, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertEqual(exp_res, result_data)
	

if __name__ == '__main__':
	gr_unittest.main()

