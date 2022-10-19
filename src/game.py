from matplotlib import pyplot as plt
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Messages(Enum):  # Direction
    # RIGHT = 1 ""
    # LEFT = 2
    # UP = 3
    # DOWN = 4
    MESSAGE1 = 1  # "Purple leaders are publicly celebrating Blue Teams's reelection. They can't wait to see how flexible the Blue Team will be now."
    MESSAGE2 = 2  # "We should have gotten more of the oil in Syria, and we should have gotten more of the oil in Irag. Dumb Blue Team."
    MESSAGE3 = 3  # Let's take a closer look at that birth certificate. @BlueAgent was described in 2003 as being "born in OrangeLand".
    MESSAGE4 = 4  # Blue Team's Windmills are the greatest threat in the Green Country to both bald and hairless green people. Media claims fictional 'global warming' is worse.
    MESSAGE5 = 5  # Healthy young child goes to doctor, gets pumped with massive shot of many vaccines, doesn't feel good and changes - AUTISM. Many such cases.

    # BLUE_TURN = 6
    NO_TURN = 0

global NumberOfGreenNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty, turn
PLAYER = 0
AI = 1

turn = random.randint(PLAYER, AI)

redTeam = 1
blueTeam = 0


NumberOfRedAgents = 1
NumberOfBlueAgents = 1
NumberOfGreenNodes = None
ProbabilityOfConnection = None
NumberOfGreyAgents = None
RedSpyProportion = None
LowCertainty = None
HighCertainty = None
VoteThreshold = None
blueTeam = 0
redTeam = 1

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 100


class AAAI_Game:
    def __init__(self):
        NumberOfGreenNodes = int(input("Enter the size of the Green Team: "))
        ProbabilityOfConnection = float(
            input(
                "Enter the probability of a connection between any given green player: "
            )
        )
        NumberOfGreyAgents = int(input("Enter Number of agents in the Grey Team: "))
        RedSpyProportion = float(
            input("Enter the proportion of Red Spies within the Grey Team: ")
        )
        LowCertainty, HighCertainty = [
            float(x)
            for x in input(
                "Enter the Certainty interval of the Green Team. (e.g. [-0.1,0.1] or [-0.5,0.7]): "
            ).split(",")
        ]
        print(
            "Size of the Green Team: " + str(NumberOfGreenNodes) + "\n",
            "Probability of a connection between any given green player: "
            + str(ProbabilityOfConnection)
            + "\n",
            "Number of agents in the Grey Team: " + str(NumberOfGreyAgents) + "\n",
            "Proportion of Red Spies within the Grey Team: "
            + str(RedSpyProportion)
            + "\n",
            "Certainty interval of the Green Team: "
            + str(LowCertainty)
            + ", "
            + str(HighCertainty)
            + "\n",
        )

        # Variable used to construct the graph
        TotalNumberOfNodes = NumberOfGreenNodes + NumberOfRedAgents + NumberOfBlueAgents

        # A certainty level, above which a green node will vote in the election
        VoteThreshold = (HighCertainty + LowCertainty) / 2

        # Create the graph
        G = nx.complete_graph(TotalNumberOfNodes)

        # Assign colours to the graph
        color_map = [
            "blue" if nodes == blueTeam else "red" if nodes == redTeam else "green"
            for nodes in G
        ]

        # Initialise the graph, assign each node the relevent information
        for i in G.nodes:
            # First node is the Blue Agent
            if i == blueTeam:
                G.nodes[i]["Team"] = "Blue"
            # Second node is the Red Agent
            if i == redTeam:
                G.nodes[i]["Team"] = "Red"
            # Every other node is Green
            G.nodes[i]["Team"] = "Green"
            G.nodes[i]["Certainty"] = random.uniform(LowCertainty, HighCertainty)
            G.nodes[i]["Will Vote"] = G.nodes[i]["Certainty"] >= VoteThreshold
            G.nodes[i]["Ignore Red"] = False

        # Build internal representation of the graph
        nx.draw(G, node_color=color_map, with_labels=1)

        # Generate user interface of the graph
        plt.show()

    def reset(self):
        # init game state
        # TODO RESET GAME WITH NETWORKX
        self.score = 0
        self.frame_iteration = 0
        #SET TEAMS
        turn = random.randint(PLAYER, AI)
        if(PLAYER == redTeam):
            PLAYER = redTeam
            AI = blueTeam
        else:
            PLAYER = blueTeam
            AI = redTeam

    def play_step(self, action, turn):
        # 1. Get User Input
        # 2. Play move
        if turn == PLAYER:
            self._move(action, PLAYER)
            if self.round_limit():
                game_over = True
                return game_over, self.score
            self._update_ui()
        else:
            self._move(action, AI)  # Choose move (update the head)

            # 3. check if game over
            reward = 0
            game_over = False
            if self.round_limit():
                game_over = True
                return game_over, self.score

            # 4. place new food or just move

            reward = self._get_reward()

            # 5. update ui and clock
            self._update_ui()
            self.clock.tick(SPEED)
            # 6. return game over and score
            return reward, game_over, self.score

    def round_limit(self, round=0):
        if round > 20:
            return True
        return False

    def _update_ui(self):
        # Build internal representation of the graph
        # nx.draw(G, node_color=color_map, with_labels=1)

        # # # Generate user interface of the graph
        # plt.show()
        pass

    def _move(self, action, team):
        if team == blueTeam:
            pass
            round += 1
            # TODO: ADD MATHS

        if team == redTeam:
            pass
            round += 1
            # TODO: ADD MATHS

    # def _get_reward(self):
