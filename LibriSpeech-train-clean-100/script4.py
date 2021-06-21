import os
import shutil

path = os.getcwd()
os.chdir("train-clean-100/")
li = os.listdir()
num = 0
for k in range(len(li)):
    if k % 51 == 0:
        num += 1
    shutil.move(path + '/train-clean-100/'+li[k], path + '/Input' + str(num))
