#!/usr/bin/env bash

# Main emotion identification script.

. ./path.sh || exit 1
. ./cmd.sh || exit 1

stage=6

# Data preparation
if [ $stage -le 0 ]; then
  personal_utils/download_data.sh
  echo "Download data done"
fi

if [ $stage -le 1 ]; then
  personal_utils/prepare_data.sh
  utils/utt2spk_to_spk2utt.pl local/data/train/utt2spk > local/data/train/spk2utt
  utils/utt2spk_to_spk2utt.pl local/data/test/utt2spk > local/data/test/spk2utt
  utils/fix_data_dir.sh local/data/train
  utils/fix_data_dir.sh local/data/test
  echo "Prepare data done"
fi

if [ $stage -le 2 ]; then
  personal_utils/run_ivector_common.sh
  echo "Ivector common done"
fi

if [ $stage -le 3 ]; then
  personal_utils/run_acoustic_model.sh
  echo "Running acoustic model done"
fi
 
if [ $stage -le 4 ]; then
  python3 personal_utils/run_bert.py
  echo "Running bert model done"
fi

if [ $stage -le 4 ]; then
  dset=train
  paste-feats ark:local/data/${dset}_hires/bert_embeddings.ark  ark:local/data/${dset}_hires/nnet_prediction.ark ark,scp:local/data/${dset}_hires/combined.ark,local/data/${dset}_hires/combined.scp
  echo "Concatenating features done"
fi

if [ $stage -le 5 ]; then
  python3 personal_utils/lda.py
  echo "Running LDA done"
fi

if [ $stage -le 6 ]; then
  personal_utils/run_tdnn.sh
  echo "TDNN created and trained"
fi

if [ $stage -le 7 ]; then
  dir="local/data/train_hires"
  nj=3

  $decode_cmd JOB=1:$nj compute_output.JOB.log \
  nnet3-compute $dir/nnet/final.raw scp:$dir/feats.scp ark,scp:$dir/predictions.ark,$dir/predictions.scp

  echo "Ran embeddings through TDNN"
fi


#/data/train_hires/nnet_prediction.scp
# paste-feats 
# ivector-compute-lda (https://github.com/kaldi-asr/kaldi/blob/59299d1cf95b72bb109d583947d9e9ece19aa6dc/egs/voxceleb/v2/run.sh#L175)

#do we need minibatches
#any recommendations on our tdnn architecutre
#does lda work? we could get lda to work, since we cannot generate ivectors for our concatenated embeddings. (unable to convert feat to vects)
#when lda how many classes do you recommend to fit on? use emotion classes
# extract-xvectors
# egs generation script gets random chunk from audio file. use voxceleb/v2. nnet-copy-egs to see content of egs. 
# NJ(num jobs) controls the number of ark files

# utt2spk speaker should be emotion
