from Audio import Audio
from Audio import Gain
from ChebFilter import Filter
from ChebFilter import Filter_Bank
import os

def find_Blind_intro ():
    for root,dirs,files in os.walk('.'):
        if 'Blind_intro.wav' in files:
            return os.path.join(root, 'Blind_intro.wav')
    print ('Could not find Blind_intro.wav.')
    exit (1)

if __name__ == "__main__":
    print ('Please enter gain for each range (in dB).')
    try:
        sub_low = Gain(float(input ('16Hz - 60Hz gain: ')))
        low = Gain(float(input ('60Hz - 250Hz gain: ')))
        mid_low = Gain(float(input ('250Hz - 2kHz gain: ')))
        mid_high = Gain(float(input ('2kHz - 4kHz gain: ')))
        high = Gain(float(input ('4kHz - 6kHz gain: ')))
        bright = Gain(float(input ('6kHz - 16kHz gain: ')))
    except AttributeError:
        print ('ERROR: Gain must be between 6.02dB and -40dB.')
        exit (1)
    except KeyboardInterrupt:
        print ('\nBye!')
        exit(0)
    blind_intro_path = find_Blind_intro()
    my_audio = Audio(blind_intro_path)
    filter1 = Filter(16,60,sub_low.get_gain(), my_audio)
    filter2 = Filter(60,250,low.get_gain(), my_audio)
    filter3 = Filter(250,2000,mid_low.get_gain(), my_audio)
    filter4 = Filter(2000,4000,mid_high.get_gain(), my_audio)
    filter5 = Filter(4000,6000,high.get_gain(), my_audio)
    filter6 = Filter(6000,16000,bright.get_gain(), my_audio)
    bank_of_filters = Filter_Bank([filter1, filter2, filter3, filter4, filter5, filter6])
    new_audio = bank_of_filters.apply_and_sum(my_audio)
    new_audio = Audio(wav_path=None, sampling_rate=my_audio.get_sampling_rate(), data=new_audio)
    new_audio.save_audio('new_Blind_intro.wav')
    try:
        dump_plots = input('Do you want to see filter and waveform plots?(Y/N) ')
        if dump_plots == 'Y' or dump_plots == 'y':
            my_audio.print_audio('Blind_intro')
            new_audio.print_audio('new_Blind_intro')
            my_audio.print_fft('Blind_intro_fft')
            new_audio.print_fft('new_Blind_intro_fft')
            bank_of_filters.dump_all_plots()
    except KeyboardInterrupt:
        print ('\nBye!')
        exit(0)