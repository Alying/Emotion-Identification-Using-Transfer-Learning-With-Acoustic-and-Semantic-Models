#!/usr/bin/env bash

# Main emotion identification script.

./path.sh

stage=0

# Data preparation
if [ $stage -le 0 ]; then
  utils/download_data.sh
fi

