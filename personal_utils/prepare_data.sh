cd local

for set in test train; do
  dir=data/$set
  if [ ! -e $dir ]; then
    mkdir -p $dir
  fi
done

cd ../utils

python3 split_data.py