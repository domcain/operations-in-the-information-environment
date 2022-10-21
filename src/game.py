from matplotlib import pyplot as plt
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

multiplierDict = {
    1:1.01,
    2:1.03,
    3:1.09,
    4:1.32,
    5:1.99
}

global NumberOfGreenNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty, turn
PLAYER = 0
AI = 1

# turn = random.randint(PLAYER, AI)

NumberOfRedAgents = 1
NumberOfBlueAgents = 1
NumberOfGreenNodes = 20
ProbabilityOfConnection = 0.3
NumberOfGreyAgents = 5
RedSpyProportion = 0.5
LowCertainty = -0.9
HighCertainty = 0.9
# A certainty level, above which a green node will vote in the election.
VoteThreshold = (HighCertainty + LowCertainty) / 2
StandardTolerance = 10
AverageTolerance = 50
# Create a normal distribution of tolerance value's to be given to each green node later.
ToleranceFloat = np.random.normal(AverageTolerance, StandardTolerance, NumberOfGreenNodes)
# Above ^^^ creates an array of floats, convert this into an array of integers.
Tolerance = ToleranceFloat.astype(int)
blueTeam    = 0
redTeam     = 1

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class AAAI_Game:
    def __init__(self):
        global NumberOfGreenNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty
        NumberOfGreenNodes = int(input("Enter the size of the Green Team: "))
        ProbabilityOfConnection = float(input(
            "Enter the probability of a connection between any given green player: "
        ))
        NumberOfGreyAgents = int(input("Enter Number of agents in the Grey Team: "))
        RedSpyProportion = float(input("Enter the proportion of Red Spies within the Grey Team: "))
        LowCertainty,HighCertainty = [float(x) for x in input(
            "Enter the Certainty interval of the Green Team. (e.g. [-0.1,0.1] or [-0.5,0.7]): "
        ).split(',')]
        print(
            "Size of the Green Team: " + str(NumberOfGreenNodes) + "\n",
            "Probability of a connection between any given green player: " + str(ProbabilityOfConnection) + "\n",
            "Number of agents in the Grey Team: " + str(NumberOfGreyAgents) + "\n",
            "Proportion of Red Spies within the Grey Team: " + str(RedSpyProportion) + "\n",
            "Certainty interval of the Green Team: " + str(LowCertainty) + ', ' + str(HighCertainty) + "\n"
        )
        # Create the graph.
        self.G = nx.gnp_random_graph(NumberOfGreenNodes, ProbabilityOfConnection)

        # Initialise the graph, assign each node the relevent information.
        for i in self.G.nodes:
            self.G.nodes[i]["Team"] = "Green"
            self.G.nodes[i]["Certainty"] = random.uniform(LowCertainty,HighCertainty)
            self.G.nodes[i]["Will Vote"] = None
            self.G.nodes[i]["Ignore Red"] = False
            self.G.nodes[i]["Tolerance"] = Tolerance[i]      
                
        # Build internal representation of the graph.
        nx.draw(self.G, node_color="Green", with_labels=1)

        # Generate user interface of the graph.
        plt.show()
    
    def access_graph(self, graph):
        return self.G

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
            # self.clock.tick(SPEED)

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
        # TODO LOW PRIORITY
        pass

    def _green_interact(self):
        #TODO
        # get green nodes to interact with eachother after a move has been made
        # neighbors = list(self.G.neighbors(0))
        
        pass

    def _update_node(self, node_id, action, team):
        node = self.G.nodes[node_id]
        if node["Certainty"] > HighCertainty:
            node["Will Vote"] = True
        
        if LowCertainty < node["Certainty"] < HighCertainty:
            node["Will Vote"] = None
        
        if node["Certainty"] < LowCertainty:
            node["Will Vote"] = False

        if team == redTeam & node["Certainty"] > 0:
            node["Ignore Red"] = random.random()<(((1 - action) * 10)/node["Tolerance"]) 
            # TODO Document this
            # chance of ignoring redTeam

    def _move(self, action, team):
        
        if team == blueTeam:
            for n in self.G.nodes: #add multiplier for each message level then affect blue budget
                self.G.nodes[n]["Certainty"] * multiplierDict[action]
                self._update_node(n, multiplierDict[action], blueTeam)
            round += 1
            # TODO: ADD MATHS

        if team == redTeam:
            self.G.nodes[n]["Certainty"] * (2 - multiplierDict[action])
            self._update_node(n, multiplierDict[action], redTeam)
            round += 1
            # TODO: ADD MATHS

    # def _get_reward(self):
