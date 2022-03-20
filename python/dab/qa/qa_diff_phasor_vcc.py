#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import gnuradio.dab as grdab

class qa_diff_phasor_vcc(gr_unittest.TestCase):
	"""
	@brief QA for the phase differentiation block.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_diff_phasor_vcc(self):
		a = [1+2j,2+3.5j,3.5+4j,4+5j,5+6j]
		b = [1j,1j,1j,1j,1j]
		c = [-1j+3,1j,-7+0j,2.5j+0.333,3.2j]
		d = [(0.35979271051026462+0.89414454782483865j),
		     (0.19421665709046287+0.024219594550527801j),
		     (0.12445564785882557+0.40766238899138718j),
		     (0.041869638845043688+0.97860437393366329j),
		     (0.068927762235083234+0.16649764877365247j)]
		e = [(0.16207552830286298+0.435385030608331j),
		     (0.47195779613669675+0.37824764113272558j),
		     (0.13911998015446148+0.6585095669811617j),
		     (0.093510743358783954+0.98446560079828938j),
		     (0.86036393297704694+0.72043005342024602j)]
		multconj = lambda x,y: x.conjugate()*y
		src_data        = a+b+c+d+e
		expected_result = [0j,0j,0j,0j,0j]+map(multconj,a,b)+map(multconj,b,c)+map(multconj,c,d)+map(multconj,d,e)
		src = blocks.vector_source_c(src_data)
		s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, 5)
		diff_phasor_vcc = grdab.diff_phasor_vcc(5)
		v2s = blocks.vector_to_stream(gr.sizeof_gr_complex, 5)
		dst = blocks.vector_sink_c()
		self.tb.connect(src, s2v, diff_phasor_vcc, v2s, dst)
		self.tb.run()
		result_data = dst.data()
		# print expected_result
		# print result_data
		self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)

if __name__ == '__main__':
	gr_unittest.main()

