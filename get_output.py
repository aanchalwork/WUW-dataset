import os, sys, stat
import shutil
#import pyaudioconvert as pac
import mutagen
from mutagen.wave import WAVE

def change_dir(current, mfa_data_path):
    li = os.listdir(current)
    for k in li:
        if os.path.isdir( current + "/" + k):
            change_dir(current + "/" + k, mfa_data_path)
        elif ".wav" in k:
            if current != mfa_data_path:
                k=k.strip()
                #pac.convert_wav_to_16bit_mono(k, k[:-4]+"_new"+k[-4:])
                shutil.move(os.path.join(current,(k)), mfa_data_path)
        elif ".lab" in k:
            if current != mfa_data_path:
                k=k.strip()
                #os.rename(k,k[:-4]+"_new"+k[-4:])
                shutil.move(os.path.join(current,(k)), mfa_data_path)
    if current != mfa_data_path:
        shutil.rmtree(current)



def analy_aud(Path, Range):
    os.chdir(Path)
    mfa_data_path = Path
    change_dir(Path, mfa_data_path)
    os.chdir(Path)
    all = os.listdir()
    num_wav_files = 0
    num_lab_files = 0
    total_length = 0
    out = []
    for k in range(len(Range)):
        out.append(0)

    for fil in all:
        if ".wav" in fil:
            num_wav_files += 1
            song = WAVE(fil)
            length = song.info.length
            total_length += length
            for i in range(len(Range)):
                if Range[i][0] < length < Range[i][1]:
                    out[i] += 1
        if ".lab" in fil:
            num_lab_files += 1
    os.chdir("../")
    g = open("statictics.txt", "w+")
    g.write("The number of audio files are {}.\n".format(num_wav_files))
    g.write("The number of .lab files are {}.\n".format(num_lab_files))
    g.write("Average Size: {}.\n".format(total_length/num_wav_files))
    for p in range(len(Range)):
        g.write("The number of files whose length is between {} and {} are {}.\n".format(Range[p][0], Range[p][1], out[p]))
    return Path
    

data_path = analy_aud(os.path.abspath("mfa_data"), [[1,2],[3,5]])
os.chdir(data_path)
os.chdir("../")
out_path = os.getcwd()


lexi_path = os.path.abspath("librispeech-lexicon.txt")
output_path = os.path.join(out_path, "output")
input_path = os.path.abspath("mfa_data")
os.system(f"mfa align {input_path} {lexi_path} english {output_path}")