import transformers
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import torch
import os
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from collections import defaultdict
from textwrap import wrap

from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F

import warnings
warnings.filterwarnings('ignore')


class SentimentClassifier(nn.Module):
    # define varabiables to be used
    PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
    tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    MAX_LEN = 160
    device = torch.device("cpu")
    class_names = ['negative', 'neutral', 'positive']


    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(SentimentClassifier.PRE_TRAINED_MODEL_NAME)
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)


    def forward(self, input_ids, attention_mask):
        returned = self.bert(input_ids=input_ids, attention_mask=attention_mask)

        pooled_output = returned["pooler_output"]
        output = self.drop(pooled_output)

        return self.out(output)

    # Method to load best_saved_model
    def load_sentiment_model(*args):
        model = SentimentClassifier(len(SentimentClassifier.class_names))
        model = model.to(SentimentClassifier.device)

        model.load_state_dict(torch.load('helpers/best_model_state.pt', map_location=torch.device('cpu')))
        return model