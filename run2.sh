
. ./path.sh || exit 1
. ./cmd.sh || exit 1

steps/make_mfcc_pitch.sh --nj 1 --cmd "$train_cmd" local/data/train local/data/logs local/data
steps/make_mfcc_pitch.sh --nj 30 --cmd "$train_cmd" local/data/train
steps/compute_cmvn_stats.sh local/data/train