import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy import fftpack

class Audio ():
    def __init__(self, sampling_rate=None, data=None):
        self.sampling_rate = sampling_rate
        self.data = data

    def load_audio (self, wav_path):
        if os.path.exists(wav_path):
            self.__wav_path__ = wav_path
        else:
            raise FileNotFoundError
        self.sampling_rate, self.data = wavfile.read(self.__wav_path__)
        print ('Loaded ' + str(os.path.basename(wav_path)) + ' with ' + str(len(self.data)) + ' data points and sampling rate of ' + str(self.sampling_rate) + 'Hz.')

    def save_audio (self, filename):
        wavfile.write(filename, self.sampling_rate, self.data)
    
    def get_data(self):
        return self.data

    def get_sampling_rate(self):
        return self.sampling_rate

    def calculate_fft(self):
        self.w_axis = fftpack.fftfreq(len(self.data), (1/self.sampling_rate))
        self.fft_of_data = fftpack.fft(self.data)
        return (self.w_axis, self.fft_of_data)

    def print_fft(self):
        self.calculate_fft()
        mag = np.abs(self.fft_of_data)
        plt.bar(self.w_axis, mag)
        print ('Saving mag bars')
        plt.savefig('marg_bars.png')
        print ('Finished saving mag bars.')
        angle = np.angle(self.fft_of_data)
        plt.plot(self.w_axis, angle)
        print ('Saving angle plot.')
        plt.savefig('angle.png')
        print ('Finished saving angle plot.')


if __name__ == "__main__":
    my_audio = Audio()
    my_audio.load_audio('../audio/Blind_intro.wav')
    print(my_audio.get_sampling_rate())
    print(my_audio.get_data())
    my_audio.print_fft()

        
