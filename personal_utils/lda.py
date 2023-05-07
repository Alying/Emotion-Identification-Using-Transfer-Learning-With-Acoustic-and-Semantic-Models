# Author Daniel Mao
# Job: Unused in final code. Here in case we need to revisit

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import kaldi_io
from collections import OrderedDict

for DIR in ["test", "train"]:
    iter = 0
    check_sum = 0
    id_to_index_mapper = OrderedDict()

    for key,mat in kaldi_io.read_mat_scp(f'local/data/{DIR}_hires/combined.scp'):
        check_sum = check_sum + mat.shape[0]
        if iter == 0:
            X = mat
            Y = np.full((1, mat.shape[0]), iter)
        else:
            X = np.vstack((X, mat))
            Y = np.append(Y, np.full((1, mat.shape[0]), iter))

        id_to_index_mapper[key] = mat.shape[0]
        iter = iter + 1

    # print(X.shape)
    # print(check_sum)
    # print(Y.shape)

    clf = LinearDiscriminantAnalysis(n_components = 50)
    clf.fit(X, Y)

    X = clf.transform(X)

    # print(X.shape)
    # print(id_to_index_mapper)

    ark_scp_output=f'ark:| copy-feats --compress=true ark:- ark,scp:local/data/{DIR}_hires/feats.ark,local/data/{DIR}_hires/feats.scp'
    with kaldi_io.open_or_fd(ark_scp_output,'wb') as f:
      total_index = 0
      for key, index in id_to_index_mapper.items():
          mat = X[total_index:total_index+index, :]
          total_index = total_index + index
        #   print(index)
        #   print(mat.shape)
          kaldi_io.write_mat(f, mat, key=key)
