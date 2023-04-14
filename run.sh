#!/usr/bin/env bash

# Main emotion identification script.

. ./path.sh || exit 1
. ./cmd.sh || exit 1

stage=0

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

 # --online-ivectors=scp:exp/nnet3_cleaned/ivectors_train_hires/ivector_online.scp --online-ivector-period=10 
 # use kaldi-io to convert bert embeddings to ark
 # <<1,2,3>, <4,5,6>> audio frames
 # <<1,1,1>> sentence
fi
 