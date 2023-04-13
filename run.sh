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
  # steps/make_mfcc_pitch.sh --nj 30 --cmd "$train_cmd" local/data/train
  # steps/compute_cmvn_stats.sh local/data/train
fi

if [ $stage -le 3 ]; then
 dir=local/data/tdnn1d_sp
 dset=test
 nj=10
 # --online-ivector-dir $dir/ivectors_${dset}_hires \
#  steps/nnet3/decode.sh --num-threads 4 --nj $nj --cmd "$decode_cmd" \
#           --acwt 1.0 --post-decode-acwt 10.0 \
#           --scoring-opts "--min-lmwt 5 " \
#          $dir/graph local/data/${dset}_hires $dir/decode_${dset} || exit 1;
#  echo "Neural network decoding done"

 $decode_cmd JOB=1:$nj $dir/log/compute_output.JOB.log \
 nnet3-compute --online-ivectors=scp:exp/nnet3_cleaned/ivectors_train_hires/ivector_online.scp --online-ivector-period=10  \
 $dir/final.mdl scp:local/data/train_hires/feats.scp ark:nnet_prediction.ark

 # --online-ivectors=scp:exp/nnet3_cleaned/ivectors_train_hires/ivector_online.scp --online-ivector-period=10 
 # use kaldi-io to convert bert embeddings to ark
 # <<1,2,3>, <4,5,6>> audio frames
 # <<1,1,1>> sentence
fi
 