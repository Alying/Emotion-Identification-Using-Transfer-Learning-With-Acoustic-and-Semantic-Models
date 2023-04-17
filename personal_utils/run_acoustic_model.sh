model_dir=local/data/tdnn1d_sp
dset=train
nj=10

# nnet3-copy --binary=false local/data/tdnn1d_sp/final.mdl local/data/tdnn1d_sp/final_text.mdl

cp personal_utils/final_golden.mdl $model_dir/final_text.mdl

$decode_cmd JOB=1:$nj $model_dir/log/compute_output.JOB.log \
nnet3-compute --online-ivectors=scp:exp/nnet3_cleaned/ivectors_${dset}_hires/ivector_online.scp --online-ivector-period=10  \
$model_dir/final_text.mdl scp:local/data/${dset}_hires/feats.scp ark,scp:local/data/${dset}_hires/nnet_prediction.ark,local/data/${dset}_hires/nnet_prediction.scp