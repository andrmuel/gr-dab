#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_repartition_vectors(gr_unittest.TestCase):
	"""
	@brief QA for the vector repartitioning block

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_repartition_vectors(self):
		ilen = 3
		mult = 2
		div  = 3
		olen = 2
		src_data        = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6)
		trig            = (0,    1,    0,    0,       0,       0,    0,    0,    1,     1,    0)
		expected_data   = (3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,1,2,3,4,5,6)
		expected_trig   = (1,  0,  0,  0,    0,    0,    0,  0,  0,  1,  0,  0)
		src = blocks.vector_source_b(src_data)
		trigsrc = blocks.vector_source_b(trig)
		s2v = blocks.stream_to_vector(gr.sizeof_char, ilen)
		repartition_vectors = grdab.repartition_vectors(gr.sizeof_char,ilen,olen,mult,div)
		v2s = blocks.vector_to_stream(gr.sizeof_char, olen)
		dst = blocks.vector_sink_b()
		trigdst = blocks.vector_sink_b()
		self.tb.connect(src, s2v, repartition_vectors, v2s, dst)
		self.tb.connect(trigsrc, (repartition_vectors,1), trigdst)
		self.tb.run()
		result_data = dst.data()
		result_trig = trigdst.data()
		self.assertEqual(expected_data, result_data)
		self.assertEqual(expected_trig, result_trig)
	
	def test_002_repartition_vectors(self):
		ilen = 3
		mult = 2
		div  = 3
		olen = 2
		src_data        = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6)
		trig            = (0,    1,    0,    0,       0,       0,    0,    0,    1,     1,    0)
		expected_data   = (3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,1,2,3,4,5,6)
		expected_trig   = (1,  0,  0,  0,    0,    0,    0,  0,  0,  1,  0,  0)
		src = blocks.vector_source_f(src_data)
		trigsrc = blocks.vector_source_b(trig)
		s2v = blocks.stream_to_vector(gr.sizeof_float, ilen)
		repartition_vectors = grdab.repartition_vectors(gr.sizeof_float,ilen,olen,mult,div)
		v2s = blocks.vector_to_stream(gr.sizeof_float, olen)
		dst = blocks.vector_sink_f()
		trigdst = blocks.vector_sink_b()
		self.tb.connect(src, s2v, repartition_vectors, v2s, dst)
		self.tb.connect(trigsrc, (repartition_vectors,1), trigdst)
		self.tb.run()
		result_data = dst.data()
		result_trig = trigdst.data()
		self.assertFloatTuplesAlmostEqual(expected_data, result_data)
		self.assertEqual(expected_trig, result_trig)

if __name__ == '__main__':
	gr_unittest.main()

