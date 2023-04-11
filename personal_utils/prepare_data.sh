cd local

for set in test train; do
  dir=data/$set
  if [ ! -e $dir ]; then
    mkdir -p $dir
  fi
done

cd ../personal_utils

python3 prepare_data.py