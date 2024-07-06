import pandas as pd
import numpy as np
from konlpy.tag import Okt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import accuracy_score
import re
from collections import Counter
import pickle
from tqdm import tqdm

# 데이터 로드
train_data = pd.read_csv('ratings_train.txt', delimiter='\t')
test_data = pd.read_csv('ratings_test.txt', delimiter='\t')

# 전처리
train_data = train_data.drop_duplicates(subset=['document']).dropna(how='any')
train_data['document'] = train_data['document'].apply(lambda x: re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", x))
test_data = test_data.drop_duplicates(subset=['document']).dropna(how='any')
test_data['document'] = test_data['document'].apply(lambda x: re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", x))

okt = Okt()
stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

def tokenize(text):
    tokens = okt.morphs(text, stem=True)
    tokens = [word for word in tokens if not word in stopwords]
    return tokens

train_data['tokenized'] = train_data['document'].apply(tokenize)
test_data['tokenized'] = test_data['document'].apply(tokenize)

# 단어 사전 생성 및 저장
all_tokens = [token for sentence in train_data['tokenized'] for token in sentence]
vocab = Counter(all_tokens)
vocab_size = len(vocab) + 1
word_to_index = {word: i+1 for i, (word, _) in enumerate(vocab.most_common())}

with open('word_to_index.pkl', 'wb') as f:
    pickle.dump(word_to_index, f)

def tokens_to_sequences(tokens):
    return [word_to_index.get(token, 0) for token in tokens]

train_data['sequences'] = train_data['tokenized'].apply(tokens_to_sequences)
test_data['sequences'] = test_data['tokenized'].apply(tokens_to_sequences)

# 빈 시퀀스가 있는지 확인하고, 제거
train_data = train_data[train_data['sequences'].apply(len) > 0]
test_data = test_data[test_data['sequences'].apply(len) > 0]

# 패딩 함수 정의
def pad_sequences(sequences, maxlen=30):
    padded = np.zeros((len(sequences), maxlen), dtype=int)
    for i, seq in enumerate(sequences):
        if len(seq) > maxlen:
            padded[i] = np.array(seq[:maxlen])
        else:
            padded[i, -len(seq):] = np.array(seq)
    return padded

x_train = pad_sequences(train_data['sequences'])
x_test = pad_sequences(test_data['sequences'])
y_train = np.array(train_data['label'])
y_test = np.array(test_data['label'])

# PyTorch Dataset 정의
class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = torch.LongTensor(texts)
        self.labels = torch.FloatTensor(labels)
        
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.texts[idx], self.labels[idx]

train_dataset = TextDataset(x_train, y_train)
test_dataset = TextDataset(x_test, y_test)

# 데이터셋 크기 확인
print(f"Train dataset size: {len(train_dataset)}")
print(f"Test dataset size: {len(test_dataset)}")

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

# 모델 구축
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

embedding_dim = 100
hidden_dim = 128
output_dim = 1

# 학습률 설정
learning_rates = [0.0015, 0.001, 0.0005]

for lr in learning_rates:
    print(f"Training with learning rate: {lr}")
    
    model = SentimentLSTM(vocab_size, embedding_dim, hidden_dim, output_dim)
    model = model.to('cuda')

    # 손실 함수 및 옵티마이저 정의
    criterion = nn.BCELoss()
    optimizer = optim.RMSprop(model.parameters(), lr=lr)

    # 학습 손실 및 정확도 기록을 위한 리스트
    train_losses = []
    val_accuracies = []

    # 모델 학습 및 저장
    num_epochs = 5
    patience = 3
    best_acc = 0
    patience_counter = 0

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in tqdm(train_loader):
            optimizer.zero_grad()
            input_ids = batch[0].to('cuda')
            labels = batch[1].to('cuda')

            outputs = model(input_ids)
            loss = criterion(outputs.squeeze(), labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_train_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch + 1}, Loss: {avg_train_loss}")

        # 검증
        model.eval()
        total_val_loss = 0
        correct_predictions = 0
        with torch.no_grad():
            for batch in tqdm(test_loader):
                input_ids = batch[0].to('cuda')
                labels = batch[1].to('cuda')

                outputs = model(input_ids)
                loss = criterion(outputs.squeeze(), labels)
                total_val_loss += loss.item()

                preds = outputs.squeeze().round()
                correct_predictions += torch.sum(preds == labels)

        avg_val_loss = total_val_loss / len(test_loader)
        accuracy = correct_predictions.double() / len(test_loader.dataset)
        print(f"Validation Loss: {avg_val_loss}, Accuracy: {accuracy}")

        if accuracy > best_acc:
            best_acc = accuracy
            torch.save(model.state_dict(), f'final_best_model_lr_{lr}.pth')
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping")
                break

    print(f"Best Accuracy for learning rate {lr}: {best_acc}")

# word_to_index 저장
with open('word_to_index.pkl', 'wb') as f:
    pickle.dump(word_to_index, f)
