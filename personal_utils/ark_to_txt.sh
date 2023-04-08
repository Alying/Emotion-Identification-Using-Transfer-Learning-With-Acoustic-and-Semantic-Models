dir=$1
for filename in $dir/*.ark; do
    rm ${filename}.txt
    touch ${filename}.txt
    copy-feats ark:${filename} ark,t:${filename}.txt
done