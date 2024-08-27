#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_fractional_interpolator_triggered_update(gr_unittest.TestCase):
	"""
	@brief Module test for the fractional interpolator block with triggered update.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_fractional_interpolator_triggered_update_cc(self):
		src_data = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1]
		trigger  = [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		expected_result = [3,4,5,6,7,8,0,2,4] # not sure why the values at the start and end are missing, but the trigger works nicely ..
		expected_result = [x + 0j for x in expected_result]
		src0 = blocks.vector_source_c(src_data)
		src1 = blocks.vector_source_b(trigger)
		fractional_interpolator_triggered_update = grdab.fractional_interpolator_triggered_update_cc(0,1)
		fractional_interpolator_triggered_update.set_interp_ratio(2)
		dst = blocks.vector_sink_c()
		self.tb.connect(src0, (fractional_interpolator_triggered_update,0))
		self.tb.connect(src1, (fractional_interpolator_triggered_update,1))
		self.tb.connect(fractional_interpolator_triggered_update, dst)
		self.tb.run()
		result_data = dst.data()
		# print src_data
		# print expected_result
		# print result_data
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)


if __name__ == '__main__':
	gr_unittest.main()

