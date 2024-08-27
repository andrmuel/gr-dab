#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_measure_ber_b(gr_unittest.TestCase):
	"""
	@brief QA for bit error rate measure sink.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_measure_ber_b(self):
		src0 = blocks.vector_source_b(range(0,256))
		src1 = blocks.vector_source_b(range(0,256))
		sink = grdab.measure_ber_b()
		self.tb.connect(src0, (sink,0))
		self.tb.connect(src1, (sink,1))
		self.tb.run()
		assert(sink.ber()==0)
	
	def test_001_measure_ber_b(self):
		src0 = blocks.vector_source_b([0]*100)
		src1 = blocks.vector_source_b([255]*100)
		sink = grdab.measure_ber_b()
		self.tb.connect(src0, (sink,0))
		self.tb.connect(src1, (sink,1))
		self.tb.run()
		assert(sink.ber()==1)

	def test_002_measure_ber_b(self):
		src0 = blocks.vector_source_b(range(0,256)*2)
		src1 = blocks.vector_source_b([0]*256+[255]*256)
		sink = grdab.measure_ber_b()
		self.tb.connect(src0, (sink,0))
		self.tb.connect(src1, (sink,1))
		self.tb.run()
		self.assertAlmostEqual(sink.ber(), 0.5) # every bit is set 50% of the time

	def test_003_measure_ber_b(self):
		src0 = blocks.vector_source_b([0,7,255,250])
		src1 = blocks.vector_source_b([0,2,255,3])
		sink = grdab.measure_ber_b()
		self.tb.connect(src0, (sink,0))
		self.tb.connect(src1, (sink,1))
		self.tb.run()
		self.assertAlmostEqual(sink.ber(), 8./32.) # every bit is set 50% of the time

if __name__ == '__main__':
	gr_unittest.main()

