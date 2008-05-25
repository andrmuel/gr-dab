Index: gnuradio-core/src/python/gnuradio/blks2impl/channel_model.py
===================================================================
--- gnuradio-core/src/python/gnuradio/blks2impl/channel_model.py	(revision 8484)
+++ gnuradio-core/src/python/gnuradio/blks2impl/channel_model.py	(working copy)
@@ -60,3 +60,6 @@
      
     def set_taps(self, taps):
         self.multipath.set_taps(taps)
+
+    def set_timing_offset(self, epsilon):
+        self.timing_offset.set_interp_ratio(epsilon)
