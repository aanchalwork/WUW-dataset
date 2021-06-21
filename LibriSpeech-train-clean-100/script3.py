import mutagen
import os
from mutagen.flac import FLAC
import xlsxwriter

def get_time(filename):
    f= open(filename,'r')
    li=[]
    for k in f:
        name, tex = k.strip().split(" ",1)
        voice = FLAC(name+".flac")
        li.append(voice.info.length)
    f.close()
    return li

# input the name of file
name1 = input("Name of the File: ")

# Creating xlsx
workbook = xlsxwriter.Workbook(name1+'.xlsx')
worksheet = workbook.add_worksheet()
row = 1

os.chdir(name1+'/')
path = os.getcwd()
li1 = os.listdir(path)
no_of_files=0
total_time = 0
for file1 in li1:
    os.chdir(file1+'/')
    path = os.getcwd()
    li2 = os.listdir(path)
    for file2 in li2:
        os.chdir(file2+'/')
        li= get_time(file1+'-'+file2+'.trans.txt')
        no_of_files += len(li)
        t1 = 0
        t2 = 0
        t3 = 0
        for k in li:
            if k < 2:
                t1+=1
            elif k >= 2 and k < 5:
                t2 += 1
            else:
                t3 +=1
        worksheet.write( row, 1 , file1)
        worksheet.write( row, 2 , file2)
        worksheet.write( row, 3 , len(li))
        worksheet.write( row, 4 , t1)
        worksheet.write( row, 5 , t2)
        worksheet.write( row, 6 , t3)
        row += 1
        os.chdir('../')
    os.chdir('../')  

# closing workbook
workbook.close()