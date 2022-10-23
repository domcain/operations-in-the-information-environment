from math import gamma
import random
import sys
import os
import numpy as np
from collections import deque
import torch
from game import AAAI_Game
from model import Linear_QNet, QTrainer
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001  # LEARNING RATE

PLAYER = 0
AI = 1
redTeam = 1
blueTeam = 0
NoOfActions = 5


# add 
turn = PLAYER
class Agent:
    def __init__(self, game):
        self.n_games = 0  # max 50
        self.epsilon = 0  # randomness level
        self.gamma = 0.9  # discount rate, smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft() when memory is full
        self.model = Linear_QNet(
            game.NumberOfNodes, 256, NoOfActions #7 needs to chane to AI red or blue moves 
        )  # first is size of state, output is 7 (seven different numbers in action). play with hidden.
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):  # in video 11 states/values
        WillVote, WontVote = game._update_will_vote_values(game.G) #returns the amount of green nodes voting
        print("Voting Array: ", WillVote)
        print("Not Voting Array: ", WontVote)
        state = np.concatenate((WillVote,WontVote))
        print("state: ", state)
        return np.array(state,dtype=int)
        # will return an array of state values

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append(
            (state, action, reward, next_state, game_over)
        )  # popleft if MAX_MEMORY is full

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(
                self.memory, BATCH_SIZE
            )  # Returns list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(
            *mini_sample
        )  # puts all of states, actions, rewards, next_states, dones together or iterate
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
        # for state, action, reward, next_state, game_over in mini_sample:

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves: tradeoff between exploration and exploitation (deep learning)
        self.epsilon = 80 - self.n_games
        # the more games the smaller the epsilon (or randomness) leading to more tailored moves
        
        if AI == redTeam:  
            final_move = [0, 0, 0, 0, 0, 0, 0]  # 5 levels of potency in ascending order
            #Pick Random Move 
            if random.randint(0, 200) < self.epsilon: 
                move = random.randint(0, 4)  # gives random number between 0 and 4
                final_move[move] = 1
                display_message(move, redTeam)
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)  # will execute forward function
                print("Prediction: ", prediction)
                move = torch.argmax(prediction).item()
                final_move[move] = 1

        if AI == blueTeam:
            final_move = [0, 0, 0, 0, 0, 0, 0]  # 5 levels of budget spend in ascending order with the last two options being play a grey agent and do nothing (respectively)
            if random.randint(0, 200) < self.epsilon:
                move = random.randint(0, 6)  # gives random number between 0 and 6
                final_move[move] = 1
                display_message(move, blueTeam)
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)  # will execute forward function
                move = torch.argmax(prediction).item()
                final_move[move] = 1

        return final_move

def display_message(number, team):
    if team == blueTeam:
        if number == 0:
            print("Just in from the blueTeam: '.'\n")
        if number == 1:
            print("Just in from the blueTeam: '.'\n")
        if number == 2:
            print("Just in from the blueTeam: '.'\n")
        if number == 3:
            print("Just in from the blueTeam: '.'\n")
        if number == 4:
            print("Just in from the blueTeam: '.'\n")
        if number == 5:
            print("Blue Team played a SPY '.'\n")
        if number == 6:
            print("Blue Team skipped a turn '.'\n")

    if team == redTeam:
        if number == 0:
            print("Just in from the redTeam: 'Purple leaders are publicly celebrating Blue Teams's reelection. They can't wait to see how flexible the Blue Team will be now.'\n")
        if number == 1:
            print("Just in from the redTeam: 'We should have gotten more of the oil in Syria, and we should have gotten more of the oil in Irag. Dumb Blue Team.'\n")
        if number == 2:
            print("Just in from the redTeam: 'Let's take a closer look at that birth certificate. @BlueAgent was described in 2003 as being 'born in OrangeLand'.\n")
        if number == 3:
            print("Just in from the redTeam: 'Blue Team's Windmills are the greatest threat in the Green Country to both bald and hairless green people. Media claims fictional 'global warming' is worse.'\n")
        if number == 4:
            print("Just in from the redTeam: 'Healthy young child goes to doctor, gets pumped with massive shot of many vaccines, doesn't feel good and changes - AUTISM. Many such cases.'\n")

def get_user_action():
    level = 0
    while 1 > level or 5 < level:
        try:
            level = int(input("Enter a message potency level between 1 - 5: "))
        except ValueError:
            print("That wasn't an integer :(\n")
    return level

def train():
    plot_scores = []  # track scores
    plot_mean_scores = []  # average scores
    total_score = 0
    final_move_index = 0
    record = 0
    game = AAAI_Game()
    agent = Agent(game)
    # game.__init__()
    turn = PLAYER
    while True:  # training loop
        if turn == AI:
            if AI == blueTeam:
                NoOfActions = 7
            if AI == redTeam:
                NoOfActions = 5
            # get current state
            current_state = agent.get_state(game)

            # get move
            final_move = agent.get_action(current_state)
            final_move_index = final_move.index(1)
            # perform move and get new state
            reward, done, score = game.play_step(final_move_index, turn)
            new_state = agent.get_state(game)

            # train short-memory
            agent.train_short_memory(current_state, final_move, reward, new_state, done)

            # remember this ^
            agent.remember(current_state, final_move, reward, new_state, done)

            turn += 1
            turn = turn % 2

        if turn == PLAYER:
            if turn == blueTeam:
                action = get_user_action() #get user input 
                done = game.play_step(action, blueTeam)
            if turn == redTeam:
                action = get_user_action() #get user input 
                game.play_step(action, redTeam)
            
            turn += 1
            turn = turn % 2

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:  # highest score
                record = score
                agent.model.save()

            print("Game", agent.n_games, "Score", score, "Record", record)

            # TODO: plot


if __name__ == "__main__":
    train()