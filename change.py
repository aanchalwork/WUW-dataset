from pydub import AudioSegment
import os
os.chdir("noise/")
cw = os.getcwd()
li = os.listdir()
for k in li:
    myaudio = AudioSegment.from_wav(k, "wav")
    new_audio = myaudio[0:1500]
    new_audio.export(os.path.join(cw,"au"+k+".wav"),"wav")