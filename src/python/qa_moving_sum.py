#!/usr/bin/env python

from gnuradio import gr, gr_unittest
import dab

class qa_moving_sum(gr_unittest.TestCase):

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_square_ff(self):
		src_data = (0,1,3,3,-3.5,-7.7,2,2,3)
		expected_result = (0,2,8,14,5,-16.4,-18.4,-7.4,14)
		src = gr.vector_source_f(src_data)
		moving_sum = gr.moving_sum_ff(3,2)
		dst = gr.vector_sink_f()
		self.tb.connect(src, moving_sum)
		self.tb.connect(moving_sum, dst)
		self.tb.run()
		result_data = dst.data()
		self.assertFloatTuplesAlmostEqual(expected_result, result_data, 9)

if __name__ == '__main__':
	gr_unittest.main()

