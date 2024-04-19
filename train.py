import torch
import torch.optim as optim

#One function here, train_model, which takes in the model, train_loader, criterion, optimizer, and num_epochs as arguments.
#I am not using the validation set in this at the moment, but it can easily be reconfigured by uncommenting the relevant lines. It will also require
#an additional argument for the validation loader. and some tweaks in the driver code.

def train_model(model, train_loader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        model.train()  # Set the model to training mode
        total_train_loss = 0
        
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()
        
        # After each epoch, evaluate on the validation set
        # model.eval()  # Set the model to evaluation mode
        # total_val_loss = 0
        # with torch.no_grad():
        #     for inputs, labels in val_loader:
        #         outputs = model(inputs)
        #         val_loss = criterion(outputs, labels)
        #         total_val_loss += val_loss.item()
        
        # Printing average losses
        print(f'Epoch {epoch+1}/{num_epochs}, Training Loss: {total_train_loss/len(train_loader)}')
              #, Validation Loss: {total_val_loss/len(val_loader)}')
    
    



