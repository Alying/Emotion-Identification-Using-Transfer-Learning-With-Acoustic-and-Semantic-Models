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
  rm -r local/data/test*
  rm -r local/data/train*
  rm -r exp/tri3*

  personal_utils/prepare_data.sh
  utils/utt2spk_to_spk2utt.pl local/data/train/utt2spk > local/data/train/spk2utt
  utils/utt2spk_to_spk2utt.pl local/data/test/utt2spk > local/data/test/spk2utt
  utils/fix_data_dir.sh local/data/train
  utils/fix_data_dir.sh local/data/test

  utils/prepare_lang.sh personal_utils/lang "<unk>" local/data/lang_temp local/data/lang
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
  nj=5
  tar -xf personal_utils/tri3.tar.gz -C exp/

  for dset in test train
  do
    steps/align_si.sh --nj $nj --cmd "$train_cmd" \
    local/data/${dset}_hires local/data/lang exp/tri3 exp/tri3_${dset}_ali

    for i in exp/tri3_${dset}_ali/ali.*.gz;
      do ali-to-phones --ctm-output exp/tri3_${dset}_ali/final.mdl ark:"gunzip -c $i|" -> ${i%.gz}.ctm;
    done;

    cd exp/tri3_${dset}_ali
    cat *.ctm > merged_alignment.txt
    cd ../..

    rm -r local/data/${dset}_temp
    mkdir local/data/${dset}_temp
  done

  Rscript personal_utils/id2phone.R 
  python3 personal_utils/split_alignments.py

  python3 personal_utils/align_nnet.py
  echo "Running align code done"
fi

if [ $stage -le 5 ]; then
  python3 personal_utils/run_bert.py

  # dset="train" 
  # for file in local/data/${dset}_hires/bert_embeddings*.scp;
  # do cat $file >> local/data/${dset}_hires/bert_embeddings.scp
  # done

  # dset="test" 
  # for file in local/data/${dset}_hires/bert_embeddings*.scp;
  # do cat $file >> local/data/${dset}_hires/bert_embeddings.scp
  # done

  echo "Running bert model done"
fi

if [ $stage -le 6 ]; then
  for dset in train test;
  do paste-feats scp:local/data/${dset}_hires/bert_embeddings.scp  ark:local/data/${dset}_hires/nnet_prediction_aligned.ark ark,scp:local/data/${dset}_hires/combined.ark,local/data/${dset}_hires/combined.scp
  done
  echo "Concatenating features done"
fi

if [ $stage -le 7 ]; then
  python3 personal_utils/prepare_lda.py
  
  for dir in test train
  do
    utils/utt2spk_to_spk2utt.pl local/data/${dir}_hires/utt2spk2 > local/data/${dir}_hires/spk2utt2
    $train_cmd local/data/${dir}_hires/log/compute_mean.log \
      ivector-mean scp:local/data/${dir}_hires/lda_feats.scp \
      local/data/${dir}_hires/mean.vec || exit 1;
  done

  dir="train"  
  lda_dim=100
  $train_cmd local/data/${dir}_hires/log/lda.log \
    ivector-compute-lda --total-covariance-factor=0.0 --dim=$lda_dim \
    "ark:ivector-subtract-global-mean scp:local/data/${dir}_hires/lda_feats.scp ark:- |" \
    ark:local/data/${dir}_hires/utt2spk2 local/data/${dir}_hires/transform.mat || exit 1;

  $train_cmd local/data/${dir}_hires/log/plda.log \
    ivector-compute-plda ark:local/data/${dir}_hires/spk2utt2 \
    "ark:ivector-subtract-global-mean scp:local/data/${dir}_hires/lda_feats.scp ark:- | transform-vec local/data/${dir}_hires/transform.mat ark:- ark:- | ivector-normalize-length ark:-  ark:- |" \
    local/data/${dir}_hires/plda || exit 1;

  echo "Running LDA/PLDA done"
fi

if [ $stage -le 8 ]; then
  python3 personal_utils/create_trials.py

  $train_cmd local/data/test_hires/log/score_lda.log \
    ivector-plda-scoring --normalize-length=true \
    "ivector-copy-plda --smoothing=0.0 local/data/train_hires/plda - |" \
    "ark:ivector-subtract-global-mean local/data/train_hires/mean.vec scp:local/data/train_hires/lda_feats.scp ark:- | transform-vec local/data/train_hires/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean local/data/test_hires/mean.vec scp:local/data/test_hires/lda_feats.scp ark:- | transform-vec local/data/train_hires/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    local/data/test_hires/trials exp/scores || exit 1;

  echo "PLDA Scoring done"
fi

if [ $stage -le 9 ]; then
  python3 personal_utils/score_model.py
  echo "Scored Results"
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
