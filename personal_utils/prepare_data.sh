# Author Alina Ying
# Job: Runs prepare_data.py
# Input: Expects the local/data/CREMA-D/
# Output: Creates text, segments, utt2spk, wav.scp in local/data/train and test

cd local

for set in test train; do
  dir=data/$set
  if [ ! -e $dir ]; then
    mkdir -p $dir
  fi
done

cd ../personal_utils

python3 prepare_data.py