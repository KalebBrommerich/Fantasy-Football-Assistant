import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, MinMaxScaler

"""
data_preparation file
This file is used to make the data usable by the prediction model. 
Identifies feature columns, establishes and saves scalers, and creates sequences for the model.
"""

def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

def create_sequences(data, seq_length, target_column,filepath): #seq length should always be 2??? 
    feature_columns = [col for col in data.columns if col not in [target_column, 'Player', 'Year']]
    X, y = [], []
    scaler = StandardScaler()
    target_scaler = MinMaxScaler(feature_range=(0, 1))
    
    # Process each player's data separately
    for player, group in data.groupby('Player'):
        group = group.sort_values(by='Year')  # Ensure the data is in chronological order, I already do this in the other file...
        group[feature_columns] = scaler.fit_transform(group[feature_columns])  # Scale data per player, "StandardScaler"
        group[target_column] = target_scaler.fit_transform(group[[target_column]]) # "MinMaxScaler from 0to1", potentially a point contention, it was associated with the .08 issue
        
        
        group_values = group[feature_columns].values
        group_labels = group[target_column].values
        
        for i in range(len(group) - seq_length):
            X.append(group_values[i:(i + seq_length)])
            y.append(group_labels[i + seq_length])
    if "passing" in filepath:
        joblib.dump(scaler, 'Models/passing_feature_scaler.pkl')  # Saves the feature scaler
        joblib.dump(target_scaler, 'Models/passing_target_scaler.pkl')  # Saves the target scaler
    elif "rushing" in filepath:
        joblib.dump(scaler, 'Models/rushing_feature_scaler.pkl')  # Saves the feature scaler
        joblib.dump(target_scaler, 'Models/rushing_target_scaler.pkl')  # Saves the target scaler
    elif "receiving" in filepath:
        joblib.dump(scaler, 'Models/receiving_feature_scaler.pkl')  # Saves the feature scaler
        joblib.dump(target_scaler, 'Models/receiving_target_scaler.pkl')  # Saves the target scaler
        

    return np.array(X), np.array(y)

