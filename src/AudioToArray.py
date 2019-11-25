import os
import scipy.io as scio

class AudioFileToArray ():
    def __init__(self, wav_path):
        if os.path.exists(wav_path):
            self.__wav_path__ = wav_path
        else:
            raise FileNotFoundError
        self.sampling_rate, self.data = scio.wavfile.read(self.__wav_path__)

    def get_data(self):
        return self.data

    def get_sampling_rate(self):
        return self.sampling_rate

class ArrayToAudioFile ():
    def __init__(self, sampling_rate, data, wav_path):
        print ('Saving file.')

        
