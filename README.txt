---Names & Unis---
Alina Ying ay2355
Daniel Mao dm3559

---Date---
5/6/2023

---Project Name---
Emotion Identification Project

---Project Summary---
Identifying human emotion is a hard task because emotions are a subjective experiment; however, 
being able to automatically recognize them could have potentially major impact in the fields of 
mental health, trade negotiation, and much more. This paper describes an emotion recognition 
system that uses transfer learning to leverage both the information from the acoustic features 
of the speech signal and the semantic features of the utterances. We show that with our system 
we are able to achieve state of the art level results with a 72.5% accuracy when trained and 
tested on the Crema-D dataset.

---How to run---
(1) Run install.sh to get necessary prerequisites
(2) Run run.sh (you do not need to run path.sh or run.sh they are executed in run.sh)

---Directory breakdown---
(1) conf/ contains all the configuration files for running kaldi scripts.
(2) exp/ contains intermediate output files, mainly the alignment ones
(3) kaldi-io-for-python necessary to get the kaldi-io plugin to run
(4) local/data contains all the downloaded input data and intermediate results. Includes the 
    train/test directories.
    (4.1) lang/ contains all the necessary files to create the language model
    (4.2) tri3.tar.gz is the triphone model from kaldi (trained by ourselves since original 
          doesn't work). Uses lang/ in alingment.
(5) personal_utils/ all the scripts that we wrote ourselves to get the project to run
(6) results/ contains all results from different experiments. New results are written here as "scores"
    files
(7) rnnlm/ sid/ steps/ utils/ all symbolic links to access different kaldi scripts

---Contributions---
Alina - created personal_utils/split_data.sh
                personal_utils/download_data.sh
                personal_utils/run_bert.sh
Daniel - created everything else underneath personal_utils/
We both contributed to run.sh and install.sh

---GitHub Link---
https://github.com/Alying/emotion_identification_research_project
