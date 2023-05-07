# Author Eleanor Chodroff (Copied from online)
# See https://eleanorchodroff.com/tutorial/kaldi/forced-alignment.html
# Job: Convert phone ID's into phone symbols
# Input: Expects to see exp/tri3_train_ali/merged_alignment.txt, 
#                                         /phones.txt
#                       local/data/train/segments
#        And all the corresponding files under test
# Output: Creates exp/tri3_train_ali/final_ali.txt as well for test

for (dset in list("train", "test")) {
    phones <- read.table(sprintf("exp/tri3_%s_ali/phones.txt", dset), quote="\"")
    segments <- read.table(sprintf("local/data/%s/segments", dset), quote="\"")
    ctm <- read.table(sprintf("exp/tri3_%s_ali/merged_alignment.txt", dset), quote="\"")


    names(ctm) <- c("file_utt","utt","start","dur","id")
    ctm$file <- gsub("_[0-9]*$","",ctm$file_utt)
    names(phones) <- c("phone","id")
    names(segments) <- c("file_utt","file","start_utt","end_utt")

    ctm2 <- merge(ctm, phones, by="id")
    ctm3 <- merge(ctm2, segments, by=c("file_utt","file"))
    ctm3$start_real <- ctm3$start + ctm3$start_utt
    ctm3$end_real <- ctm3$start_utt + ctm3$dur

    write.table(ctm3, sprintf("exp/tri3_%s_ali/final_ali.txt", dset), row.names=F, quote=F, sep="\t")
}