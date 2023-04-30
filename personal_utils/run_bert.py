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

id_to_dims_mapper = {}

# (3) BERT model
# get tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# load pre-trained model
model = BertModel.from_pretrained('bert-base-uncased',
                                   output_hidden_states=True,
                                   return_dict=False)
model.eval()

for DIR in ["train", "test"]:
    for key,mat in kaldi_io.read_mat_scp(f'local/data/{DIR}_hires/nnet_prediction.scp'):
        id_to_dims_mapper[key] = mat.shape[0]

    with open(f'local/data/{DIR}/text', 'r') as f:
        for line in f:
            # print(repr(line))

            split_point = line.index(" ")
            sentence_id = line[:split_point]
            sentence = line[split_point:].strip()

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

                    sentence_embedding = last_hidden_state.numpy()
                    sentence_embedding = sentence_embedding.mean(axis=0)
                    sentence_embedding = sentence_embedding.reshape(1,768)

                    sentence_to_embeddings_mapper[sentence] = sentence_embedding
                    id_to_embeddings_mapper[sentence_id] = np.repeat(sentence_embedding, repeats=id_to_dims_mapper[sentence_id], axis = 0)
            else:
                sentence_embedding = sentence_to_embeddings_mapper[sentence]
                id_to_embeddings_mapper[sentence_id] = np.repeat(sentence_embedding, repeats=id_to_dims_mapper[sentence_id], axis = 0)

    #print_dict(id_to_embeddings_mapper)

    # (4) convert to ark and scp files
    ark_file_length = 600 # features we want per ark file
    file_number = 0
    line_number = 0
    previous_file_number = 0
    ark_scp_output=f'ark:| copy-feats --compress=true ark:- ark,scp:local/data/{DIR}_hires/bert_embeddings{file_number}.ark,local/data/{DIR}_hires/bert_embeddings{file_number}.scp'
    f = kaldi_io.open_or_fd(ark_scp_output,'wb')

    #full_scp_output=f'ark:| copy-feats --compress=true ark:- ark,scp:local/data/{DIR}_hires/bert_embeddings.ark,local/data/{DIR}_hires/bert_embeddings.scp'
    #with kaldi_io.open_or_fd(full_scp_output,'wb') as f_final:
    for key,mat in id_to_embeddings_mapper.items():
        #print(key,":",mat)
        ark_scp_output=f'ark:| copy-feats --compress=true ark:- ark,scp:local/data/{DIR}_hires/bert_embeddings{file_number}.ark,local/data/{DIR}_hires/bert_embeddings{file_number}.scp'
        if previous_file_number != file_number:
            f.close()
            f = kaldi_io.open_or_fd(ark_scp_output,'wb')
            previous_file_number += 1
        kaldi_io.write_mat(f, mat, key=key)
        
        if line_number % ark_file_length == 0 and line_number != 0:
            file_number += 1
        line_number+=1
        
        #kaldi_io.write_mat(f_final, mat, key=key)
    f.close()


"""    list_of_files = []
    for i in range(file_number+1):
        list_of_files.append(f"local/data/{DIR}_hires/bert_embeddings{i}.scp")
    print(list_of_files)


    with open(f"local/data/{DIR}_hires/bert_embeddings.txt",'wb') as f_final:
        f_final.write("\n".join([open(i, 'wb') for i in list_of_files])) """
