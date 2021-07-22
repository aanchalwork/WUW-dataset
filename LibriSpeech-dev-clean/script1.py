import os

def create_txt(filename):
    f= open(filename,'r')
    for k in f:
        name, tex = k.strip().split(" ",1)
        g = open(name+'.lab','w+')
        g.write(tex)
        g.close()
        os.system("mv "+name+".lab"+" ..")
    f.close()

def delete(filename):
    f= open(filename,'r')

    for k in f:
        name, tex = k.strip().split(" ",1)
        os.remove(name+'.txt')
    f.close()

def create_wav(filename):
    f= open(filename,'r')
    for k in f:
        name, tex = k.strip().split(" ",1)    
        os.system("ffmpeg -i "+ name + ".flac" + " -ac 1 -ar 16000"+" " + name + '.wav' )
        os.system("mv "+name+".wav"+" ..")
    f.close()    


os.chdir('dev-clean/')
path = os.getcwd()
li1 = os.listdir(path)
for file1 in li1:
    os.chdir(file1+'/')
    path = os.getcwd()
    li2 = os.listdir(path)
    for file2 in li2:
        os.chdir(file2+'/')
        create_txt(file1+'-'+file2+'.trans.txt')
        #delete(file1+'-'+file2+'.trans.txt')
        create_wav(file1+'-'+file2+'.trans.txt')
        os.chdir('../')
        os.system("rm -rf "+file2)
    os.chdir('../')  