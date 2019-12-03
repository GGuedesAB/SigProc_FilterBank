import os
from scipy.io import wavfile

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

    def save_audio (self, filename):
        wavfile.write(filename, self.sampling_rate, self.data)
    
    def get_data(self):
        return self.data

    def get_sampling_rate(self):
        return self.sampling_rate

if __name__ == "__main__":
    my_audio = Audio()
    my_audio.load_audio('../audio/Blind_intro.wav')
    print(my_audio.get_sampling_rate())
    print(my_audio.get_data()) 

        
