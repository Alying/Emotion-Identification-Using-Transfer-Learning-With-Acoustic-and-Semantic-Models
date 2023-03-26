#!/usr/bin/env bash
# Used for downloading CremaD data

mkdir -p local/data
cd local/data   ### Note: the rest of this script is executed from the directory 'db'.

debug_mode=true

# TED-LIUM database:
if [ ! -e CREMA-D ]; then
  echo "$0: cloning the CREMA-D data (it won't re-download if it was already downloaded.)"
  # the following command won't re-get it if it's already there
  # because of the --continue switch.
 
  if $debug_mode; then
  	mkdir -p CREMA-D
	wget --continue https://github.com/CheyneyComputerScience/CREMA-D/archive/refs/heads/master.zip || exit 1
  	unzip master.zip -d CREMA-D 
  else
     	git lfs clone https://github.com/CheyneyComputerScience/CREMA-D.git
  fi
else
  echo "$0: not downloading or unzipping CREMA-D because it already exists."
fi

exit 0

