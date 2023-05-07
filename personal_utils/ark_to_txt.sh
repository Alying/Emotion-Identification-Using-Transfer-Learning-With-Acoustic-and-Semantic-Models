# Author Daniel Mao
# Job: Converts all ark files to readable form in directory
# Input: Expects directory name
# Output: Creates readable ark files for all ark files in directory

dir=$1
for filename in $dir/*.ark; do
    rm ${filename}.txt
    touch ${filename}.txt
    copy-feats ark:${filename} ark,t:${filename}.txt
done