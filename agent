import random
import numpy as np
from collections import deque
import torch
from game import AAAI_Game, Direction, Point
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001  # LEARNING RATE


class Agent:
    def __init__(self):
        self.n_games = 0  # max 50
        self.epsilon = 0  # randomness level
        self.gamma = 0.9  # discount rate, smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft() when memory is full
        self.model = Linear_QNet(
            11, 256, 3
        )  # first is size of state, output is 3 (three different numbers in action). play with hidden.
        self.trainer = QTrainer(self.model, lr=LR, gamme=self.gamma)

    def get_state(self, game):  # in video 11 states/values
        # add in dangers and stuff
        pass

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

        states, actions, rewards, next_states, dones = zip(
            *mini_sample
        )  # puts all of states, actions, rewards, next_states, dones together or iterate
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
        # for state, action, reward, next_state, game_over in mini_sample:

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves: tradeoff between exploration and exploitation (deep learning)
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]  # beginning
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)  # gives random 0 1 or 2
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)  # will execute forward function
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []  # track scores
    plot_mean_scores = []  # average scores
    total_score = 0
    record = 0
    agent = Agent()
    game = AAAI_Game()
    while True:  # training loop
        # get current state
        current_state = agent.get_state(game)

        # get move
        final_move = agent.get_action(current_state)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        new_state = agent.get_state(game)

        # train short-memory
        agent.train_short_memory(current_state, final_move, reward, new_state, done)

        # remember this ^
        agent.remember(current_state, final_move, reward, new_state, done)

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
