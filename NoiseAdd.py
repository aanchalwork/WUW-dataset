import librosa
import os
import numpy as np
import math


os.chdir("noise/")
cw = os.getcwd()
li = os.listdir(cw)
os.chdir("../")
os.chdir("noisy_audio/")
noise_path = os.getcwd()
os.chdir("../")
os.chdir("audio/")
aud_path = os.getcwd()
li2 = os.listdir(aud_path)
SNR = -20

for k in li:
    noise, sr = librosa.load(os.path.join(cw,k))
    for aud in li2:
        os.mkdir(os.path.join(noise_path,aud))
        os.chdir(aud+"/")
        all_cw = os.getcwd()
        all = os.listdir(all_cw)
        for audio in all:
            signal,sr2 = librosa.load(os.path.join(all_cw,audio))
            RMS_signal=math.sqrt(np.mean(signal**2))
            RMS_noise_exp = RMS_signal/pow(10,SNR/20)
            RMS_noise = math.sqrt(np.mean(noise**2))
            a = RMS_noise_exp/RMS_noise
            print(librosa.get_duration(noise))
            print(librosa.get_duration(signal))
            if sr == sr2:
                signal_noise = signal + (a*noise)
                librosa.output.write_wav(os.path.join(noise_path,aud,audio),signal_noise,sr)
        os.chdir("../")




