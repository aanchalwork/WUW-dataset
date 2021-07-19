import textgrid
import os
import shutil
from pydub import AudioSegment
import nltk
from nltk.corpus import stopwords
import copy


stop_words = set(stopwords.words('english'))
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
        word_list = []
        total = []
        silence = False
        for each in tgrid:
            if each.tier == "words":
                if each.name.lower() not in stop_words:
                    tim = each.stop - each.start
                    tim = tim * 1000
                    name = each.name.lower()
                    start = float(each.start)*1000
                    stop = float(each.stop)*1000
                    if 25 > len(name) > 4 and 1500 > tim > 500:
                        total.append([name,start,stop])
                        if name not in audio_list:
                            os.mkdir(os.path.join(aud_path,name))
                            audio_list.append(name)
                        myaudio = AudioSegment.from_wav(wav_name+".wav", "wav")
                        new_audio = myaudio[start : stop]
                        k = 0
                        while(tim + k <= 1500):
                            sil_audio = AudioSegment.silent(duration=k) + new_audio + AudioSegment.silent(duration=(1500-tim-k))
                            n = len(sil_audio)
                            sil_audio = sil_audio +  AudioSegment.silent(duration=1500-n)
                            sil_audio.export(os.path.join(aud_path,name, name + str(int(k/100))+ "_" + wav_name +".wav"),"wav")
                            k = k+ 100
                        
        
                        if stop - 1500 < 0:
                            initial = 0
                        else:
                            initial = stop - 1500
                        while initial < start:
                            audio_clip = myaudio[initial : initial + 1500]
                            audio_clip.export(os.path.join(aud_path , name, name + str(int(initial/100))+ "_new_" + wav_name +".wav"),"wav")
                            initial = initial + 100
                

               

                if len(word_list) == 0:
                    if each.name.lower() not in stop_words and each.name != "":
                        word_list.append(copy.deepcopy(each))
                elif len(word_list) == 1:
                    if each.name.lower() in stop_words or each.name == "":
                        silence = True
                    else:
                        word_list.append(copy.deepcopy(each))
                        if silence == False:
                            start2 = word_list[0].start
                            stop2 = word_list[1].stop
                            start2 = start2 * 1000
                            stop2 = stop2 * 1000
                            tim = stop2 - start2
                            myaudio = AudioSegment.from_wav(wav_name+".wav", "wav")
                            new_audio = myaudio[start2 : stop2]
                        else:
                            start2 = word_list[0].start
                            stop2 = word_list[0].stop + word_list[1].stop - word_list[1].start + 0.1
                            start2 = start2 * 1000
                            stop2 = stop2 * 1000
                            tim = stop2 - start2
                            myaudio = AudioSegment.from_wav(wav_name+".wav", "wav")
                            new_audio = myaudio[float(word_list[0].start)*1000 : float(word_list[0].stop)*1000] + AudioSegment.silent(duration=100) + myaudio[float(word_list[1].start)*1000 : float(word_list[1].stop)*1000]
                            silence = False                       
                        name = word_list[0].name.lower() + "_" + word_list[1].name.lower()
                        if tim < 1500:
                            if name not in audio_list:
                                os.mkdir(os.path.join(aud_path,name))
                                audio_list.append(name)
                            
                            
                            k = 0
                            while(tim + k <= 1500):
                                sil_audio = AudioSegment.silent(duration=k) + new_audio + AudioSegment.silent(duration=(1500-tim-k))
                                n = len(sil_audio)
                                sil_audio = sil_audio +  AudioSegment.silent(duration=1500-n)
                                sil_audio.export(os.path.join(aud_path,name, name + str(int(k/100))+ "_" + wav_name +".wav"),"wav")
                                k = k+ 100
                        word_list.clear()
                        word_list.append(copy.deepcopy(each))




        if len(total) >= 3:
            length = len(total)
            for i in range(0,length-2):
                for j in range(i+1,length-1):
                    for k in range(i+2,length):
                        name = total[i][0] + "_" + total[j][0] + "_" + total[k][0]
                        myaudio = AudioSegment.from_wav(wav_name+".wav", "wav")
                        new_audio = myaudio[total[i][1] : total[i][2]] + AudioSegment.silent(duration=100) + myaudio[total[j][1] : total[j][2]] + AudioSegment.silent(duration=100) + myaudio[total[k][1] : total[k][2]]
                        tim = total[i][2] - total[i][1] + total[j][2] - total[j][1] + total[k][2] - total[k][1] + 200
                        if tim < 1500:
                            if name not in audio_list:
                                os.mkdir(os.path.join(aud_path,name))
                                audio_list.append(name)
                        k = 0
                        while(tim + k <= 1500):
                            sil_audio = AudioSegment.silent(duration=k) + new_audio + AudioSegment.silent(duration=(1500-tim-k))
                            n = len(sil_audio)
                            sil_audio = sil_audio +  AudioSegment.silent(duration=1500-n)
                            sil_audio.export(os.path.join(aud_path,name, name + str(int(k/100))+ "_" + wav_name +".wav"),"wav")
                            k = k+ 100
                        




                    

                    
                    









    

