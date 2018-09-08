#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
from gnuradio import qtgui
import grdab
import osmosdr
import sip
import sys
import time
import grdab.channel_mapping



class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2000000
        self.ppm = ppm = 0
        self.gain_rf = gain_rf = 50
        self.gain_if = gain_if = 20
        self.gain_bb = gain_bb = 20
        self.current_frequency = current_frequency = 220.352e6
        self.variable_qtgui_push_button_0 = variable_qtgui_push_button_0 = 0

        ##################################################
        # Blocks
        ##################################################
        self._ppm_range = Range(-1000, 1000, 1, 0, 200)
        self._ppm_win = RangeWidget(self._ppm_range, self.set_ppm, "ppm", "counter_slider", float)
        self.top_grid_layout.addWidget(self._ppm_win, 0,0,1,1)
        self._gain_rf_range = Range(0, 100, 1, 50, 200)
        self._gain_rf_win = RangeWidget(self._gain_rf_range, self.set_gain_rf, 'Gain RF', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_rf_win, 1,0,1,1)
        self._gain_if_range = Range(0, 100, 1, 20, 200)
        self._gain_if_win = RangeWidget(self._gain_if_range, self.set_gain_if, 'Gain IF', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_if_win, 2,0,1,1)
        self._gain_bb_range = Range(0, 100, 1, 20, 200)
        self._gain_bb_win = RangeWidget(self._gain_bb_range, self.set_gain_bb, 'Gain BB', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_bb_win, 3,0,1,1)

        nchannels = len(grdab.channel_mapping.table)
        default_channel = 26
        self._ch_select_range = Range(0, nchannels-1, 1, default_channel, 200)
        self._ch_select_win = RangeWidget(self._ch_select_range, self.set_channel, 'Channel', "counter_slider", float)
        self.top_grid_layout.addWidget(self._ch_select_win, 4,0,1,1)

        _variable_qtgui_push_button_0_push_button = Qt.QPushButton("Save adjustments to configuration file")
        self._variable_qtgui_push_button_0_choices = {'Pressed': 1, 'Released': 0}
        _variable_qtgui_push_button_0_push_button.pressed.connect(lambda: self.set_variable_qtgui_push_button_0(self._variable_qtgui_push_button_0_choices['Pressed']))
        _variable_qtgui_push_button_0_push_button.released.connect(lambda: self.set_variable_qtgui_push_button_0(self._variable_qtgui_push_button_0_choices['Released']))
        self.top_grid_layout.addWidget(_variable_qtgui_push_button_0_push_button, 6,0,1,1)


        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,1,5,1)
        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_1.set_update_time(0.10)
        self.qtgui_const_sink_x_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        self.qtgui_const_sink_x_1.enable_axis_labels(True)
        
        if not True:
          self.qtgui_const_sink_x_1.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_1_win, 5,1,5,1)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(current_frequency, 0)
        self.osmosdr_source_0.set_freq_corr(ppm, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain_rf, 0)
        self.osmosdr_source_0.set_if_gain(gain_if, 0)
        self.osmosdr_source_0.set_bb_gain(gain_bb, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(2000000, 0)
          
        self.digital_mpsk_snr_est_cc_0 = digital.mpsk_snr_est_cc(0, 10000, 0.001)
        self.dab_ofdm_demod_0 = grdab.ofdm_demod(
                  grdab.parameters.dab_parameters(
                    mode=1,
                    sample_rate=samp_rate,
                    verbose=False
                  ),
                  grdab.parameters.receiver_parameters(
                    mode=1,
                    softbits=True,
                    input_fft_filter=True,
                    autocorrect_sample_rate=False,
                    sample_rate_correction_factor=1,
                    verbose=False,
                    correct_ffe=True,
                    equalize_magnitude=True
                  )
                )
          
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_to_stream_0, 0), (self.digital_mpsk_snr_est_cc_0, 0))    
        self.connect((self.dab_ofdm_demod_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.digital_mpsk_snr_est_cc_0, 0), (self.qtgui_const_sink_x_1, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.dab_ofdm_demod_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.osmosdr_source_0.set_freq_corr(self.ppm, 0)

    def get_gain_rf(self):
        return self.gain_rf

    def set_gain_rf(self, gain_rf):
        self.gain_rf = gain_rf
        self.osmosdr_source_0.set_gain(self.gain_rf, 0)

    def get_gain_if(self):
        return self.gain_if

    def set_gain_if(self, gain_if):
        self.gain_if = gain_if
        self.osmosdr_source_0.set_if_gain(self.gain_if, 0)

    def set_channel(self, val):
        channel = grdab.channel_mapping.table[int(val)]
        print(channel['frequency'])
        self.current_frequency = float(channel['frequency'])*1e6
        self.osmosdr_source_0.set_center_freq(self.current_frequency, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.current_frequency, self.samp_rate)

    def get_gain_bb(self):
        return self.gain_bb

    def set_gain_bb(self, gain_bb):
        self.gain_bb = gain_bb
        self.osmosdr_source_0.set_bb_gain(self.gain_bb, 0)

    def get_variable_qtgui_push_button_0(self):
        return self.variable_qtgui_push_button_0

    def set_variable_qtgui_push_button_0(self, variable_qtgui_push_button_0):
        self.variable_qtgui_push_button_0 = variable_qtgui_push_button_0
        if variable_qtgui_push_button_0 == 1:
          import grdab.app.config
          import os
          cfg_dir = "".join([os.getenv("HOME"),"/.grdab"])
          cfg = grdab.app.config.Configuration(cfg_dir)
          cfg.adjust_config = {"gain" : {"gain_rf" : self.get_gain_rf(), "gain_if" : self.get_gain_if(), "gain_bb" : self.get_gain_bb()}, "ppm" : self.get_ppm()}
          cfg.save()



def main(top_block_cls=top_block, options=None, frequency=220.352e6, rf_gain=25, if_gain=0, bb_gain=0, ppm=80):

    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"


    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb._gain_rf_win.d_widget.slider.setValue(rf_gain)
    tb._gain_rf_win.d_widget.counter.setValue(rf_gain)

    tb._gain_if_win.d_widget.slider.setValue(if_gain)
    tb._gain_if_win.d_widget.counter.setValue(if_gain)

    tb._gain_bb_win.d_widget.slider.setValue(bb_gain)
    tb._gain_bb_win.d_widget.counter.setValue(bb_gain)

    tb._ppm_win.d_widget.slider.setValue(ppm)
    tb._ppm_win.d_widget.counter.setValue(ppm)

    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


