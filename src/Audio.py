import os
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.io import wavfile
from scipy import fftpack

class Audio ():
    def __init__(self, wav_path=None, sampling_rate=None, data=None):
        self.sampling_rate = sampling_rate
        self.data = data
        if wav_path is not None:
            self.load_audio(wav_path)
        else:
            self.number_of_samples = len(data)
            self.create_audio(data, sampling_rate)

    def create_audio (self, data, sampling_rate):
        self.sampling_rate=sampling_rate
        self.data=data

    def load_audio (self, wav_path):
        if os.path.exists(wav_path):
            self.__wav_path__ = wav_path
        else:
            raise FileNotFoundError
        self.sampling_rate, self.data = wavfile.read(self.__wav_path__)
        self.number_of_samples = len(self.data)
        print ('Loaded ' + str(os.path.basename(wav_path)) + ' with ' + str(self.number_of_samples) + ' data points and sampling rate of ' + str(self.sampling_rate) + 'Hz.')

    def normalize_data (self):
        maxim = max(self.data)
        self.data = [d/maxim for d in self.data]
        self.data = np.array(self.data, dtype=np.float32)
    
    def reload_from_new_audio (self, audio):
        self.sampling_rate = audio.get_data
        self.data = audio.get_sampling_rate

    def save_audio (self, filename):
        self.normalize_data()
        wavfile.write(filename, self.sampling_rate, self.data)

    def get_data (self):
        return self.data

    def get_sampling_rate (self):
        return self.sampling_rate

    def get_number_of_samples (self):
        return self.number_of_samples

    def calculate_fft(self):
        self.w_axis = fftpack.fftfreq(self.number_of_samples, (1/self.sampling_rate))
        self.fft_of_data = fftpack.fft(self.data)
        #self.fft_of_data = [i/self.number_of_samples for i in self.fft_of_data]
        return (self.w_axis, self.fft_of_data)

    def print_audio(self, name):
        self.normalize_data()
        print ('Saving audio waveform.')
        sampling_period = 0
        time_list = []
        plt.figure(figsize=(1920/300, 1080/300), dpi=300)
        plt.subplot(111)
        for sample in self.data:
            time_list.append(sampling_period)
            sampling_period += 1/self.sampling_rate
        plt.plot(time_list, self.data)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Intensidade')
        plt.savefig(name+'.png')
        print ('Finished saving audio waveform.')

    def print_fft(self, name):
        self.calculate_fft()
        plt.figure(figsize=(1920/300, 1080/300), dpi=300)
        new_w_axis = fftpack.fftshift(self.w_axis)
        print ('Saving fft plot.')
        plt.subplot(211)
        mag = np.abs(self.fft_of_data)
        plt.plot(self.w_axis, mag)
        plt.subplot(212)
        angles = np.angle(self.fft_of_data)
        i = 0
        new_angles = []
        for angle in angles:
            i = i + (np.abs(angle)*180/math.pi)
            new_angles.append(i)
        plt.plot(new_w_axis, new_angles)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Angle [°]')
        plt.savefig(name+'.png')
        print ('Finished saving fft plot.')

class Gain ():
    def __init__ (self, gain):
        if gain < -40 or gain > 6.02:
            raise AttributeError
        else:
            self.gain = float(pow(10, (gain/20)))
    
    def get_gain(self):
        return self.gain

        
