import torch
import torch.optim as optim

class ModelTrainer:
    def train_model(model, train_loader, criterion, optimizer, max_epochs):
        epoch = 0
        training_loss = float('inf')  # Initialize to a high value
        
        while training_loss > 0.1 and epoch < max_epochs:
            model.train()  # Set the model to training mode
            total_train_loss = 0  # Reset total training loss for each epoch
            
            # Loop over training data
            for inputs, labels in train_loader:
                optimizer.zero_grad()  # Reset gradients
                outputs = model(inputs)  # Forward pass
                loss = criterion(outputs, labels)  # Calculate loss
                loss.backward()  # Backward pass
                optimizer.step()  # Update weights
                total_train_loss += loss.item()  # Accumulate loss
            
            # Calculate average training loss for the epoch
            training_loss = total_train_loss / len(train_loader)
            epoch += 1
            
            # Log progress
            print(f'Epoch {epoch}, Training Loss: {training_loss:.4f}')
        
        # Indicate training completion or max epochs reached
        if training_loss <= 0.1:
            print("Training Complete. Loss is below 0.1")
        else:
            print(f"Reached Maximum Epochs: {max_epochs}. Final Training Loss: {training_loss:.4f}")
