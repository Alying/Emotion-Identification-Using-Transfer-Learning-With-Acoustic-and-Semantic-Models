#!/usr/bin/env bash

# Main emotion identification script.

stage=0

# Data preparation
if [ $stage -le 0 ]; then
  download_data.sh
fi

