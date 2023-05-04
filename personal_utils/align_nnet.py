import numpy as np
import kaldi_io, codecs, math
# from collections import OrderedDict

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

lex = {}
with codecs.open("personal_utils/lang/lexiconp.txt", "rb", "utf-8") as f:
    for line in f:
        line = line.strip()
        columns = line.split("\t")
        word = columns[0].split(" ")[0]
        length = len(columns[1].split(" "))
        lex[word] = length

for DIR in ["train", "test"]:
    id_to_mat = {}
    id_to_redmat = {}
    id_to_ts = {}
    for key,mat in kaldi_io.read_mat_scp(f'local/data/{DIR}_hires/nnet_prediction.scp'):
        id_to_mat[key] = mat

    for key in id_to_mat:
        try:
            with open(f"local/data/{DIR}_temp/{key}.txt") as f:
                id_to_ts[key] = []
                last = -1
                for line in f:
                    line = line.strip()
                    line = line.split("\t")
                    id_to_ts[key].append(float(line[-2]))
                    last = max(float(line[-2]) + float(line[-1]), last)
                    
                id_to_ts[key].append(round(last, 2))
                id_to_ts[key].sort()
                id_to_ts[key].pop(0)
                # print(id_to_ts[key])
        except:
            id_to_ts[key] = []

    for key in id_to_mat:
        sentence = get_text(key.split("_")[1])
        sentence = sentence.rstrip(sentence[-1])
        phones = 0
        for word in sentence.split(" "):
            phones = phones + lex[word.lower()]

        # cannot get actual align so assume percentages based on number of phones per word
        if phones > len(id_to_ts[key]):
            slice_index = 0
            arr = sentence.split(" ")

            for i, word in enumerate(arr):
                percent = lex[word.lower()] / float(phones)

                if i >= len(arr) - 1:
                    id_to_redmat[key] = np.vstack((id_to_redmat[key], id_to_mat[key][slice_index:, :].mean(0)))
                else:
                    if i == 0:
                        id_to_redmat[key] = id_to_mat[key][slice_index:math.floor(slice_index + percent * id_to_mat[key].shape[0]), :].mean(0)
                    else:
                        id_to_redmat[key] = np.vstack((id_to_redmat[key], id_to_mat[key][slice_index:math.floor(slice_index + percent * id_to_mat[key].shape[0]), :].mean(0)))
                    slice_index = math.floor(slice_index + percent * id_to_mat[key].shape[0])
        else:        
            index = -1
            previous = 0
            slice_index = 0
            arr = sentence.split(" ")

            for i, word in enumerate(arr):
                index = index + lex[word.lower()]
                percent = (id_to_ts[key][index] - previous) / id_to_ts[key][-1]
                previous = id_to_ts[key][index]

                if i >= len(arr) - 1:
                    id_to_redmat[key] = np.vstack((id_to_redmat[key], id_to_mat[key][slice_index:, :].mean(0)))
                else:
                    if i == 0:
                        id_to_redmat[key] = id_to_mat[key][slice_index:math.floor(slice_index + percent * id_to_mat[key].shape[0]), :].mean(0)
                    else:
                        id_to_redmat[key] = np.vstack((id_to_redmat[key], id_to_mat[key][slice_index:math.floor(slice_index + percent * id_to_mat[key].shape[0]), :].mean(0)))
                    slice_index = math.floor(slice_index + percent * id_to_mat[key].shape[0])


    ark_scp_output=f'ark:| copy-feats ark:- ark,scp:local/data/{DIR}_hires/nnet_prediction_aligned.ark,local/data/{DIR}_hires/nnet_prediction_aligned.scp'
    with kaldi_io.open_or_fd(ark_scp_output,'wb') as f:
        for key, value in id_to_redmat.items():
            kaldi_io.write_mat(f, value, key=key)