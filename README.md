# CLIPA Tool

Before using this tool some packages need to be installed. All the installations given below are done in [Anaconda](https://docs.anaconda.com/anaconda/install/windows/).
## Installation
For generating the aligned audio clips we use a third party tool, [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/introduction.html). So for installing this MFA tool follow the steps given in the [documentation](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html).<br />
If you have followed the installation steps given in the documentation we can observe that all the installation is done in an environment named aligner. Now the next steps should also be downloaded in the aligner environment. So before running the below commands make sure that you are in the aligner environment ("conda activate aligner").<br/>

pip install mutagen <br/>
conda install -c main ffmpeg <br/>
pip install pydub <br/>
conda install -c anaconda git <br/>
git clone https://github.com/kylerbrown/textgrid.git <br/>
cd textgrid <br/>
pip install . <br/>
Install the NLTK module from the [website](https://www.nltk.org/install.html)

### get_output.py
This script is used for changing the directory structure and running the mfa aligner on the mfa_data. The output files will be stored in the directory named output.<br/>

**Note**: 
1. The dataset name should be *mfa_data* or you can just clone this repisitory and copy all the dataset files in the mfa_data.  
1. The dataset files should contain the audio files(16 bit mono wav file) and their corresponding .lab files with same name.

### get_audio.py
This script generates the audio clips of words whose word length lies between 4 and 25 and time length lies between 0.5 and 1.5 seconds and then the clipping is done.
Clipping is done in the follwing methods mentioned:
1.  All these audio clips are clipped such a way that silence is added to the clip before and after with a stride length of 100 milli seconds to make the time length 1500 milli seconds.
2. Chuncks of 1500 milliseconds are taken out from the audio clip in different time ranges with stride length of 100 milliseconds such a way that the required word is present in it.
3. Clipping is done such a way that 2 adjacent words are clipped from the sentence. Silence is added as mentioned in method 1.

**Note**:
1. If a stop word is in between 2 words then these words are also adjacent. In this case stop word is removed and a silence of 100 milliseconds is added between 2 words.<br/>

First this script moves all the .textgrid files in output to mfa_data directory. Then it clips out individual words with the help of textgrid files and it does clipping as discussed above. All these files are in the audio folder.

After running the installation steps run the get_output.py and then the get_audio.py.

