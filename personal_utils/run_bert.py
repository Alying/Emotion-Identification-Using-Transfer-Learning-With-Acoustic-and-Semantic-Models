import torch
from transformers import BertTokenizer, BertModel
import logging
import matplotlib.pyplot as plt

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Load pre-trained model
model = BertModel.from_pretrained('bert-base-uncased',
                                   output_hidden_states=True)
model.eval()

with open('local/data/test/text', 'r') as f:
    for line in f:
        print(repr(line))
        marked_text = "[CLS] " + line + " [SEP]"

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
            # print(outputs)
