import torch
import torch.nn as nn
import re
from konlpy.tag import Okt
import numpy as np
import pickle

# 모델 구조 정의 (저장된 모델과 동일하게)
class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SentimentLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        lstm_out = lstm_out[:, -1, :]
        out = self.fc(lstm_out)
        return self.sigmoid(out)

# 단어 사전 로드
with open('word_to_index.pkl', 'rb') as f:
    word_to_index = pickle.load(f)

vocab_size = len(word_to_index) + 1
embedding_dim = 100
hidden_dim = 128
output_dim = 1

# 모델 로드
model = SentimentLSTM(vocab_size, embedding_dim, hidden_dim, output_dim)
model.load_state_dict(torch.load('final_best_model.pth'))
model = model.to('cuda')
model.eval()  # 평가 모드로 전환

# 전처리 함수 정의
okt = Okt()
stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

def tokenize(text):
    tokens = okt.morphs(text, stem=True)
    tokens = [word for word in tokens if not word in stopwords]
    return tokens

def tokens_to_sequences(tokens):
    return [word_to_index.get(token, 0) for token in tokens]

def pad_sequences(sequences, maxlen=30):
    padded = np.zeros((len(sequences), maxlen), dtype=int)
    for i, seq in enumerate(sequences):
        if len(seq) > maxlen:
            padded[i] = np.array(seq[:maxlen])
        else:
            padded[i, -len(seq):] = np.array(seq)
    return padded

def preprocess_input(text):
    text = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)
    tokens = tokenize(text)
    sequence = tokens_to_sequences(tokens)
    padded_sequence = pad_sequences([sequence])
    return torch.LongTensor(padded_sequence).to('cuda')

# 예측 함수 정의
def predict_sentiment(text, model):
    input_tensor = preprocess_input(text)
    with torch.no_grad():
        output = model(input_tensor)
        prediction = output.squeeze().item()
        return prediction

# 입력 텍스트에 대한 예측
sample_texts = ["삼류영화", "유명한 감독이라 기대했는데 아쉽네요"]
for sample_text in sample_texts:
    prediction = predict_sentiment(sample_text, model)
    print(f'입력 문장: "{sample_text}"')
    print(f'긍정 확률: {prediction:.4f}')
    print(f'예측 결과: {"긍정" if prediction >= 0.5 else "부정"}')
