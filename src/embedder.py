import pandas as pd

import torch
from transformers import AutoTokenizer, AutoModel


device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")
model = AutoModel.from_pretrained("cointegrated/LaBSE-en-ru").to(device)

def make_single_embs(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt').to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.pooler_output
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].tolist()

