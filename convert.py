import csv
import os

os.chdir("data2/")
li = os.listdir()

for file in li:
    os.chdir(file+"/")
    with open("line_index.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            g = open(row[1][4:]+".lab","w+")
            g.write(row[2])
            g.close()
            os.system("ffmpeg -i "+ row[1] + ".wav" + " -acodec pcm_s16le -ac 1 -ar 16000 " + row[1][4:] + '.wav' )
            os.system("rm "+row[1]+".wav")
    os.chdir("../")