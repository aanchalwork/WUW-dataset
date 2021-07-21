import textgrid
import os
import shutil
from pydub import AudioSegment
import nltk
from nltk.corpus import stopwords
import copy

def move_textgerid(src,trg):
    '''
    This Function renames the files in output and move all the files to the mfa_data directory
    '''
    li = os.listdir(src)
    for k in li:
        os.rename(os.path.join(src,k),os.path.join(src,k[9:]))
        shutil.move(os.path.join(src,k[9:]),trg)



def clipping_1(start, stop, name, wav_name, aud_path):
    '''
    Arguments:
        start    : start time in the wav file
        stop     : stop time in the wav file
        name     : name of the word which we are clipping
        wav_name : name of the wav file in the folder from which we are clipping
        aud_path : path of the directory where we want to save the audio file

    This function clips the word from the original file and add silence to the file at both the front and back of the clip to make it 1500 milliseconds of length.
    This is done with a stride length of 100 milliseconds.
    '''
    myaudio = AudioSegment.from_wav(wav_name+".wav", "wav")
    new_audio = myaudio[start : stop]
    tim = stop - start
    k = 0
    while(tim + k <= 1500):
        sil_audio = AudioSegment.silent(duration=k) + new_audio + AudioSegment.silent(duration=(1500-tim-k))
        n = len(sil_audio)
        sil_audio = sil_audio +  AudioSegment.silent(duration=1500-n)
        sil_audio.export(os.path.join(aud_path,name, name + str(int(k/100))+ "_" + wav_name +".wav"),"wav")
        k = k+ 100




def clipping_2(start, stop, name, wav_name, aud_path):
    '''
    Arguments:
        start    : start time in the wav file
        stop     : stop time in the wav file
        name     : name of the word which we are clipping
        wav_name : name of the wav file in the folder from which we are clipping
        aud_path : path of the directory where we want to save the audio file

    This function clips chuncks of 1500 milliseconds from the audio clip with a stride length of 100 milliseonds.
    '''
    myaudio = AudioSegment.from_wav(wav_name+".wav", "wav")
    if stop - 1500 < 0:
        initial = 0
    else:
        initial = stop - 1500
    while initial < start:
        audio_clip = myaudio[initial : initial + 1500]
        audio_clip.export(os.path.join(aud_path , name, name + str(int(initial/100))+ "_new_" + wav_name +".wav"),"wav")
        initial = initial + 100



def clipping(tim, name, wav_name, aud_path, new_audio):
    k = 0
    while(tim + k <= 1500):
        sil_audio = AudioSegment.silent(duration=k) + new_audio + AudioSegment.silent(duration=(1500-tim-k))
        n = len(sil_audio)
        sil_audio = sil_audio +  AudioSegment.silent(duration=1500-n)
        sil_audio.export(os.path.join(aud_path,name, name + str(int(k/100))+ "_" + wav_name +".wav"),"wav")
        k = k+ 100  




def monograms(tgrid, wav_name, stop_words, audio_list, aud_path):
    '''
    Arguments:
        tgrid      : textgrid file of a wav file
        wav_name   : name of the wav file
        stop_words : the words which we want to ignore while clipping
        audio_list : list of all the folders present in the audio directory
        aud_path   : path to the audio directory
    
    This function generates the monograms.
    '''
    total = []
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
                    
                    clipping_1(start, stop, name, wav_name, aud_path)
                    clipping_2(start, stop, name, wav_name, aud_path)
    
    return total, audio_list



def bigrams(tgrid, wav_name, stop_words, audio_list, aud_path):
    '''
    Arguments:
        tgrid      : textgrid file of a wav file
        wav_name   : name of the wav file
        stop_words : the words which we want to ignore while clipping
        audio_list : list of all the folders present in the audio directory
        aud_path   : path to the audio directory
    
    This function generates the bigrams.
    '''
    word_list = []
    silence = False
    for each in tgrid:
        if each.tier == "words":
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
                        
                        clipping(tim, name, wav_name, aud_path, new_audio)
                    word_list.clear()
                    word_list.append(copy.deepcopy(each))


def trigrams(total, wav_name, audio_list, aud_path):
    '''
    Arguments:
        total  : it contains all the words present in the wav_name audio clip
        wav_name : name of the audio file
        audio_list : list of all the folders present in the audio directory
        aud_path   : path to the audio directory
    '''
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
                        clipping(tim, name, wav_name, aud_path, new_audio)






stop_words = set(stopwords.words('english')) # Stop words: Words which we want to exclude
os.chdir("mfa_data/")
trg = os.getcwd() # it contains the path to mfa_data(dataset)
os.chdir("../")
main = os.getcwd()
os.mkdir(os.path.join(main,"audio")) # created a new folder named audio for storing the audio files after clipping.
os.chdir("audio/")
aud_path = os.getcwd() # the variable contains the path audio directory
os.chdir("../")
audio_list = os.listdir(aud_path) # This list contains all the folders on the audio diretory. Initially 0 folders because this directory is just created.
os.chdir("output/")
src = os.getcwd() # This variable contains the path to the textgrid files which were generated by the mfa aligner.
move_textgerid(src,trg)
os.chdir(trg)
li = os.listdir(trg)
for fil in li:
    if ".TextGrid" in fil:
        tgrid = textgrid.read_textgrid(fil)
        wav_name = fil[:-9]
        total, audio_list = monograms(tgrid, wav_name, stop_words, audio_list, aud_path)
        bigrams(tgrid, wav_name, stop_words, audio_list, aud_path)
        trigrams(total, wav_name, audio_list, aud_path)


