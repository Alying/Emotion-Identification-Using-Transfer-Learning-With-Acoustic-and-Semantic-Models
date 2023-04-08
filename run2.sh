
. ./path.sh || exit 1
. ./cmd.sh || exit 1

utils/utt2spk_to_spk2utt.pl local/data/train/utt2spk > local/data/train/spk2utt
steps/make_mfcc.sh --nj 1 --cmd "$train_cmd" local/data/train local/data/logs local/data