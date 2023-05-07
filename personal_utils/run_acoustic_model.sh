# Author Daniel Mao
# Job: Creates necessary prereq files for Kaldi's lda algorithm to run
# Input: Expects to see combined.scp+ark in local/data/train_hires and test_hires
# Output: Creates lda_feats.scp+ark and utt2spk2 files in train_hires and test_hires

model_dir=local/data/tdnn1d_sp
#dset=train
nj=10

sudo touch $model_dir/extract.config
sudo chmod 777 $model_dir/extract.config
echo "output-node name=output input=tdnnf12.noop" > $model_dir/extract.config
nnet3-copy --binary=false --nnet-config=$model_dir/extract.config $model_dir/final.mdl $model_dir/final2.raw

for dset in test train
do
	$decode_cmd JOB=1:$nj $model_dir/log/compute_output.JOB.log \
	nnet3-compute --online-ivectors=scp:exp/nnet3_cleaned/ivectors_${dset}_hires/ivector_online.scp --online-ivector-period=10  \
	$model_dir/final2.raw scp:local/data/${dset}_hires/feats.scp ark,scp:local/data/${dset}_hires/nnet_prediction.ark,local/data/${dset}_hires/nnet_prediction.scp
done
