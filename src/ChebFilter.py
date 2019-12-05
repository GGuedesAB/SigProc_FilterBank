from scipy import signal
import math
import numpy as np
from matplotlib import pyplot as plt
import Audio

class Filter ():
    # Interface to be defined
    def __init__ (self, low_f, high_f, gain, audio=None):
        self.audio = audio
        self.order = None
        self.wn = None
        self.b_num = None
        self.a_den = None
        self.low_f = low_f
        self.high_f = high_f
        self.gain = gain #linear
        self.filter_type = 'bandpass'
        self.pass_atten = 0.5 #dB
        self.stop_atten = 40 #dB
        self.create_filter(self.audio.get_sampling_rate())

    def create_filter (self, fs=None):
        if fs is None:
            fs = 44100
        self.fs = fs
        width = self.high_f - self.low_f
        f_pass = width/2
        f_stop = f_pass + pow(width/100,2) + 300
        self.fn = [self.low_f, self.high_f]
        self.order, self.fc = signal.cheb1ord(f_pass, f_stop, self.pass_atten, self.stop_atten, fs=self.fs)
        # b is numerator, a is denominator
        self.b_num, self.a_den = signal.cheby1(self.order, self.pass_atten, self.fn, btype=self.filter_type, fs=self.fs)
        self.b_num = [i*self.gain for i in self.b_num]
    
    def plot_filter_linear (self):
        w, h = signal.freqz(self.b_num, self.a_den, worN=100000, fs=self.fs)
        plt.xlim(0,self.fs/2)
        plt.plot (w, np.abs(h))
        plt.grid(which='both', axis='both')
        plt.show()

    def plot_filter_bode (self):
        w, h = signal.freqz(self.b_num, self.a_den, worN=100000, fs=self.fs)
        h_dB = 20 * np.log10(np.abs(h))
        plt.xlim(0,self.fs/2)
        plt.plot (w, h_dB)
        plt.grid(which='both', axis='both')
        plt.show()

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
        for each_filter in self.list_of_filters:
            each_filter.apply_filter()

        print ('Applyin in cascade.')

if __name__ == "__main__":
    my_filter = Filter(16,60,1)
    my_filter.create_filter()
    my_filter.plot_filter_bode()