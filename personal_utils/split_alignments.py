#  split_alignments.py
#  
#
#  Created by Eleanor Chodroff on 3/25/15.
#
#
#

import sys,csv
results=[]

#name = name of first text file in final_ali.txt
#name_fin = name of final text file in final_ali.txt

name = "110236_20091006_82330_F"
name_fin = "120958_20100126_97016_M"
try:
    with open("final_ali.txt") as f:
        next(f) #skip header
        for line in f:
            columns=line.split("\t")
            name_prev = name
            name = columns[1]
            if (name_prev != name):
                try:
                    with open((name_prev)+".txt",'w') as fwrite:
                        writer = csv.writer(fwrite)
                        fwrite.write("\n".join(results))
                        fwrite.close()
                #print name
                except e:
                    print("Failed to write file")
                    sys.exit(2)
                del results[:]
                results.append(line[0:-1])
            else:
                results.append(line[0:-1])
except e:
    print("Failed to read file")
    sys.exit(1)
# this prints out the last textfile (nothing following it to compare with)
try:
    with open((name_prev)+".txt",'w') as fwrite:
        writer = csv.writer(fwrite)
        fwrite.write("\n".join(results))
        fwrite.close()
                #print name
except e:
    print("Failed to write file")
    sys.exit(2)