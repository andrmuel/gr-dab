#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_frequency_interleaver_vcc(gr_unittest.TestCase):
	"""
	@brief QA for frequency interleaving.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_frequency_interleaver_vcc(self):
		src_data        = [0,1,2,3,4,5,6,7,8,9+1j]
		expected_result = [2,1,4,0,3,7,6,9+1j,5,8]
		expected_result = [complex(x) for x in expected_result]
		src = blocks.vector_source_c(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, 5)
		frequency_interleaver_vcc = grdab.frequency_interleaver_vcc([3,1,0,4,2])
		v2s = blocks.vector_to_stream(gr.sizeof_gr_complex, 5)
		dst = blocks.vector_sink_c()
		self.tb.connect(src, s2v, frequency_interleaver_vcc, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)

if __name__ == '__main__':
	gr_unittest.main()

