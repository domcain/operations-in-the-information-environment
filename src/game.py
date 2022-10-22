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
TotalVoting = 0
blueTeam    = 0
redTeam     = 1

# Australian Liberal/Labour expenses on political advertisement in 2022
StartingBudgetAUD = 250000
CurrentBalance = StartingBudgetAUD

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class AAAI_Game:
    def __init__(self):
        global NumberOfGreenNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty
        # NumberOfGreenNodes = int(input("Enter the size of the Green Team: "))
        # ProbabilityOfConnection = float(input(
        #     "Enter the probability of a connection between any given green player: "
        # ))
        # NumberOfGreyAgents = int(input("Enter Number of agents in the Grey Team: "))
        # RedSpyProportion = float(input("Enter the proportion of Red Spies within the Grey Team: "))
        # LowCertainty,HighCertainty = [float(x) for x in input(
        #     "Enter the Certainty interval of the Green Team. (e.g. [-0.1,0.1] or [-0.5,0.7]): "
        # ).split(',')]
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
            
        self.update_graph(self.G, TotalVoting)   
        # Build internal representation of the graph.
        nx.draw(self.G, node_color="Green", with_labels=1)

        # Generate user interface of the graph.
        plt.show()
    
    def access_graph(self, graph):
        return self.G

    def update_graph(self, graph, TotalVoting): #Set totalVoting for state access
        totalVoting = []
        for (p, d) in graph.nodes(data=True):
            if d['Certainty'] >= HighCertainty:
                totalVoting.append(p)
        TotalVoting = len(totalVoting)
        print("TotalVoting @ start: ", TotalVoting)

    def reset(self):
        global PLAYER, AI, turn
        # init game state
        self.G = nx.gnp_random_graph(NumberOfGreenNodes, ProbabilityOfConnection)
 
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
            game_over = False
            if self.round_limit():
                game_over = True
                return game_over, self.score
            self._update_ui()
            # self.update_graph(self.G)
            return game_over
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
            # self.update_graph(self.G)
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
    
    # Get green nodes to interact with each other.
    def _green_interact(self):
        # Iterate through the array of green nodes
        for i in self.G.nodes(data="Certainty"):
            # Who is the current nodes neighbours?
            neighbors = nx.neighbors(self.G, i)
            # Iterate through the current nodes neighbours
            for j in neighbors:
                # Neighbors haven't already interacted
                if neighbors[j] > i:
                    # Set the nodes certainty to the average between its
                    # current certainty, and the neighbouring nodes certainty.
                    self.G.nodes[i]["Certainty"] = (self.G.nodes[i]["Certainty"] + self.G.nodes[j]["Certainty"]) / 2 

    def _update_node(self, node_id, action, team):
        node = self.G.nodes[node_id]
        if node["Certainty"] > HighCertainty:
            node["Will Vote"] = True
            TotalVoting += 1 
        
        if LowCertainty < node["Certainty"] < HighCertainty:
            node["Will Vote"] = None
        
        if node["Certainty"] < LowCertainty:
            node["Will Vote"] = False
        
        # From Reds message potency, e.g. 1.x, x*10 becomes the chance of ignoring red team members.
        IgnoreRedchance = ((1 - action) * 10)
        # Green nodes only ignore Red when their certainty value is positive (leaning toward voting).
        if team == redTeam & node["Certainty"] > 0:
            # If the Green node doesn't tolerate Red's nonsense, they will ignore them. 
            if IgnoreRedchance >= node["Tolerance"]:
                node["Ignore Red"] = True
            # If they tolerate a bit, leave whether they ignore Red to chance (nonsense / tolerance of respective node).
            else:
                node["Ignore Red"] = random.random()<(IgnoreRedchance/node["Tolerance"])             

    def _move(self, action, team):
        global BudgetAUD, CurrentBalance, round
        if team == blueTeam & action <= 5 & CurrentBalance > 0:
            # Add multiplier for each message level then affect blue budget
            for n in self.G.nodes:
                self.G.nodes[n]["Certainty"] = self.G.nodes[n]["Certainty"] * multiplierDict[action]
                self._update_node(n, multiplierDict[action], blueTeam)
            # Subtract the cost of the move from the budget.
            CurrentBalance -= BudgetAUD*(multiplierDict[action]-1)
            round += 1
        # Intrduce a foreign power into the game.   
        elif action == 6:
            # introduce_grey_agent()
            round += 1
        # Skip blue teams turn.
        elif action == 7:
            round += 1
            # TODO: ADD MATHS

        if team == redTeam:
            self.G.nodes[n]["Certainty"] = self.G.nodes[n]["Certainty"] * (2 - multiplierDict[action])
            self._update_node(n, multiplierDict[action], redTeam)
            round += 1
            # TODO: ADD MATHS

    # def _get_reward(self):
