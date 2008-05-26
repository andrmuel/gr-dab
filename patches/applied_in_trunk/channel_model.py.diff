Index: gnuradio-core/src/python/gnuradio/blks2impl/channel_model.py
===================================================================
--- gnuradio-core/src/python/gnuradio/blks2impl/channel_model.py	(revision 8484)
+++ gnuradio-core/src/python/gnuradio/blks2impl/channel_model.py	(working copy)
@@ -23,7 +23,7 @@
 from gnuradio import gr
 
 class channel_model(gr.hier_block2):
-    def __init__(self, noise_voltage=0.0, frequency_offset=0.0, epsilon=1.0, taps=[1.0,0.0]):
+    def __init__(self, noise_voltage=0.0, frequency_offset=0.0, epsilon=1.0, taps=[1.0,0.0], noise_seed=3021):
         ''' Creates a channel model that includes:
           - AWGN noise power in terms of noise voltage
           - A frequency offest in the channel in ratio
@@ -40,7 +40,7 @@
         self.multipath = gr.fir_filter_ccc(1, taps)
         
         self.noise_adder = gr.add_cc()
-        self.noise = gr.noise_source_c(gr.GR_GAUSSIAN,noise_voltage)
+        self.noise = gr.noise_source_c(gr.GR_GAUSSIAN, noise_voltage, noise_seed)
         self.freq_offset = gr.sig_source_c(1, gr.GR_SIN_WAVE, frequency_offset, 1.0, 0.0)
         self.mixer_offset = gr.multiply_cc()
 
@@ -60,3 +60,6 @@
      
     def set_taps(self, taps):
         self.multipath.set_taps(taps)
+
+    def set_timing_offset(self, epsilon):
+        self.timing_offset.set_interp_ratio(epsilon)
