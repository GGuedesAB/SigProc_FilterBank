from scipy import signal
import math
import numpy as np
from matplotlib import pyplot as plt
from Audio import Audio

class Filter ():
    # Interface to be defined
    def __init__ (self, low_f, high_f, gain, audio=None):
        self.audio = audio
        self.order = None
        self.wn = None
        self.b_num = None
        self.a_den = None
        self.b_num_dig = None
        self.a_den_dig = None
        self.low_f = low_f
        self.high_f = high_f
        self.high_f_Hz = high_f
        self.low_f_Hz = low_f
        self.gain = gain #linear
        self.filter_type = 'bandpass'
        self.pass_atten = 0.5 #dB
        self.stop_atten = 40 #dB
        self.f_stop = None
        self.width = None
        self.fs = None
        self.sampling_period = None
        self.number_of_samples = None
        self.create_analog_filters()
        self.create_digital_filter()

    def create_analog_filters (self):
        self.high_f = 2*math.pi*self.high_f
        self.low_f = 2*math.pi*self.low_f
        if self.audio is None:
            self.fs = 44100
            self.number_of_samples = 364917
        else:
            self.fs = self.audio.get_sampling_rate()
            self.number_of_samples = self.audio.get_number_of_samples()
        self.sampling_period = 1/self.fs
        width = self.high_f - self.low_f
        f_pass = width/2
        if width > 2*math.pi*1000:
            f_stop = f_pass + width/2
        else:
            f_stop = f_pass + 2000
        self.f_stop = self.high_f_Hz
        self.width = width/(2*math.pi)
        self.fn = [self.low_f, self.high_f]
        tangent = np.tan([wd/(2*self.fs) for wd in self.fn])
        wrapped_corner_freq = [2*self.fs*f for f in tangent]
        self.order, self.fc = signal.cheb1ord(f_pass, f_stop, self.pass_atten, self.stop_atten, fs=self.fs)
        self.Pb_num, self.Pa_den = signal.cheby1(self.order, self.pass_atten, wrapped_corner_freq, btype=self.filter_type, analog=True)
        self.b_num, self.a_den = signal.cheby1(self.order, self.pass_atten, self.fn, btype=self.filter_type, analog=True)
        self.Pb_num = [i*self.gain for i in self.Pb_num]

    def create_digital_filter (self):
        self.b_num_dig, self.a_den_dig = signal.bilinear(self.Pb_num, self.Pa_den, self.fs)
        return (self.b_num_dig, self.a_den_dig)

    def plot_filters (self, bode=False):
        if bode:
            wd, hd = signal.freqz(self.b_num_dig, self.a_den_dig, worN=self.number_of_samples, fs=self.fs)
            wa, ha = signal.freqs(self.b_num, self.a_den, worN=self.number_of_samples)
            Pwa, Pha = signal.freqs(self.Pb_num, self.Pa_den, worN=self.number_of_samples)
            wa = [w/(2*math.pi) for w in wa]
            Pwa = [w/(2*math.pi) for w in Pwa]
            plt.figure(figsize=(5760/300, 3240/300), dpi=300)
            plt.subplot(231)
            plt.semilogx (wa, 20*np.log10(np.abs(ha)), 'b')
            plt.ylabel('Mag [dB]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0.1,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(234)
            plt.semilogx (wa, np.angle(ha), 'b')
            plt.ylabel('Angle [rad]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0.1,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(232)
            plt.semilogx (wd, 20*np.log10(np.abs(hd)), 'r')
            plt.ylabel('Mag [dB]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0.1,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(235)
            plt.semilogx (wd, np.angle(hd), 'r')
            plt.ylabel('Angle [rad]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0.1,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(233)
            plt.semilogx (Pwa, 20*np.log10(np.abs(Pha)), 'g')
            plt.ylabel('Mag [dB]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0.1,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(236)
            plt.semilogx (wa, np.angle(Pha), 'g')
            plt.ylabel('Angle [rad]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0.1,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.legend()
            plt.savefig(str(self.low_f_Hz) + '-' + str(self.high_f_Hz) + 'bode.png')
            plt.close()
            
        else:
            wd, hd = signal.freqz(self.b_num_dig, self.a_den_dig, worN=self.number_of_samples, fs=self.fs)
            wa, ha = signal.freqs(self.b_num, self.a_den, worN=self.number_of_samples)
            Pwa, Pha = signal.freqs(self.Pb_num, self.Pa_den, worN=self.number_of_samples)
            wa = [w/(2*math.pi) for w in wa]
            Pwa = [w/(2*math.pi) for w in Pwa]
            plt.figure(figsize=(5760/300, 3240/300), dpi=300)
            plt.subplot(231)
            plt.plot (wa, np.abs(ha), 'b')
            plt.ylabel('Gain')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(234)
            plt.plot(wa, np.angle(ha), 'b')
            plt.ylabel('Angle [rad]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(232)
            plt.plot (wd, np.abs(hd), 'r')
            plt.ylabel('Gain')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(235)
            plt.plot (wd, np.angle(hd), 'r')
            plt.ylabel('Angle [rad]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(233)
            plt.plot (Pwa, np.abs(Pha), 'g')
            plt.ylabel('Gain')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.subplot(236)
            plt.plot (Pwa, np.angle(Pha), 'g')
            plt.ylabel('Angle [rad]')
            plt.xlabel('Frequency [Hz]')
            plt.xlim(0,self.f_stop + self.width)
            plt.grid(which='both', axis='both')
            plt.savefig(str(self.low_f_Hz) + '-' + str(self.high_f_Hz) + 'lin.png')
            plt.close()

    def plot_zp (self):
        zd,pd,kd = signal.tf2zpk(self.b_num_dig, self.a_den_dig)
        za,pa,ka = signal.tf2zpk(self.b_num, self.a_den)
        Pza, Ppa, Pka = signal.tf2zpk(self.Pb_num, self.Pa_den)
        plt.figure(figsize=(5760/300, 3240/300), dpi=300)
        plt.subplot(131)
        plt.xlabel('Imaginary')
        plt.ylabel('Real')
        plt.grid(True)
        plt.xlim(-1.2,1.2)
        plt.ylim(-1,1)
        plt.plot(np.real(zd), np.imag(zd), 'or')
        plt.plot(np.real(pd), np.imag(pd), 'xr')
        x = np.linspace(-2,2,400)
        y = np.linspace(-2,2,400)
        x,y = np.meshgrid(x,y)
        z = x*x+y*y
        plt.contour(x,y,z,[1])
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
        plt.savefig(str(self.low_f_Hz) + '-' + str(self.high_f_Hz) + 'zp.png')
        plt.close()        

    def print_transfer_func (self):
        i = 0
        last_num = len(self.b_num)
        with open (str(self.low_f_Hz) + '-' + str(self.high_f_Hz) + 'transfer_func.txt', 'w+') as file:
            file.write ('Num: ')
            for num in self.b_num:
                if i == last_num-1:
                    file.write (str(num) + 's^' + str(i) + '\n')
                else:    
                    file.write (str(num) + 's^' + str(i) + ' + ')
                    i+=1

            last_den = len(self.a_den)
            file.write ('Den: ')
            i = 0
            for den in self.a_den:
                if i == last_den-1:
                    file.write (str(den) + 's^' + str(i) + '\n')
                else:
                    file.write (str(den) + 's^' + str(i) + ' + ')
                    i+=1
        
    def plot_imp_resp (self):
        td, yd = signal.dimpulse((self.b_num_dig, self.a_den_dig, self.sampling_period), n=self.number_of_samples)
        plt.figure(figsize=(1920/300, 1080/300), dpi=300)
        plt.xlim(0,0.5/pow(self.high_f_Hz,0.5))
        plt.step(td, np.squeeze(yd), 'r')
        plt.grid(True)
        plt.savefig(str(self.low_f_Hz) + '-' + str(self.high_f_Hz) + 'imp_resp.png')
        plt.close()
        

    def apply_filter (self, audio):
        if self.a_den_dig is None or self.b_num_dig is None:
            print ('ERROR: Please create your filter before applying to audio signal.')
            exit (1)
        self.result= signal.lfilter(self.b_num_dig, self.a_den_dig, audio.get_data())
        return self.result

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

    def apply_and_sum (self, audio):
        sampling_rate = audio.get_sampling_rate()
        data = audio.get_data()
        my_new_audio = [0]*audio.get_number_of_samples()
        list_of_filtered_audio = []
        for fltr in self.list_of_filters:
            filtered_audio = fltr.apply_filter(audio)
            list_of_filtered_audio.append(filtered_audio)
        for each_audio in list_of_filtered_audio:
            my_new_audio += each_audio
        return my_new_audio

    def dump_all_plots (self):
        for fltr in self.list_of_filters:
            fltr.plot_filters()
            fltr.plot_filters(True)
            fltr.plot_zp()
            fltr.print_transfer_func()
            fltr.plot_imp_resp()
