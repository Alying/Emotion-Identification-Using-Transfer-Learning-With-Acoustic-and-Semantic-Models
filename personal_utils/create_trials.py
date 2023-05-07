# Author Daniel Mao
# Job: Creates trials file for pLDA to score
# Input: Expects to see lda_feats.scp+ark in local/data/train_hires and test_hires
# Output: Creates trials file in local/data/test_hires

import numpy as np
import kaldi_io, random

def getRep(id):
    parts = id.split("_")
    return parts[1] + "_" + parts[2] + "_" + parts[3]

def replaceRepEmotion(rep, emo):
    parts = rep.split("_")
    return parts[0] + "_" + emo + "_" + parts[2]

rep_ids = {}
for key,_ in kaldi_io.read_vec_flt_scp(f'local/data/train_hires/lda_feats.scp'):
    rep_ids[key] = getRep(key)
random.seed(777)
temp = list(rep_ids.items())
random.shuffle(temp)
rep_ids_shuffled = dict(temp)

key_list = list(rep_ids_shuffled.keys())
val_list = list(rep_ids_shuffled.values())

test_ids = {}
emotions = ["ANG", "DIS", "FEA", "HAP", "NEU", "SAD"]
for key,_ in kaldi_io.read_vec_flt_scp(f'local/data/test_hires/lda_feats.scp'):
    compares = []
    for emotion in emotions:
        standard = replaceRepEmotion(getRep(key), emotion)
        if standard not in val_list:
            splitted = standard.split("-")
            nstandard = splitted[0][:-2]+"XX-"+splitted[1]
            if nstandard in val_list:
                compares.append(nstandard)
                continue
            nstandard = splitted[0][:-2]+"MD-"+splitted[1]
            if nstandard in val_list:
                compares.append(nstandard)
                continue
            nstandard = splitted[0][:-2]+"HI-"+splitted[1]
            if nstandard in val_list:
                compares.append(nstandard)
                continue
            nstandard = splitted[0][:-2]+"LO-"+splitted[1]
            if nstandard in val_list:
                compares.append(nstandard)
                continue
            
            print("encountered test example with no corresponding train golden, skipping it")
            continue
        else:
            compares.append(standard)
    test_ids[key] = compares
    # print(test_ids[key])

with open(f"local/data/test_hires/trials", 'w') as f: 
    for key,value in test_ids.items(): 
        for test_id in value:
            compare_id = key_list[val_list.index(test_id)]
            f.write('%s %s\n' % (compare_id, key))

print("Trials created")