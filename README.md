# LibriSpeech-dataset
This repository contans 5 datasets namely
* LibriSpeech-Dev-clean
* LibriSpeech-test-clean
* LibriSpeech-Dev-other
* LibriSpeech-test-other
* LibriSpeech-train-clean-100

Each folder contains Input files, Output files and some other files which are downloaded from the slr.

For each audio files we have
* .Wav files
* .Lab files
* .textgrid file

## Aligning
For generating the output files, I used the montreal forced aligner. A pretrained english model was used to generate the outputs and the dictionary used was Librispeech-lexicon.txt. For using the aligner the documentation structure should be in a specific format. The audio files and their corresponding text files should be in same directory. The format for the files are mentioned below.
### Audio File
* Bit Depth : 16 bit
* Type : .WAV
* Sampling Rate : 16KHz

### Text File
* Type : .LAB

### Output
* Type : .TEXTGRID
To know more about the data formats visit the Montreal forced aligner documentation.

## Documentation Statictics
### LibriSpeech-dev-other
