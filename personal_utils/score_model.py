import kaldi_io
import sys

dset = "train"
count = 0
emotion_mapping = ['ANG','DIS','FEA','HAP','NEU','SAD']

with open(f"local/data/{dset}_hires/predictions.ark.txt", "r") as f:
    for line in f:
        #print(line)
        emotion_values = line.split()
        print(emotion_values)
        closest_to_zero = sys.float_info.max
        closest_to_zero_ind = -1

        for i,emotion_value in enumerate(emotion_values):
            try: 
                emotion_val = float(emotion_value)
                if abs(emotion_val) < closest_to_zero:
                    closest_to_zero = abs(emotion_val)
                    closest_to_zero_ind = i
            except ValueError:
                # string is not a float
                break
        print(closest_to_zero_ind)
        emotion = emotion_mapping[closest_to_zero_ind]
        print(emotion)

        count+=1
        if count > 2:
            break
