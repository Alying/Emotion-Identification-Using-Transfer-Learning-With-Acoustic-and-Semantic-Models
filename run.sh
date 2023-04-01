#!/usr/bin/env bash

# Main emotion identification script.

./path.sh

stage=0

# Data preparation
if [ $stage -le 0 ]; then
  utils/download_data.sh
fi

if [ $stage -le 1 ]; then
  utils/prepare_data.sh
fi

if [ $stage -le 2 ]; then
  utils/make_mfcc.sh
fi
