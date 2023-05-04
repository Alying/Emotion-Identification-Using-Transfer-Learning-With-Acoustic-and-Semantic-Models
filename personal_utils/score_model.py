from collections import Counter
import os

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

emotion_mapping = ['ANG','DIS','FEA','HAP','NEU','SAD']

directory = 'results'
 
for filename in os.listdir(directory):
    fpath = os.path.join(directory, filename)

    id_to_votes = {}
    with open(fpath, "r") as f:
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
    correct_emotions_l = [0, 0, 0, 0, 0, 0]
    emotions_total_l = [0, 0, 0, 0, 0, 0]
    for k in id_to_votes:
        id_to_votes[k] = most_frequent(id_to_votes[k])
        correct_emo = k.split("-")[0]
        predicted_emo = emotion_mapping[id_to_votes[k]]
        if predicted_emo == correct_emo:
            correct_emotions = correct_emotions + 1
            correct_emotions_l[id_to_votes[k]] = correct_emotions_l[id_to_votes[k]] + 1
        elif predicted_emo == "ANG" and correct_emo == "DIS":
            correct_emotions = correct_emotions + 1
            correct_emotions_l[id_to_votes[k]] = correct_emotions_l[id_to_votes[k]] + 1
        elif predicted_emo == "DIS" and correct_emo == "ANG":
            correct_emotions = correct_emotions + 1
            correct_emotions_l[id_to_votes[k]] = correct_emotions_l[id_to_votes[k]] + 1

        emotions_total_l[id_to_votes[k]] = emotions_total_l[id_to_votes[k]] + 1

    print("TOTAL accuracy: ", correct_emotions/float(len(id_to_votes)), "correct_emotions: ", correct_emotions, "total utterances: ", len(id_to_votes))
    print("ANG accuracy: ", correct_emotions_l[0]/float(emotions_total_l[0]), "correct_emotions: ", correct_emotions_l[0], "total utterances: ", emotions_total_l[0])
    print("DIS accuracy: ", correct_emotions_l[1]/float(emotions_total_l[0]), "correct_emotions: ", correct_emotions_l[1], "total utterances: ", emotions_total_l[1])
    print("FEA accuracy: ", correct_emotions_l[2]/float(emotions_total_l[0]), "correct_emotions: ", correct_emotions_l[2], "total utterances: ", emotions_total_l[2])
    print("HAP accuracy: ", correct_emotions_l[3]/float(emotions_total_l[0]), "correct_emotions: ", correct_emotions_l[3], "total utterances: ", emotions_total_l[3])
    print("NEU accuracy: ", correct_emotions_l[4]/float(emotions_total_l[0]), "correct_emotions: ", correct_emotions_l[4], "total utterances: ", emotions_total_l[4])
    print("SAD accuracy: ", correct_emotions_l[5]/float(emotions_total_l[0]), "correct_emotions: ", correct_emotions_l[5], "total utterances: ", emotions_total_l[5])
    print(f"Finished processing {fpath}")

