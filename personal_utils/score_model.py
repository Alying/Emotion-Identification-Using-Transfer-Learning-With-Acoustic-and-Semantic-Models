import kaldi_io
import sys

dset = "test"
count = 0
emotion_mapping = ['ANG','DIS','FEA','HAP','NEU','SAD']

total_utterances = 0
correct_emotions = 0
emotion_votes={}
current_emotion_id = ""
with open(f"local/data/{dset}_hires/predictions.ark.txt", "r") as f:
    for line in f:
        #print(line)
        emotion_values = line.split()
        closest_to_zero = sys.float_info.max
        closest_to_zero_ind = -1
        previous_emotion_id=""

        for i,emotion_value in enumerate(emotion_values):
            try: 
                emotion_val = float(emotion_value)
                if abs(emotion_val) < closest_to_zero:
                    closest_to_zero = abs(emotion_val)
                    closest_to_zero_ind = i
            except ValueError:
                # either the emotion id or ']'
                if len(emotion_value) > 3:
                    # if not first utterance id, compare voted emotion to actual emotion
                    if current_emotion_id != "":
                        previous_emotion_id = current_emotion_id
                        voted_emotion = max(emotion_votes, key=emotion_votes.get)
                        #print("===actual: ",previous_emotion_id,"voted: ",voted_emotion)
                        if previous_emotion_id == voted_emotion:
                            correct_emotions += 1
                           # print(correct_emotions)
                    current_emotion_id = emotion_value[:3]
                    emotion_votes = {'ANG':0,'DIS':0,'FEA':0,'HAP':0,'NEU':0,'SAD':0}
                    #print(emotion_value, emotion_idi)
                    total_utterances += 1
                break
        emotion = emotion_mapping[closest_to_zero_ind]
        emotion_votes[emotion] += 1

print("accuracy: ",correct_emotions/total_utterances, "correct_emotions: ", correct_emotions, "total utterances: ", total_utterances)
