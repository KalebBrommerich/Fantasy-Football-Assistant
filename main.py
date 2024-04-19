import joblib
import pandas as pd
from data_preparation import load_data, create_sequences
from dataset import PlayerStatsDataset
from model import RNNModel
from train import train_model
from torch.utils.data import DataLoader
import numpy as np
import torch

data_val = load_data('combined_passing_2018_2023.csv')
data = load_data('combined_passing_2012_2017.csv')
input_size = [col for col in data.columns if col not in ['Fantasy_Points', 'Player', 'Year']].__len__()

def main():
    X, y = create_sequences(data, 2,'Fantasy_Points')
    #X_val, y_val = create_sequences(data_val, 2, 'Fantasy_Points')
    model = RNNModel(input_size, hidden_dim=50, num_layers=2, dropout_prob=0.3)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    train_loader = DataLoader(PlayerStatsDataset(X, y), batch_size=32, shuffle=True)
    #val_loader = DataLoader(PlayerStatsDataset(X_val, y_val), batch_size=32, shuffle=False)
    train_model(model, train_loader, criterion, optimizer, num_epochs=20)
    torch.save(model.state_dict(), 'model.pth')

    model_path = 'model.pth'
    feature_scaler_path = 'feature_scaler.pkl'
    target_scaler_path = 'target_scaler.pkl'
    dataset_path = 'combined_passing_2018_2023.csv'
    player_name = 'Josh Allen'
    seq_length = 2
    model, feature_scaler, target_scaler = load_model_and_scalers(model_path, feature_scaler_path, target_scaler_path)
    predicted_output = predict(model, feature_scaler, target_scaler, dataset_path, player_name, seq_length)
    print("Predicted Output:", predicted_output)
# Make a prediction

def load_model_and_scalers(model_path, feature_scaler_path, target_scaler_path):
    # Load the trained model
    model = RNNModel(input_size, hidden_dim=50, num_layers=2, dropout_prob=0.3)
    model.load_state_dict(torch.load(model_path))
    model.eval()  # Set model to evaluation mode

    # Load scalers
    feature_scaler = joblib.load(feature_scaler_path)
    target_scaler = joblib.load(target_scaler_path)
    
    return model, feature_scaler, target_scaler

def predict(model, feature_scaler, target_scaler, dataset_path, player_name, seq_length):
    # Load and prepare the dataset
    data = pd.read_csv(dataset_path)
    data = data[data['Player'] == player_name]
    if data.empty:
        return "No data available for player: {}".format(player_name)

    feature_columns = [col for col in data.columns if col not in ['Fantasy_Points', 'Player', 'Year']]
    data[feature_columns] = feature_scaler.transform(data[feature_columns])

    # Create sequences
    X = []
    for i in range(len(data) - seq_length + 1):
        X.append(data[feature_columns].iloc[i:i + seq_length].values)

    # Convert to numpy array and make a tensor
    X = np.array(X)
    input_tensor = torch.tensor(X, dtype=torch.float32)

    # Make prediction
    with torch.no_grad():
        output = model(input_tensor)

    # Inverse scale the prediction
    prediction_scaled = output.numpy()
    prediction = target_scaler.inverse_transform(prediction_scaled.reshape(-1, 1))
    
    return prediction.flatten()



    

if __name__ == '__main__':
    main()
