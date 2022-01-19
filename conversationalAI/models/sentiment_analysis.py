from transformers import BertModel, BertTokenizer
import torch
from torch import nn

import warnings
warnings.filterwarnings('ignore')


class SentimentClassifier(nn.Module):
    # define varabiables to be used
    PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
    tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    MAX_LEN = 160
    device = torch.device("cpu")
    class_names = ['negative', 'neutral', 'positive']

    # Initialize
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(SentimentClassifier.PRE_TRAINED_MODEL_NAME)
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    # Method to get sentiment based speech converted to text - STT
    def get_sentiment(sentiment):
        model = SentimentClassifier.load_sentiment_model()
        encoded_review = SentimentClassifier.tokenizer.encode_plus(
            sentiment,
            max_length=SentimentClassifier.MAX_LEN,
            add_special_tokens=True,
            return_token_type_ids=False,
            padding=True,
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True,
        )

        input_ids = encoded_review['input_ids'].to(SentimentClassifier.device)
        attention_mask = encoded_review['attention_mask'].to(SentimentClassifier.device)
        output = model(input_ids, attention_mask)
        _, prediction = torch.max(output, dim=1)

        return SentimentClassifier.class_names[prediction]

    # Method to load best_saved_model
    def load_sentiment_model(*args):
        model = SentimentClassifier(len(SentimentClassifier.class_names))
        model = model.to(SentimentClassifier.device)

        model.load_state_dict(torch.load('helpers/best_model_state.pt', map_location=torch.device('cpu')))
        return model