import os
import random
import pandas as pd
from sklearn.model_selection import train_test_split
cwd = os.getcwd()

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

df['emoVote'] = df['emoVote'].apply(tied_emotions)
print(df.emoVote.head(15))

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.2)
print(cwd)
print("HELLO")

