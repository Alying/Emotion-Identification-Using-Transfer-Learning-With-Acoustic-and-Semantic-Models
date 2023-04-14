#!/usr/bin/env bash
# Used for downloading CremaD data

mkdir -p local/data
cd local/data   ### Note: the rest of this script is executed from the directory 'db'.

# CREMA-D database:
if [ ! -e CREMA-D ]; then
  echo "$0: cloning the CREMA-D data" 
  git lfs clone https://github.com/CheyneyComputerScience/CREMA-D.git
else
  echo "$0: not downloading or unzipping CREMA-D because it already exists."
fi

# IEMOCAP database:
if [ ! -e IEMOCAP_full_release ]; then
  echo "$0: downloading the IEMOCAP data (it won't re-download if it was already downloaded.)"
  tar -xf "IEMOCAP_full_release_withoutVideos.tar.gz"
else
  echo "$0: not downloading or unzipping IEMOCAP because it already exists."
fi

# Tedlium database:
if [ ! -e Tedlium.tar.gz ]; then
  echo "$0: downloading the Tedlium data (it won't re-download if it was already downloaded.)"
  gsutil cp -r gs://tedlium_with_pitch_model/pretrained_tedlium_dir.tar.gz Tedlium.tar.gz
  echo "unzipping Tedlium"
  tar -xvzf "Tedlium.tar.gz"
  echo "unzipped Tedlium"
  mv kaldi-trunk/egs/tedlium/s5_r3/exp/chain_cleaned_1d/tdnn1d_sp .
  echo "moved Tedlium"
else
  echo "$0: not downloading or unzipping Tedlium because it already exists."
fi

exit 0

