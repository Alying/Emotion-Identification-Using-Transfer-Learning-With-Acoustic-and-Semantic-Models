import os
import os.path
import random
import pandas as pd
cwd = os.getcwd()

train_percent = 0.03

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

def createOutputs(df, path):
    with open(path + "wav.scp", 'a') as f:
        dfAsString = df[:train_rows][["recordingId", "path"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "utt2spk", 'a') as f:
        dfAsString = df[:train_rows][["utteranceId", "utteranceId"]].to_string(header=False, index=False)
        f.write(dfAsString + "\n")
    with open(path + "text", 'a') as f:
        dfAsString = df[:train_rows][["utteranceId", "text"]].to_string(header=False, index=False)
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
df['utteranceId'] = df.apply(lambda row: row.fileName, axis=1)
df['recordingId'] = df.apply(lambda row: row.fileName, axis=1)
df['path'] = df.apply(lambda row: "local/data/CREMA-D/AudioWAV/" + row.fileName + ".wav", axis=1)

# split train, test data
total_rows = df.shape[0]
train_rows = int(total_rows*train_percent)

createOutputs(df, "../local/data/train/")
createOutputs(df, "../local/data/test/")
