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
        self.fs = None
        self.number_of_samples = None
        self.create_analog_filters()
        self.create_digital_filter()

    def create_analog_filters (self):
        self.high_f = 2*math.pi*self.high_f
        self.low_f = 2*math.pi*self.low_f
        if self.audio is None:
            self.fs = 44100
            self.number_of_samples = 364917
        width = self.high_f - self.low_f
        f_pass = width/2
        if width > 2*math.pi*1000:
            f_stop = f_pass + width/2
        else:
            f_stop = f_pass + 2000
        self.fn = [self.low_f, self.high_f]
        tangent = np.tan([wd/(2*self.fs) for wd in self.fn])
        wrapped_corner_freq = [2*self.fs*f for f in tangent]
        self.order, self.fc = signal.cheb1ord(f_pass, f_stop, self.pass_atten, self.stop_atten, fs=self.fs)
        self.Pb_num, self.Pa_den = signal.cheby1(self.order, self.pass_atten, wrapped_corner_freq, btype=self.filter_type, analog=True)
        self.b_num, self.a_den = signal.cheby1(self.order, self.pass_atten, self.fn, btype=self.filter_type, analog=True)
        self.b_num = [i*self.gain for i in self.b_num]

    def create_digital_filter (self):
        self.b_num_dig, self.a_den_dig = signal.bilinear(self.Pb_num, self.Pa_den, self.fs)

    def plot_filters (self, bode=False):
        if bode:
            wd, hd = signal.freqz(self.b_num_dig, self.a_den_dig, worN=self.number_of_samples, fs=self.fs)
            wa, ha = signal.freqs(self.b_num, self.a_den, worN=self.number_of_samples)
            Pwa, Pha = signal.freqs(self.Pb_num, self.Pa_den, worN=self.number_of_samples)
            wa = [w/(2*math.pi) for w in wa]
            Pwa = [w/(2*math.pi) for w in Pwa]
            plt.subplot(231)
            plt.semilogx (wa, 20*np.log10(np.abs(ha)), 'b')
            plt.xlim(10,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(234)
            plt.semilogx (wa, np.angle(ha), 'b')
            plt.xlim(10,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(232)
            plt.semilogx (wd, 20*np.log10(np.abs(hd)), 'r')
            plt.xlim(10,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(235)
            plt.semilogx (wa, np.angle(hd), 'r')
            plt.xlim(10,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(233)
            plt.semilogx (Pwa, 20*np.log10(np.abs(Pha)), 'g')
            plt.xlim(10,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(236)
            plt.semilogx (wa, np.angle(Pha), 'g')
            plt.xlim(10,self.fs)
            plt.grid(which='both', axis='both')
            plt.show()
        else:
            wd, hd = signal.freqz(self.b_num_dig, self.a_den_dig, worN=self.number_of_samples, fs=self.fs)
            wa, ha = signal.freqs(self.b_num, self.a_den, worN=self.number_of_samples)
            Pwa, Pha = signal.freqs(self.Pb_num, self.Pa_den, worN=self.number_of_samples)
            wa = [w/(2*math.pi) for w in wa]
            Pwa = [w/(2*math.pi) for w in Pwa]
            plt.subplot(231)
            plt.plot (wa, np.abs(ha), 'b')
            plt.xlim(0,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(234)
            plt.plot(wa, np.angle(ha), 'b')
            plt.xlim(0,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(232)
            plt.plot (wd, np.abs(hd), 'r')
            plt.xlim(0,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(235)
            plt.plot (wd, np.angle(hd), 'r')
            plt.xlim(0,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(233)
            plt.plot (Pwa, np.abs(Pha), 'g')
            plt.xlim(0,self.fs)
            plt.grid(which='both', axis='both')
            plt.subplot(236)
            plt.plot (Pwa, np.angle(Pha), 'g')
            plt.xlim(0,self.fs)
            plt.grid(which='both', axis='both')
            plt.show()

    def plot_zp (self):
        zd,pd,kd = signal.tf2zpk(self.b_num_dig, self.a_den_dig)
        za,pa,ka = signal.tf2zpk(self.b_num, self.a_den)
        Pza, Ppa, Pka = signal.tf2zpk(self.Pb_num, self.Pa_den)
        plt.subplot(131)
        plt.xlabel('Imaginary')
        plt.ylabel('Real')
        plt.grid(True)
        plt.plot(np.real(zd), np.imag(zd), 'or')
        plt.plot(np.real(pd), np.imag(pd), 'xr')
        plt.subplot(132)
        plt.xlabel('Imaginary')
        plt.ylabel('Real')
        plt.grid(True)
        plt.plot(np.real(za), np.imag(za), 'ob')
        plt.plot(np.real(pa), np.imag(pa), 'xb')
        plt.subplot(133)
        plt.xlabel('Imaginary')
        plt.ylabel('Real')
        plt.grid(True)
        plt.plot(np.real(Pza), np.imag(Pza), 'og')
        plt.plot(np.real(Ppa), np.imag(Ppa), 'xg')
        plt.show()

    #def print_transfer_func (self):

    #def plot_imp_resp (self):

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
    my_filter.plot_zp()