import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

def create_sequences(data, seq_length, target_column):
    feature_columns = [col for col in data.columns if col not in [target_column, 'Player', 'Year']]
    X, y = [], []
    scaler = StandardScaler()
    target_scaler = MinMaxScaler(feature_range=(0, 1))
    
    # Process each player's data separately
    for player, group in data.groupby('Player'):
        group = group.sort_values(by='Year')  # Ensure the data is in chronological order
        group[feature_columns] = scaler.fit_transform(group[feature_columns])  # Scale data per player
        group[target_column] = target_scaler.fit_transform(group[[target_column]])
        
        
        group_values = group[feature_columns].values
        group_labels = group[target_column].values
        
        for i in range(len(group) - seq_length):
            X.append(group_values[i:(i + seq_length)])
            y.append(group_labels[i + seq_length])
    joblib.dump(scaler, 'feature_scaler.pkl')  # Saves the feature scaler
    joblib.dump(target_scaler, 'target_scaler.pkl')  # Saves the target scaler        

    return np.array(X), np.array(y)

