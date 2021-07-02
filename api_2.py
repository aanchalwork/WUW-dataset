import os

os.system("conda create -n aligner2 -c conda-forge openblas python=3.8 openfst pynini ngram baumwelch")
os.system("conda activate aligner2")
os.system("pause")
'''
os.system("pip install mutagen")
os.system("pip install montreal-forced-aligner")
os.system("mfa thirdparty download")
os.system("mfa thirdparty kaldi /path/to/kaldi/repo")
os.system("mfa thirdparty validate")
os.system("mfa download acoustic english")
'''