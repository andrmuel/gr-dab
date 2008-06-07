#!/usr/bin/env python

from gnuradio import gr, gr_unittest
import dab_swig

class qa_block_partitioning_vbb(gr_unittest.TestCase):
	"""
	@brief QA for the vector element adder block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_block_partitioning_vbb(self):
		ilen = 3
		mult = 2
		div  = 3
		olen = 2
		src_data        = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6)
		trig            = (0,    1,    0,    0,       0,       0,    0,    0,    1,     1,    0)
		expected_data   = (3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,1,2,3,4,5,6)
		expected_trig   = (1,  0,  0,  0,    0,    0,    0,  0,  0,  1,  0,  0)
		src = gr.vector_source_b(src_data)
		trigsrc = gr.vector_source_b(trig)
		s2v = gr.stream_to_vector(gr.sizeof_char, ilen)
		block_partitioning_vbb = dab_swig.block_partitioning_vbb(ilen,olen,mult,div)
		v2s = gr.vector_to_stream(gr.sizeof_char, olen)
		dst = gr.vector_sink_b()
		trigdst = gr.vector_sink_b()
		self.tb.connect(src, s2v, block_partitioning_vbb, v2s, dst)
		self.tb.connect(trigsrc, (block_partitioning_vbb,1), trigdst)
		self.tb.run()
		result_data = dst.data()
		result_trig = trigdst.data()
		self.assertEqual(expected_data, result_data)
		self.assertEqual(expected_trig, result_trig)
	

if __name__ == '__main__':
	gr_unittest.main()

