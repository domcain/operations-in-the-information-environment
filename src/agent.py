from math import gamma
import random
from socket import AI_ALL
import sys
import os
import numpy as np
from collections import deque
import torch
from game import AAAI_Game, NumberOfGreyAgents
from model import Linear_QNet, QTrainer
import numpy as np
import networkx as nx
from helper import plot
import matplotlib.pyplot as plt

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001  # LEARNING RATE

PLAYER = 0
AI = 1
redTeam = 1
blueTeam = 0
NoOfActions = 5

#Set to True to test with random moves
isTesting = True 

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
        state = np.concatenate((WillVote,WontVote))
        # will return an array of state values
        return np.array(state,dtype=int)

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
                # print("Prediction: ", prediction)
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
            print("Blue Party Announcement: 'We welcome all those showing support in our struggle for Democracy! ' \n")
        if number == 1:
            print("Just in from The Blue Party: 'Records indicate absence of Blue Party interference in Red Parties' resource negotiations with The United Blacklands.'\n")
        if number == 2:
            print("'Official Birth Certificate of @BluePartyLeader clarifies their idigenous Greenland heritage.'\n")
        if number == 3:
            print("Just in from The Blue Party: 'R&D into wind turbines conducted in 2012 reduced wildlife wind-turbine related deaths to 0 since their implementation in 2015.'\n")
        if number == 4:
            print("Breaking News: 'Concerns that Autism Spectrum Disorder(ASD) might be linked to vaccination, BUT studies have shown that there is no link between receiving vaccines and developing ASD. The National Institute of Medicine reviewed the safety of 8 vaccines. The findings state that vaccines are very safe.'\n")
        if number == 5:
            print("The Blue Party have snuck an illegal immigrant into Greenland\n")
        if number == 6:
            print("The Blue Party turned a blind eye\n")

    if team == redTeam:
        if number == 0:
            print("Just in from the Proud Elephants: 'Purple leaders are publicly celebrating the formalisation of Gang; 'The Blue Party'. They can't wait to see how flexible The Blue Party may be.'\n")
        if number == 1:
            print("Just in from the Proud Elephants: 'We should have gotten more of the oil in The United Blacklands. Dumb Blue Party meddling with negotiations.'\n")
        if number == 2:
            print("Just in from the Proud Elephants: 'Let's take a closer look at that birth certificate. Mob Boss: @BluePartyLeader was described in 2003 as being 'born in OrangeLand'.\n")
        if number == 3:
            print("Just in from the Proud Elephants: 'Blue Team's Windmills are the greatest threat in the Green Country to both bald and hairless green people. Media claims fictional 'global warming' is worse.'\n")
        if number == 4:
            print("Just in from the Proud Elephants: 'Healthy young child goes to doctor, gets pumped with massive shot of many vaccines, doesn't feel good and changes - AUTISM. Many such cases.'\n")

def get_user_action():
    level = 0
    if PLAYER == redTeam:
        if isTesting:
            return random.randint(0,4)
        while 1 > level or 5 < level:
            try:
                level = int(input("Red Team Options: \n", "    - Enter a message potency of your choice (1 - 5) \n"))
            except ValueError:
                print("That wasn't an integer :(\n")
        return level
    if PLAYER == blueTeam:
        print("Blue Team Options: \n" , "    - Enter a message potency level between (1 - 5)\n", "    - Inject a GREY agent (6)\n","    - Skip a turn (7)\n")
        if isTesting:
            while True:
                level = random.randint(0,6)
                if level == 6 and NumberOfGreyAgents == 0:
                    continue
                else:
                    return level

        while True:
            try:
                level = int(input())
                if level == 1234: #terminate game
                    sys.exit()
                if level == 6 and NumberOfGreyAgents == 0:
                    print("Maximum number of grey agents have been played, try another move:\n")
                    continue
                if level >= 1 and level <= 7:
                    if AAAI_Game().calc_valid_move(level-1):
                        break
                    else:
                        print("You don't have enough money! Try another move :(\n")
                        continue
            except ValueError:
                print("That wasn't an integer :(\n")
            
        return level-1



def train():
    global PLAYER, AI
    plot_scores = []  # track scores
    plot_mean_scores = []  # average scores
    total_score = 0
    final_move_index = 0
    record = 0
    done = False
    game = AAAI_Game()
    agent = Agent(game)
    # game.__init__()
    turn = PLAYER
    AiGamesWon = 0
    while True:  # training loop
        if done:
            # train long memory, plot result
            done = False
            game.reset()
            
            agent.n_games += 1
            agent.train_long_memory()
            if game.WhoWon == AI:
                AiGamesWon += 1
                agent.model.save()
            if score > record and game.WhoWon == AI:  # highest score
                record = score
                agent.model.save()
                score = 0
            if game.WhoWon == PLAYER:
                score = 0

            print("RESULTS:","\n    - Game: ", agent.n_games, "\n    - Score: ", score, "\n    - Record: ", record, "\n    - Who Won? : ", game.WhoWon)
            
            plot_scores.append((AiGamesWon/agent.n_games)*100)
            total_score += AiGamesWon
            mean_score = AiGamesWon / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            # Set Teams
            score = 0
            turn = random.randint(PLAYER, AI)
            if(PLAYER == redTeam):
                PLAYER = redTeam
                AI = blueTeam
            else:
                PLAYER = blueTeam
                AI = redTeam
                
        if turn == AI:
            print("Your oponent's move!\n")
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
            display_message(final_move_index, AI)
            new_state = agent.get_state(game)

            # train short-memory
            agent.train_short_memory(current_state, final_move, reward, new_state, done)

            # remember this ^
            agent.remember(current_state, final_move, reward, new_state, done)

            turn += 1
            turn = turn % 2
            # game.round += 0.5
            
            print("\n\n\n\n\n\nRound: ", game.round, "\n")
            plt.plot(label = turn)
        
        if done:
            # train long memory, plot result
            done = False
            game.reset()
            
            agent.n_games += 1
            agent.train_long_memory()
            if game.WhoWon == AI:
                AiGamesWon += 1
                agent.model.save()

            if score > record and game.WhoWon == AI:  # highest score
                record = score
                agent.model.save()
            if game.WhoWon == PLAYER:
                score = 0

            print("RESULTS:","\n    - Game: ", agent.n_games, "\n    - Score: ", score, "\n    - Record: ", record, "\n    - Who Won? : ", game.WhoWon)

            plot_scores.append((AiGamesWon/agent.n_games)*100)
            total_score += AiGamesWon
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            # Set Teams
            score = 0
            turn = random.randint(PLAYER, AI)
            if(PLAYER == redTeam):
                PLAYER = redTeam
                AI = blueTeam
            else:
                PLAYER = blueTeam
                AI = redTeam

        if turn == PLAYER:
            print("Your move!\n")
            if turn == blueTeam:
                 
                action = get_user_action() #get user input
                while game._calc_valid_move(action)!=False:
                    action = get_user_action()
                done = game.play_step(action, blueTeam)
            if turn == redTeam:
                action = get_user_action() #get user input 
                done = game.play_step(action, redTeam)
            
            turn += 1
            turn = turn % 2
            # game.round += 0.5
            print("\n\n\n\n\n\nRound: ", (game.round),"\n")

            plt.plot(label = turn)


if __name__ == "__main__":
    train()