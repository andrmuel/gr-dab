#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_measure_processing_rate(gr_unittest.TestCase):
	"""
	@brief QA for measure processing rate sink.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_measure_processing_rate(self):
		src = blocks.null_source(gr.sizeof_gr_complex)
		throttle = blocks.throttle(gr.sizeof_gr_complex, 1000000)
		head = blocks.head(gr.sizeof_gr_complex, 200000)
		sink = grdab.measure_processing_rate(gr.sizeof_gr_complex,100000)
		
		self.tb.connect(src, throttle, head, sink)
		self.tb.run()

		rate = sink.processing_rate()
		assert(rate > 900000 and rate < 1100000)
	
	def test_002_measure_processing_rate(self):
		src = blocks.null_source(gr.sizeof_char)
		throttle = blocks.throttle(gr.sizeof_char, 10000000)
		head = blocks.head(gr.sizeof_char, 1000000)
		sink = grdab.measure_processing_rate(gr.sizeof_char,1000000)
		
		self.tb.connect(src, throttle, head, sink)
		self.tb.run()

		rate = sink.processing_rate()
		assert(rate > 8000000 and rate < 12000000)

if __name__ == '__main__':
	gr_unittest.main()

