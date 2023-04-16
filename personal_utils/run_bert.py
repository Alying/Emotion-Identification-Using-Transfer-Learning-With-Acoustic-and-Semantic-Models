import torch
from transformers import BertTokenizer, BertModel
import logging
import matplotlib.pyplot as plt

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
