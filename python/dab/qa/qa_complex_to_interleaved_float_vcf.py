#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_complex_to_interleaved_float_vcf(gr_unittest.TestCase):
	"""
	@brief QA for the complex to interleaved float block

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_complex_to_interleaved_float_vcf(self):
		src_data        = (1+2j,3+4j,5+6j,7+8j)
		expected_result = (1,3,2,4,5,7,6,8)
		src = blocks.vector_source_c(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, 2)
		complex_to_interleaved_float_vcf = grdab.complex_to_interleaved_float_vcf(2)
		v2s = blocks.vector_to_stream(gr.sizeof_float, 4)
		dst = blocks.vector_sink_f()
		self.tb.connect(src, s2v, complex_to_interleaved_float_vcf, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print result_data
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)

if __name__ == '__main__':
	gr_unittest.main()

