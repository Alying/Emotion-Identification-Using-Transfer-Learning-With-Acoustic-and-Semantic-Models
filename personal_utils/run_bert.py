import torch
from transformers import BertTokenizer, BertModel
import logging
import numpy as np
import kaldi_io

def print_dict(d):
   for key,value in d.items():
       print(key," : ",value)

# (1) sentence to embeddings dictionary
sentence_to_embeddings_mapper = {}

# (2) id to embeddings dictionary
id_to_embeddings_mapper = {}

# (3) BERT model
# get tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# load pre-trained model
model = BertModel.from_pretrained('bert-base-uncased',
                                   output_hidden_states=True,
                                   return_dict=False)
model.eval()

with open('local/data/test/text', 'r') as f:
    for line in f:
        print(repr(line))
        line_arr = line.split("                  ")
        sentence_id = line_arr[0]
        sentence = line_arr[1]
        if sentence not in sentence_to_embeddings_mapper:
            marked_text = "[CLS] " + sentence + " [SEP]"

            # Tokenize our sentence with the BERT tokenizer; split sentence into tokens
            tokenized_text = tokenizer.tokenize(marked_text)
            print(tokenized_text)

            # Map the token strings to their vocabulary indeces
            indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

            # Assign all tokens belonging to one sentence with a sentence id
            segment_ids = [1]*len(tokenized_text)

            # Convert inputs to Pytorch tensors
            tokens_tensor = torch.tensor([indexed_tokens])
            segments_tensors = torch.tensor([segment_ids])

            with torch.no_grad():
                outputs = model(tokens_tensor, segments_tensors)
                #print(type(outputs))
                #print(np.shape(outputs))
                #print(outputs)

                last_hidden_state = outputs[0][0]
                #print(type(last_hidden_state))
                #print(len(last_hidden_state))
                #print(last_hidden_state.shape)
                #print(last_hidden_state)

                sentence_embedding = last_hidden_state.numpy()
                sentence_embedding = sentence_embedding.mean(axis=0)
                sentence_embedding = sentence_embedding.reshape(1,768)
                #sentence_embedding = list(sentence_embedding)
                #print(sentence_embedding)

                sentence_to_embeddings_mapper[sentence] = sentence_embedding
                id_to_embeddings_mapper[sentence_id] = sentence_embedding
        else:
            sentence_embedding = sentence_to_embeddings_mapper[sentence]
            id_to_embeddings_mapper[sentence_id] = sentence_embedding

#print_dict(id_to_embeddings_mapper)

ark_scp_output='ark:| copy-feats --compress=true ark:- ark,scp:local/data/test_hires/bert_embeddings.ark,local/data/test_hires/bert_embeddings.scp'
with kaldi_io.open_or_fd(ark_scp_output,'wb') as f:
  for key,mat in id_to_embeddings_mapper.items():
      print(key,":",mat)
      kaldi_io.write_mat(f, mat, key=key)
