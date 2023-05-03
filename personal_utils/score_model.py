from collections import Counter
 
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

emotion_mapping = ['ANG','DIS','FEA','HAP','NEU','SAD']

id_to_votes = {}
with open(f"exp/scores", "r") as f:
    index = 0
    biggest = -99
    biggest_index = 0

    for line in f:
        tokens = line.strip().split(" ")
        if float(tokens[2]) > biggest:
            biggest = float(tokens[2])
            biggest_index = index

        index = index + 1
        if index >= 6:
            if tokens[1][:-2] not in id_to_votes:
                id_to_votes[tokens[1][:-2]] = []
            id_to_votes[tokens[1][:-2]].append(biggest_index)
            index = 0
            biggest = -99
            biggest_index = 0

correct_emotions = 0.0 
for k in id_to_votes:
    id_to_votes[k] = most_frequent(id_to_votes[k])
    correct_emo = k.split("-")[0]
    predicted_emo = emotion_mapping[id_to_votes[k]]
    if predicted_emo != correct_emo:
        correct_emotions = correct_emotions + 1

print("accuracy: ", correct_emotions/float(len(id_to_votes)), "correct_emotions: ", correct_emotions, "total utterances: ", len(id_to_votes))
