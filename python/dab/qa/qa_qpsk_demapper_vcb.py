#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks
import gnuradio.dab as grdab

class qa_qpsk_demapper_vcb(gr_unittest.TestCase):
	"""
	@brief QA for the QPSK demapper.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_qpsk_demapper_vcb(self):
		src_data        = [1+2j,3+1j,-1+1j,-1+1j,-0.0001+1000j,1+1j,1+1j,1+1j]
		expected_result = (10,128)
		src = blocks.vector_source_c(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, 4)
		qpsk_demapper_vcb = grdab.qpsk_demapper_vcb(4)
		v2s = blocks.vector_to_stream(gr.sizeof_char, 1)
		dst = blocks.vector_sink_b()
		self.tb.connect(src, s2v, qpsk_demapper_vcb, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertEqual(expected_result, result_data)

if __name__ == '__main__':
	gr_unittest.main()

