# Author Daniel Mao
# Job: Creates iVectors and mfcc_pitch features. Mainly copied from Kaldi side.
# Input: Expects local/data/train and test
# Output: Creates local/data_train_hires and test_hires. Also creates ivector extractors
# in exp/

#!/usr/bin/env bash

set -e -o pipefail

# This script contains the common feature preparation and iVector-related parts
# of the script.  See those scripts for examples of usage.

stage=0
nj=5

train_set=train 
online_cmvn_iextractor=false

num_threads_ubm=8
nnet3_affix=_cleaned     # affix for exp/nnet3 directory to put iVector stuff in, so it
                         # becomes exp/nnet3_cleaned or whatever.

. utils/parse_options.sh

# lowres features, alignments
if [ -f local/data/${train_set}/feats.scp ] && [ $stage -le 2 ]; then
  echo "$0: local/data/${train_set}/feats.scp already exists.  Refusing to overwrite the features "
  echo " to avoid wasting time.  Please remove the file and continue if you really mean this."
  exit 1;
fi

if [ $stage -le 1 ]; then
  for datadir in ${train_set} test; do
    utils/copy_data_dir.sh local/data/$datadir local/data/${datadir}_hires
  done
fi

if [ $stage -le 2 ]; then
  echo "$0: making MFCC features for low-resolution speed-perturbed data"
  steps/make_mfcc_pitch.sh --nj $nj \
    --cmd "$train_cmd" local/data/${train_set}
  steps/compute_cmvn_stats.sh local/data/${train_set}
  echo "$0: fixing input data-dir to remove nonexistent features, in case some "
  echo ".. speed-perturbed segments were too short."
  utils/fix_data_dir.sh local/data/${train_set}
fi

if [ $stage -le 3 ] && [ -f local/data/${train_set}_hires/feats.scp ]; then
  echo "$0: local/data/${train_set}_hires/feats.scp already exists."
  echo " ... Please either remove it, or rerun this script with stage > 2."
  exit 1
fi

if [ $stage -le 4 ]; then
  echo "$0: creating high-resolution MFCC features"

  # this shows how you can split across multiple file-systems.  we'll split the
  # MFCC dir across multiple locations.  You might want to be careful here, if you
  # have multiple copies of Kaldi checked out and run the same recipe, not to let
  # them overwrite each other.
  mfccdir=local/data/${train_set}_hires/data

  # do volume-perturbation on the training data prior to extracting hires
  # features; this helps make trained nnets more invariant to test data volume.
  utils/data/perturb_data_dir_volume.sh local/data/${train_set}_hires

  for datadir in ${train_set} test; do
    steps/make_mfcc_pitch.sh --nj $nj --mfcc-config conf/mfcc_hires.conf \
      --cmd "$train_cmd" local/data/${datadir}_hires
    steps/compute_cmvn_stats.sh local/data/${datadir}_hires
    utils/fix_data_dir.sh local/data/${datadir}_hires
  done
fi

if [ $stage -le 5 ]; then
  echo "$0: computing a subset of data to train the diagonal UBM."

  mkdir -p exp/nnet3${nnet3_affix}/diag_ubm
  temp_data_root=exp/nnet3${nnet3_affix}/diag_ubm

  # train a diagonal UBM using a subset of about a quarter of the data
  num_utts_total=$(wc -l <local/data/${train_set}_hires/utt2spk)
  num_utts=$[$num_utts_total/4]
  utils/data/subset_data_dir.sh local/data/${train_set}_hires \
    $num_utts ${temp_data_root}/${train_set}_hires_subset

  echo "$0: computing a PCA transform from the hires data."
  steps/online/nnet2/get_pca_transform.sh --cmd "$train_cmd" \
    --splice-opts "--left-context=3 --right-context=3" \
    --max-utts 10000 --subsample 2 \
    ${temp_data_root}/${train_set}_hires_subset \
    exp/nnet3${nnet3_affix}/pca_transform

  echo "$0: training the diagonal UBM."
  # Use 512 Gaussians in the UBM.
  steps/online/nnet2/train_diag_ubm.sh --cmd "$train_cmd" --nj 5 \
    --num-frames 700000 \
    --num-threads $num_threads_ubm \
    ${temp_data_root}/${train_set}_hires_subset 512 \
    exp/nnet3${nnet3_affix}/pca_transform exp/nnet3${nnet3_affix}/diag_ubm
fi

if [ $stage -le 6 ]; then
  # Train the iVector extractor. µUse all of the speed-perturbed data since iVector extractors
  # can be sensitive to the amount of data. The script defaults to an iVector dimension of 100.
  echo "$0: training the iVector extractor"
  steps/online/nnet2/train_ivector_extractor.sh --cmd "$train_cmd" --nj 1 \
    --num-threads 4 --num-processes 2 \
    --online-cmvn-iextractor $online_cmvn_iextractor \
    local/data/${train_set}_hires exp/nnet3${nnet3_affix}/diag_ubm \
    exp/nnet3${nnet3_affix}/extractor || exit 1;
fi

if [ $stage -le 7 ]; then
  echo "$0: On step 7"
  # note, we don't encode the 'max2' in the name of the ivectordir even though
  # that's the data we extract the ivectors from, as it's still going to be
  # valid for the non-'max2' data, the utterance list is the same.
  ivectordir=exp/nnet3${nnet3_affix}/ivectors_${train_set}_hires
  
  # We now extract iVectors on the speed-perturbed training data .  With
  # --utts-per-spk-max 2, the script pairs the utterances into twos, and treats
  # each of these pairs as one speaker; this gives more diversity in iVectors..
  # Note that these are extracted 'online' (they vary within the utterance).

  # Having a larger number of speakers is helpful for generalization, and to
  # handle per-utterance decoding well (the iVector starts at zero at the beginning
  # of each pseudo-speaker).
  temp_data_root=${ivectordir}
  utils/data/modify_speaker_info.sh --utts-per-spk-max 2 \
    local/data/${train_set}_hires ${temp_data_root}/${train_set}_hires_max2

  steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj $nj \
    ${temp_data_root}/${train_set}_hires_max2 \
    exp/nnet3${nnet3_affix}/extractor $ivectordir

  # Also extract iVectors for the test data, but in this case we don't need the speed
  # perturbation (sp) or small-segment concatenation (comb).
  for data in test; do
    steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj "$nj" \
      local/data/${data}_hires exp/nnet3${nnet3_affix}/extractor \
      exp/nnet3${nnet3_affix}/ivectors_${data}_hires
  done
fi

exit 0;
