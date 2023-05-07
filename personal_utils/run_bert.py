# Author Alina Ying
# Job: Creates textual embeddings for each word in the utterance
# Input: Expects text file in local/data/train and test
# Output: Creates bert_embeddings.scp+ark in local/data/train_hires and test

import torch
from transformers import BertTokenizer, BertModel
import logging
import numpy as np
import kaldi_io

def print_dict(d):
   for key,value in d.items():
       print(key," : ",value)

# (3) BERT model
# get tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# load pre-trained model
model = BertModel.from_pretrained('bert-base-uncased',
                                   output_hidden_states=True,
                                   return_dict=False)
model.eval()

for DIR in ["train", "test"]:
    # (1) sentence to embeddings dictionary
    sentence_to_embeddings_mapper = {}

    # (2) id to embeddings dictionary
    id_to_embeddings_mapper = {}

    with open(f'local/data/{DIR}/text', 'r') as f:
        for line in f:
            # print(repr(line))
            line = line.strip()
            split_point = line.index(" ")
            sentence_id = line[:split_point]
            sentence = line[split_point:].strip()
            sentence = sentence.rstrip(sentence[-1])

            if sentence not in sentence_to_embeddings_mapper:
                marked_text = "[CLS] " + sentence + " [SEP]"

                # Tokenize our sentence with the BERT tokenizer; split sentence into tokens
                tokenized_text = tokenizer.tokenize(marked_text)
                # print(tokenized_text)

                # Map the token strings to their vocabulary indeces
                indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

                # Assign all tokens belonging to one sentence with a sentence id
                segment_ids = [1]*len(tokenized_text)

                # Convert inputs to Pytorch tensors
                tokens_tensor = torch.tensor([indexed_tokens])
                segments_tensors = torch.tensor([segment_ids])

                with torch.no_grad():
                    outputs = model(tokens_tensor, segments_tensors)

                    last_hidden_state = outputs[0][0]

                slice_index = 1
                for i, word in enumerate(sentence.split(' ')):
                    length = len(tokenizer.tokenize(word))
                    if i == 0:
                        sentence_embedding = last_hidden_state.numpy()[slice_index : slice_index + length, : ].mean(0)
                    else:
                        sentence_embedding = np.vstack((sentence_embedding, last_hidden_state.numpy()[slice_index : slice_index + length, : ].mean(0)))
                    slice_index = slice_index+length

                sentence_to_embeddings_mapper[sentence] = sentence_embedding
                id_to_embeddings_mapper[sentence_id] = sentence_embedding
            else:
                sentence_embedding = sentence_to_embeddings_mapper[sentence]
                id_to_embeddings_mapper[sentence_id] = sentence_embedding

    print(len(id_to_embeddings_mapper.items()))

    ark_scp_output=f'ark:| copy-feats --compress=true ark:- ark,scp:local/data/{DIR}_hires/bert_embeddings.ark,local/data/{DIR}_hires/bert_embeddings.scp'
    f = kaldi_io.open_or_fd(ark_scp_output,'wb')

    for key,mat in id_to_embeddings_mapper.items():
        #print(mat.shape)
        kaldi_io.write_mat(f, mat, key=key)
        
    f.close()
    # (4) convert to ark and scp files
    # ark_file_length = 1000 # features we want per ark file
    # file_number = 0
    # line_number = 0
    # previous_file_number = 0
    # ark_scp_output=f'ark:| copy-feats --compress=true ark:- ark,scp:local/data/{DIR}_hires/bert_embeddings{file_number}.ark,local/data/{DIR}_hires/bert_embeddings{file_number}.scp'
    # f = kaldi_io.open_or_fd(ark_scp_output,'wb')

    # for key,mat in id_to_embeddings_mapper.items():
    #     #print(key,":",mat)
    #     ark_scp_output=f'ark:| copy-feats --compress=true ark:- ark,scp:local/data/{DIR}_hires/bert_embeddings{file_number}.ark,local/data/{DIR}_hires/bert_embeddings{file_number}.scp'
    #     if previous_file_number != file_number:
    #         f.close()
    #         f = kaldi_io.open_or_fd(ark_scp_output,'wb')
    #         previous_file_number += 1
    #     kaldi_io.write_mat(f, mat, key=key)
        
    #     if line_number % ark_file_length == 0 and line_number != 0:
    #         file_number += 1
    #     line_number+=1
    # f.close()


