import joblib
import pandas as pd
from data_preparation import load_data, create_sequences
from dataset import PlayerStatsDataset
from model import RNNModel
from train import ModelTrainer
from torch.utils.data import DataLoader
import numpy as np
import torch

"""
class is used for testing and training models, contains prediction function, and model loading functions

also contains create rankings, this function painfully builds dataframes which contain the rankings and outputs a csv 
"""


#test main 
def main():
    #print("Pasing")                                                    #model training lines
    #create_and_train('TrainingData/combined_passing_2006_2017.csv')
    #print("Rushing")
    #create_and_train('TrainingData/combined_rushing_2006_2017.csv')
    #print("Receiving")
    #create_and_train('TrainingData/combined_receiving_2006_2017.csv')
    
    # model_path = 'Models/receiving_model.pth'                         #test prediction setup
    # feature_scaler_path = 'Models/receiving_feature_scaler.pkl'
    # target_scaler_path = 'Models/receiving_target_scaler.pkl'
    # dataset_path = 'TrainingData/combined_receiving_2018_2023.csv'
    # player_name = 'Davante Adams'
    # seq_length = 2
    # model, feature_scaler, target_scaler = load_model_and_scalers(model_path, feature_scaler_path, target_scaler_path)
    # predicted_output = predict(model, feature_scaler, target_scaler, dataset_path, player_name, seq_length)
    # print("Predicted Output:", predicted_output)
    pass

def load_model_and_scalers(model_path, feature_scaler_path, target_scaler_path):
    if "passing" in model_path:
        input_size = 25
    elif "rushing" in model_path:
        input_size = 12
    elif "receiving" in model_path:
        input_size = 16
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

def create_and_train(filepath):
    data = load_data(filepath)
    input_size = [col for col in data.columns if col not in ['Fantasy_Points', 'Player', 'Year']].__len__()
    X, y = create_sequences(data, 2,'Fantasy_Points', filepath)
    model = RNNModel(input_size, hidden_dim=50, num_layers=2, dropout_prob=0.3)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    train_loader = DataLoader(PlayerStatsDataset(X, y), batch_size=32, shuffle=True)
    ModelTrainer.train_model(model, train_loader, criterion, optimizer, max_epochs=50)
    if "passing" in filepath:
        torch.save(model.state_dict(), 'Models/passing_model.pth')
    elif "rushing" in filepath:
        torch.save(model.state_dict(), 'Models/rushing_model.pth')
    elif "receiving" in filepath:
        torch.save(model.state_dict(), 'Models/receiving_model.pth')

def create_ranking():
    # Load models and scalers
    passing_model, passing_feature_scaler, passing_target_scaler = load_model_and_scalers(
        file_path_model[0], file_path_feature_scaler[0], file_path_target_scaler[0]
    )
    rushing_model, rushing_feature_scaler, rushing_target_scaler = load_model_and_scalers(
        file_path_model[1], file_path_feature_scaler[1], file_path_target_scaler[1]
    )
    receiving_model, receiving_feature_scaler, receiving_target_scaler = load_model_and_scalers(
        file_path_model[2], file_path_feature_scaler[2], file_path_target_scaler[2]
    )

    # Load datasets
    passing_data = pd.read_csv(file_path_predict[0])
    rushing_data = pd.read_csv(file_path_predict[1])
    receiving_data = pd.read_csv(file_path_predict[2])

    # Generate predictions for passing
    passing_predictions = pd.DataFrame({
        "Quarterbacks": passing_data["Player"].unique(),
        "Position": ["Passing"] * len(passing_data["Player"].unique()),
        "PredictionPass": [
            predict(
                passing_model,
                passing_feature_scaler,
                passing_target_scaler,
                file_path_predict[0],
                player,
                seq_length=2
            )[0]
            for player in passing_data["Player"].unique()
        ],
    })

    # Generate predictions for rushing
    rushing_predictions = pd.DataFrame({
        "Running Backs": rushing_data["Player"].unique(),
        "Position": ["Rushing"] * len(rushing_data["Player"].unique()),
        "PredictionRush": [
            predict(
                rushing_model,
                rushing_feature_scaler,
                rushing_target_scaler,
                file_path_predict[1],
                player,
                seq_length=2
            )[0]
            for player in rushing_data["Player"].unique()
        ],
    })

    # Generate predictions for receiving
    receiving_predictions = pd.DataFrame({
        "Receivers": receiving_data["Player"].unique(),
        "Position": ["Receiving"] * len(receiving_data["Player"].unique()),
        "PredictionRec": [
            predict(
                receiving_model,
                receiving_feature_scaler,
                receiving_target_scaler,
                file_path_predict[2],
                player,
                seq_length=2
            )[0]
            for player in receiving_data["Player"].unique()
        ],
    })
    
    max_length = max(len(passing_predictions), len(rushing_predictions), len(receiving_predictions))
    passing_predictions = passing_predictions.reindex(range(max_length))
    passing_predictions = passing_predictions.sort_values(by='PredictionPass', ascending=False, ignore_index=True)
    passing_predictions = passing_predictions.drop(columns='Position')

    rushing_predictions = rushing_predictions.reindex(range(max_length))
    rushing_predictions = rushing_predictions.sort_values(by='PredictionRush', ascending=False, ignore_index=True)
    rushing_predictions = rushing_predictions.drop(columns='Position')

    receiving_predictions = receiving_predictions.reindex(range(max_length))
    receiving_predictions = receiving_predictions.sort_values(by='PredictionRec', ascending=False, ignore_index=True)
    receiving_predictions = receiving_predictions.drop(columns='Position')
    
    
    ranking_df = pd.concat([passing_predictions, rushing_predictions, receiving_predictions], axis=1)

    ranking_df.to_csv("gen_rankings.csv", index=False)

    return ranking_df
   
file_path_predict = ['TrainingData/combined_passing_2018_2023.csv','TrainingData/combined_rushing_2018_2023.csv','TrainingData/combined_receiving_2018_2023.csv']
file_path_model = ['Models/passing_model.pth','Models/rushing_model.pth','Models/receiving_model.pth']
file_path_feature_scaler = ['Models/passing_feature_scaler.pkl','Models/rushing_feature_scaler.pkl','Models/receiving_feature_scaler.pkl']
file_path_target_scaler = ['Models/passing_target_scaler.pkl','Models/rushing_target_scaler.pkl','Models/receiving_target_scaler.pkl']

if __name__ == '__main__':
    main()
