# Author Eleanor Chodroff (Copied from online)
# See https://eleanorchodroff.com/tutorial/kaldi/forced-alignment.html
# Job: Split all the files in final_ali.txt into files based on utterance.
#      This is mainly a convenience method for align_nnet.py
# Input: Expects to see exp/tri3_train_ali/final_ali.txt as well as for test
# Output: Creates local/data/train_temp and also for test

import sys,csv,glob, os,os.path,re,codecs
results=[]


for dset in ["train", "test"]:
    try:
        with open(f"exp/tri3_{dset}_ali/final_ali.txt") as f:
            next(f) #skip header
            index = 0
            for line in f:
                columns=line.split("\t")
                if index == 0:
                    name = columns[1]
                    print(name)
                index = index + 1
                
                name_prev = name
                name = columns[1]
                if (name_prev != name):
                    try:
                        with open(f"local/data/{dset}_temp/" + (name_prev)+".txt",'w') as fwrite:
                            # print(name_prev)
                            writer = csv.writer(fwrite)
                            fwrite.write("\n".join(results))
                            fwrite.close()
                            # print(name)
                    except:
                        print("Failed to write file")
                        sys.exit(2)
                    del results[:]
                    results.append(line[0:-1])
                else:
                    results.append(line[0:-1])
    except:
        print("Failed to read file")
        sys.exit(1)
    # this prints out the last textfile (nothing following it to compare with)
    try:
        with open(f"local/data/{dset}_temp/" + (name_prev)+".txt",'w') as fwrite:
            writer = csv.writer(fwrite)
            fwrite.write("\n".join(results))
            fwrite.close()
            # print(name)
    except:
        print("Failed to write file")
        sys.exit(2)

print("DONE")
