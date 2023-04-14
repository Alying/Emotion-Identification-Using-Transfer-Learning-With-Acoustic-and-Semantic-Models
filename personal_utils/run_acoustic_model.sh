 model_dir=local/data/tdnn1d_sp
 dset=train
 nj=10

 $decode_cmd JOB=1:$nj $model_dir/log/compute_output.JOB.log \
 nnet3-compute --online-ivectors=scp:exp/nnet3_cleaned/ivectors_${dset}_hires/ivector_online.scp --online-ivector-period=10  \
 $model_dir/final.mdl scp:local/data/${dset}_hires/feats.scp ark,scp:local/data/${dset}_hires/nnet_prediction.ark,local/data/${dset}_hires/nnet_prediction.scp