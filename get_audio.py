import textgrid
import os
import shutil
from pydub import AudioSegment

os.chdir("mfa_data/")
trg = os.getcwd()
os.chdir("../")
main = os.getcwd()
os.mkdir(os.path.join(main,"audio"))
os.chdir("audio/")
aud_path = os.getcwd()
os.chdir("../")
audio_list = os.listdir(aud_path)
os.chdir("output/")
src = os.getcwd()
li = os.listdir()
for k in li:
    os.rename(os.path.join(src,k),os.path.join(src,k[9:]))
    shutil.move(os.path.join(src,k[9:]),trg)

os.chdir(trg)
li = os.listdir()

for fil in li:
    if ".TextGrid" in fil:
        tgrid = textgrid.read_textgrid(fil)
        wav_name = fil[:-9]
        for each in tgrid:
            if each.tier == "words":
                tim = each.stop - each.start
                tim = tim * 1000
                name = each.name.lower()
                if 25 > len(name) > 4 and 1500 > tim > 500:
                    if name not in audio_list:
                        os.mkdir(os.path.join(aud_path,name))
                        audio_list.append(name)
                    myaudio = AudioSegment.from_wav(wav_name+".wav", "wav")
                    new_audio = myaudio[float(each.start)*1000 : float(each.stop)*1000]
                    k = 0
                    while(tim + k <= 1500):
                        sil_audio = AudioSegment.silent(duration=k) + new_audio + AudioSegment.silent(duration=(1500-tim-k))
                        sil_audio.export(os.path.join(aud_path,name,name+str(int(k/100))+".wav"),"wav")
                        k = k+ 100
                    

                    
                    









    

