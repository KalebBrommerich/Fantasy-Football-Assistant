import torch
from torch import nn

class RNNModel(nn.Module):
    def __init__(self, input_size, hidden_dim, num_layers, dropout_prob=0.2):
        super(RNNModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_dim, num_layers, batch_first=True, dropout=dropout_prob)
        self.dropout = nn.Dropout(dropout_prob)
        self.fc = nn.Linear(hidden_dim, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.dropout(out[:, -1, :])
        out = self.fc(out)
        out = self.relu(out)
        return out
