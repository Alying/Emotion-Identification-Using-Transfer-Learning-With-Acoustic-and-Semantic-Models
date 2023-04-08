import os
import os.path
import random
import pandas as pd
from sklearn.model_selection import train_test_split
cwd = os.getcwd()

train_percent = 0.1

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

# read in csv
df = pd.read_csv("../local/data/CREMA-D/processedResults/tabulatedVotes.csv")

# get emotion labels
df['emoVote'] = df['emoVote'].apply(tied_emotions)
#print(df.emoVote.head(15))

# drop unnecessary columns
df = df.iloc[: , 1:]

# split train, test data
total_rows = df.shape[0]
train_rows = int(total_rows*train_percent)

if os.path.isfile("../local/data/test/data.csv") or os.path.isfile("../local/data/train/data.csv"):
   quit()

df[:train_rows].to_csv("../local/data/train/data.csv",
          index=False,
          header=True,
          mode='a')

df[train_rows+1:].to_csv("../local/data/test/data.csv",
          index=False,
          header=True,
          mode='a')
