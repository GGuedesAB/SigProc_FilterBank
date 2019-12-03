from scipy import signal
import math
import numpy as np
from matplotlib import pyplot as plt
import Audio

class Filter ():
    # Interface to be defined
    def __init__ (self, audio, attenuation, filter_type):
        if type(filter_type) is not str:
            print('ERROR: Filter type must be eihter \'lowpass\', \'highpass\', \'bandpass\' or \'bandstop\'.')
            exit (1)
        self.audio = audio
        self.order = None
        self.wn = None
        self.b_num = None
        self.a_den = None
        self.filter_type = filter_type
        self.attenuation = attenuation

    def calculate_order (self, wp, ws, gpass, gstop, fs=None):
        if fs is None:
            fs = self.audio.get_sampling_rate()
        self.fs = fs
        self.order, self.wn = signal.cheb2ord(wp, ws, gpass, gstop, False, fs)

    def create_filter (self):
        if self.order is None or self.wn is None:
            print ('ERROR: First select your filter order.')
            exit (1)
        # b is numerator, a is denominator
        self.b_num, self.a_den = signal.cheby2(self.order, self.attenuation, self.wn, btype=self.filter_type, fs=self.fs)
    
    def apply_filter (self):
        if self.a_den is None or self.b_num is None:
            print ('ERROR: Please create your filter before applying to audio signal.')
            exit (1)
        self.result = signal.lfilter(self.b_num, self.a_den, self.audio.get_data())

    def get_new_audio (self):
        if self.result is not None:
            new_audio = Audio(self.audio.get_sampling_rate(), self.result)
            return new_audio
        else:
            print ('ERROR: Apply filter in audio before getting it\'s result.')
            exit (1)

class Filter_Bank ():
    # Interface recieves an array of Filters
    def __init__ (self, list_of_filters):
        self.list_of_filters = list_of_filters
        self.parallel_results = []

    def apply_all_in_parallel (self):
        for each_filter in self.list_of_filters:
            each_filter.apply_filter()
            self.parallel_results.append(each_filter.get_new_audio())

    def apply_in_cascade_for_range (self, range):
        # Still need to think how to implement this
        # Maybe a good solution to keep in Filter class, it's frequencies
        # But I already keep wn, think about this later
        print ('Applyin in cascade.')