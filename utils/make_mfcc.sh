mfcc_config=conf/mfcc.conf

if [ -f path.sh ]; then . ./path.sh; fi

compute-mfcc-feats --verbose=2 --config=$mfcc_config ark:- ark:-
