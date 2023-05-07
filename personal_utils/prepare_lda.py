# Author Daniel Mao
# Job: Creates necessary prereq files for Kaldi's lda algorithm to run
# Input: Expects to see combined.scp+ark in local/data/train_hires and test_hires
# Output: Creates lda_feats.scp+ark and utt2spk2 files in train_hires and test_hires

import numpy as np
import kaldi_io, codecs, math
# from collections import OrderedDict

DIR = "train"

for DIR in ["train", "test"]:
    id_to_mat = {}
    for key,mat in kaldi_io.read_mat_scp(f'local/data/{DIR}_hires/combined.scp'):
        for i in range(mat.shape[0]):
            id_to_mat[key + "-" + str(i)] = mat[i:i+1, :]

    ark_scp_output=f'ark:| copy-vector ark:- ark,scp:local/data/{DIR}_hires/lda_feats.ark,local/data/{DIR}_hires/lda_feats.scp'
    # ark_scp_output=f'local/data/{DIR}_hires/test.ark'
    with kaldi_io.open_or_fd(ark_scp_output,'wb') as f:
        for key,mat in id_to_mat.items():
            #print(key,":",mat[0])
            kaldi_io.write_vec_flt(f, mat[0], key=key)

    with open(f"local/data/{DIR}_hires/utt2spk2", 'w') as f: 
        for key in id_to_mat: 
            f.write('%s %s\n' % (key, key.split('-')[0]))
