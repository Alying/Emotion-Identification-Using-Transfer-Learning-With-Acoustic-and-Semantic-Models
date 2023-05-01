model_dir=local/data/tdnn1d_sp
#dset=train
nj=10

# nnet3-copy --binary=false local/data/tdnn1d_sp/final.mdl local/data/tdnn1d_sp/final_text.mdl

for dset in test train:
do
	cp personal_utils/final_golden.mdl $model_dir/final_text.mdl
	nnet3-copy personal_utils/final_golden.mdl $model_dir/final.raw

	$decode_cmd JOB=1:$nj $model_dir/log/compute_output.JOB.log \
	nnet3-compute --online-ivectors=scp:exp/nnet3_cleaned/ivectors_train_hires/ivector_online.scp --online-ivector-period=10  \
	$model_dir/final.raw scp:local/data/${dset}_hires/feats.scp ark,scp:local/data/${dset}_hires/nnet_prediction.ark,local/data/${dset}_hires/nnet_prediction.scp
done

# . ./cmd.sh || exit 1

# egs_dir="local/data/train_hires/egs"
# nnet_dir="local/data/train_hires/nnet"
# # sid/nnet3/xvector/get_egs.sh --cmd "$train_cmd" \
# #     --nj 8 \
# #     --stage 0 \
# #     --frames-per-iter 1000000000 \
# #     --frames-per-iter-diagnostic 100000 \
# #     --min-frames-per-chunk 100 \
# #     --max-frames-per-chunk 300 \
# #     --num-diagnostic-archives 3 \
# #     --num-repeats 50 \
# #     "local/data/train_hires" $egs_dir

# #   echo "$0: creating neural net configs using the xconfig parser";
# #   num_targets=$(wc -w $egs_dir/pdf2num | awk '{print $1}')
# #   feat_dim=$(cat $egs_dir/info/feat_dim)
# #   echo $num_targets
# #   echo $feat_dim

#   # This chunk-size corresponds to the maximum number of frames the
#   # stats layer is able to pool over.  In this script, it corresponds
#   # to 100 seconds.  If the input recording is greater than 100 seconds,
#   # we will compute multiple xvectors from the same recording and average
#   # to produce the final xvector.
#   max_chunk_size=10000

#   # The smallest number of frames we're comfortable computing an xvector from.
#   # Note that the hard minimum is given by the left and right context of the
#   # frame-level layers.
#   min_chunk_size=25
# #   mkdir -p $nnet_dir/configs
# #   cat <<EOF > $nnet_dir/configs/network.xconfig
# #   # please note that it is important to have input layer with the name=input

# #   # The frame-level layers
# #   input dim=${feat_dim} name=input
# #   relu-batchnorm-layer name=tdnn1 input=Append(-2,-1,0,1,2) dim=512
# #   relu-batchnorm-layer name=tdnn2 input=Append(-2,0,2) dim=512
# #   relu-batchnorm-layer name=tdnn3 input=Append(-3,0,3) dim=512
# #   relu-batchnorm-layer name=tdnn4 dim=512
# #   relu-batchnorm-layer name=tdnn5 dim=1500

# #   # The stats pooling layer. Layers after this are segment-level.
# #   # In the config below, the first and last argument (0, and ${max_chunk_size})
# #   # means that we pool over an input segment starting at frame 0
# #   # and ending at frame ${max_chunk_size} or earlier.  The other arguments (1:1)
# #   # mean that no subsampling is performed.
# #   stats-layer name=stats config=mean+stddev(0:1:1:${max_chunk_size})

# #   # This is where we usually extract the embedding (aka xvector) from.
# #   relu-batchnorm-layer name=tdnn6 dim=512 input=stats

# #   # This is where another layer the embedding could be extracted
# #   # from, but usually the previous one works better.
# #   relu-batchnorm-layer name=tdnn7 dim=512
# #   output-layer name=output include-log-softmax=true dim=${num_targets}
# # EOF

# #  steps/nnet3/xconfig_to_configs.py \
#  #     --xconfig-file $nnet_dir/configs/network.xconfig \
#  #     --config-dir $nnet_dir/configs/
#  # cp $nnet_dir/configs/final.config $nnet_dir/nnet.config
#  # cp $nnet_dir/configs/ref.raw $nnet_dir/0.raw

#   # These three files will be used by sid/nnet3/xvector/extract_xvectors.sh
#    echo "output-node name=output input=tdnnf12.linear" > $nnet_dir/extract.config
#    echo "$max_chunk_size" > $nnet_dir/max_chunk_size
#    echo "$min_chunk_size" > $nnet_dir/min_chunk_size



# model_dir=exp/chain_cleaned_1d/tdnn1d_sp

# #cd local/data/kaldi-trunk/egs/tedlium/s5_r3/
# #nnet3-copy --nnet-config=$model_dir/configs/final.config $model_dir/final.mdl $model_dir/final.raw
# nnet3-copy --nnet-config=$nnet_dir/extract.config local/data/kaldi-trunk/egs/tedlium/s5_r3/$model_dir/final.mdl local/data/kaldi-trunk/egs/tedlium/s5_r3/$model_dir/final.raw

# cp local/data/kaldi-trunk/egs/tedlium/s5_r3/$model_dir/final.raw local/data/final.raw
# echo "$PWD"
# nnet3-xvector-compute local/data/final.raw scp:local/data/${dset}_hires/feats.scp ark,scp:local/data/${dset}_hires/nnet_prediction.ark,local/data/${dset}_hires/nnet_prediction.scp

