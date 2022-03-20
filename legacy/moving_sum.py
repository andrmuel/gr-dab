class moving_sum_ff(gr.hier_block2):
	"""
	moving sum block for float samples
	"""
	
	def __init__(self, elements, gain):
		"""
		moving sum filter, implemented with a delay line + an iir filter

		@param elements: length of the window
		@param gain: gain factor
		"""
		gr.hier_block2.__init__(self,"moving_sum",
					gr.io_signature(1, 1, gr.sizeof_float), # input signature
					gr.io_signature(1, 1, gr.sizeof_float)) # output signature

		self.input = gr.add_const_ff(0) # needed, because external inputs can only be wired to one port

		self.delay = gr.delay(gr.sizeof_float, elements)
		self.sub = gr.sub_ff()
		self.iir_filter = gr.iir_filter_ffd([gain],[0,1])
		# FIXME possible trouble with limited precision (error summing up) -> maybe implement some slow decay towards zero
		# such as self.decay = gr.multiply_const_ff(1-1./elements)
		
		self.connect(self, self.input, self.sub, self.iir_filter, self)
		self.connect(self.input, self.delay, (self.sub,1))

class moving_sum_cc(gr.hier_block2):
	"""
	moving sum block for complex samples
	"""
	
	def __init__(self, elements, gain):
		"""
		moving sum filter, implemented with a delay line + an iir filter

		@param elements: length of the window
		@param gain: gain factor
		"""
		gr.hier_block2.__init__(self,"moving_sum",
					gr.io_signature(1, 1, gr.sizeof_gr_complex), # input signature
					gr.io_signature(1, 1, gr.sizeof_gr_complex)) # output signature

		self.input = gr.kludge_copy(gr.sizeof_gr_complex) # needed, because external inputs can only be wired to one port
		
		# calculate moving sum as two separate moving sums of the real and imaginary part
		self.real = gr.complex_to_real()
		self.imag = gr.complex_to_imag()
		self.rsum = dab_python.moving_sum_ff(elements)
		self.isum = dab_python.moving_sum_ff(elements)
		self.f2c  = gr.float_to_complex()
		self.gain = gr.multiply_const_cc(gain)

		self.connect(self, self.input)
		self.connect(self.input, self.real, self.rsum, (self.f2c, 0))
		self.connect(self.input, self.imag, self.isum, (self.f2c, 1))
		self.connect(self.f2c, self.gain, self)
