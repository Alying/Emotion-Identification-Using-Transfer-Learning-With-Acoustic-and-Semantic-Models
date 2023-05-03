#!/bin/sh

#  id2phone.R
#  
#
#  Created by Eleanor Chodroff on 3/24/15.
#

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