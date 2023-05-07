# Author Daniel Mao
# Job: Parse the CremaD dataset into the necessary kaldi prerequisites
# Input: Expects the local/data/CREMA-D/
# Output: Creates text, segments, utt2spk, wav.scp in local/data/train and test

import os
import os.path
import random
import pandas as pd
import wave
import contextlib
 
cwd = os.getcwd()
 
train_percent = 0.80
test_percent = 0.20
 
def tied_emotions(row):
    emotions = str.split(row, ':')
 
    # normal single emotion
    if len(emotions) < 2:
        return emotions[0]
 
    # ignore Neutrals in tied emotions
    try:
        emotions.remove('N')
    except:
        True
 
    # pick random emotion among remaining emotions
    return random.choice(emotions)
 
def get_text(id):
    text_mapper = {
        "IEO": "It's eleven o'clock.",
        "TIE": "That is exactly what happened.",
        "IOM": "I'm on my way to the meeting.",
        "IWW": "I wonder what this is about.",
        "TAI": "The airplane is almost full.",
        "MTI": "Maybe tomorrow it will be cold.",
        "IWL": "I would like a new alarm clock.",
        "ITH": "I think I have a doctor's appointment.",
        "DFA": "Don't forget a jacket.",
        "ITS": "I think I've seen this before.",
        "TSI": "The surface is slick.",
        "WSI": "We'll stop in a couple of minutes."
    }
    result = text_mapper.get(id.upper())
    if result is None:
        raise Exception("Unknown id for get_text")
    return result
 
def getWavDuration(path):
    with contextlib.closing(wave.open(path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration
 
# TODO: Need to add remaining row
def createOutputsTrain(df, path):
    with open(path + "wav.scp", 'a') as f:
        dfAsString = df[:train_rows][["utteranceId", "path"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "utt2spk", 'a') as f:
        dfAsString = df[:train_rows][["utteranceId", "emotion"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "text", 'a') as f:
        dfAsString = df[:train_rows][["utteranceId", "text"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "segments", 'a') as f:
        dfAsString = df[:train_rows][["utteranceId", "utteranceId", "durationStart", "durationEnd"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")

def createOutputsTest(df, path):
    with open(path + "wav.scp", 'a') as f:
        dfAsString = df[train_rows:train_rows+test_rows][["utteranceId", "path"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "utt2spk", 'a') as f:
        dfAsString = df[train_rows:train_rows+test_rows][["utteranceId", "emotion"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "text", 'a') as f:
        dfAsString = df[train_rows:train_rows+test_rows][["utteranceId", "text"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "segments", 'a') as f:
        dfAsString = df[train_rows:train_rows+test_rows][["utteranceId", "utteranceId", "durationStart", "durationEnd"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
 

# if os.path.isfile("../local/data/test/data.csv") or os.path.isfile("../local/data/train/data.csv"):
#    quit()
 
# read in csv
df = pd.read_csv("../local/data/CREMA-D/processedResults/tabulatedVotes.csv")
 
# drop unnecessary columns
df = df.iloc[: , 1:11]
 
# do column transforms
df['emoVote'] = df['emoVote'].apply(tied_emotions)
df['text'] = df.apply(lambda row: get_text(row.fileName.split('_')[1]), axis=1)
df['utteranceId'] = df.apply(lambda row: row.fileName.split('_')[2] + "-" + row.fileName, axis=1)
df['emotion'] = df.apply(lambda row: row.fileName.split('_')[2], axis=1)
df['path'] = df.apply(lambda row: "local/data/CREMA-D/AudioWAV/" + row.fileName + ".wav", axis=1)
df['durationStart'] = df.apply(lambda row: 0.0, axis=1)
df['durationEnd'] = df.apply(lambda row: getWavDuration("../" + row.path), axis=1)
 
# print(df['utteranceId'].head)
 
# split train, test data
total_rows = df.shape[0]
train_rows = int(total_rows*train_percent)
test_rows = int(total_rows*test_percent)
 
createOutputsTrain(df, "../local/data/train/")
createOutputsTest(df, "../local/data/test/")
