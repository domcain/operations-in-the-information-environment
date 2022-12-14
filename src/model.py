import torch
import torch.nn as nn
import torch.optim as optim  # optimiser
import torch.nn.functional as F
import os


class Blue_Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)  # Linear Layer (see diagram)
        self.linear2 = nn.Linear(hidden_size, output_size)  # Linear Layer

    # Forward function gets the tensor for pytorch
    # Apply Linear layer and an activation function
    def forward(self, x):  # x is tensor
        x = F.relu(
            self.linear1(x)
        )  # Applies a rectified linear unit function element-wise
        x = self.linear2(x)
        return x

    # Saves model to file
    def save(self, file_name="blue_model.pth"):
        model_folder_path = "./blue_model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)  # filename for saving
        torch.save(self.state_dict(), file_name)


class Red_Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)  # Linear Layer (see diagram)
        self.linear2 = nn.Linear(hidden_size, output_size)  # Linear Layer

    # Forward function gets the tensor for pytorch
    # Apply Linear layer and an activation function
    def forward(self, x):  # x is tensor
        x = F.relu(
            self.linear1(x)
        )  # Applies a rectified linear unit function element-wise
        x = self.linear2(x)
        return x

    # Saves model to file
    def save(self, file_name="red_model.pth"):
        model_folder_path = "./red_model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)  # filename for saving
        torch.save(self.state_dict(), file_name)


class Blue_QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimiser = optim.Adam(
            model.parameters(), lr=self.lr
        )  # Using the Adam optimiser
        self.criterion = nn.MSELoss()  # Loss function loss is mean square error

    def train_step(
        self, state, action, reward, next_state, done
    ):  # done = game over boolean
        if done == True:
            print("Done is true")
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n,x)

        if len(state.shape) == 1:
            # (1, x) 1 is number of batches
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: Predicted Q values with current state
        pred = self.model(state)  # state0

        target = pred.clone()
        print(target)
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(next_state[idx])
                )
            target[idx][torch.argmax(action).item()] = Q_new

        # 2:Q_new = r + y * MAX(next_predicted q value) -> only do if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimiser.zero_grad()  # empty gradient for pytorch
        loss = self.criterion(target, pred)  # Q_new and Q respectively
        loss.backward()  # Apply a backward pass

        self.optimiser.step()


class Red_QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimiser = optim.Adam(
            model.parameters(), lr=self.lr
        )  # Using the Adam optimiser
        self.criterion = nn.MSELoss()  # Loss function loss is mean square error

    def train_step(
        self, state, action, reward, next_state, done
    ):  # done = game over boolean
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n,x)

        if len(state.shape) == 1:
            # (1, x) 1 is number of batches
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: Predicted Q values with current state
        pred = self.model(state)  # state0

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(next_state[idx])
                )
            target[idx][torch.argmax(action).item()] = Q_new
            # print("Target:  ", target)
            # print("Q_New: ", Q_new)
            # print("Action: ", action)

        # 2:Q_new = r + y * MAX(next_predicted q value) -> only do if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimiser.zero_grad()  # empty gradient for pytorch
        loss = self.criterion(target, pred)  # Q_new and Q respectively
        loss.backward()  # Apply a backward pass

        self.optimiser.step()
