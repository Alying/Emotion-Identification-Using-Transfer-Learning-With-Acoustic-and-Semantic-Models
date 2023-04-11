
. ./path.sh || exit 1
. ./cmd.sh || exit 1

steps/make_mfcc.sh --nj 1 --cmd "$train_cmd" local/data/train local/data/logs local/data