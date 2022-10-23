from matplotlib import pyplot as plt
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

multiplierDict = {
    0:1.01,
    1:1.03,
    2:1.09,
    3:1.32,
    4:1.99
}

# global NumberOfNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty, turn
PLAYER = 0
AI = 1

# turn = random.randint(PLAYER, AI)
NumberOfNodes = 20
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
ToleranceFloat = np.random.normal(AverageTolerance, StandardTolerance, NumberOfNodes)
# Above ^^^ creates an array of floats, convert this into an array of integers.
Tolerance = ToleranceFloat.astype(int)
TotalVoting = 0
TotalNotVoting = 0
blueTeam    = 0
redTeam     = 1
reward = 0

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
        global NumberOfNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty, VoteThreshold
        self.NumberOfNodes = NumberOfNodes
        self.score = 0
        # NumberOfNodes = int(input("Enter the size of the Green Team: "))
        # ProbabilityOfConnection = float(input(
        #     "Enter the probability of a connection between any given green player: "
        # ))
        # NumberOfGreyAgents = int(input("Enter Number of agents in the Grey Team: "))
        # RedSpyProportion = float(input("Enter the proportion of Red Spies within the Grey Team: "))
        # LowCertainty,HighCertainty = [float(x) for x in input(
        #     "Enter the Certainty interval of the Green Team. (e.g. [-0.1,0.1] or [-0.5,0.7]): "
        # ).split(',')]
        # VoteThreshold = (HighCertainty + LowCertainty) / 2
        print(
            "Size of the Green Team: " + str(NumberOfNodes) + "\n",
            "Probability of a connection between any given green player: " + str(ProbabilityOfConnection) + "\n",
            "Number of agents in the Grey Team: " + str(NumberOfGreyAgents) + "\n",
            "Proportion of Red Spies within the Grey Team: " + str(RedSpyProportion) + "\n",
            "Certainty interval of the Green Team: " + str(LowCertainty) + ', ' + str(HighCertainty) + "\n"
        )
        # Create the graph.
        self.G = nx.gnp_random_graph(NumberOfNodes, ProbabilityOfConnection)

        # Initialise the graph, assign each node the relevent information.
        for i in self.G.nodes:
            self.G.nodes[i]["Team"] = "Green"
            self.G.nodes[i]["Certainty"] = random.uniform(LowCertainty,HighCertainty)
            self.G.nodes[i]["Will Vote"] = None # add update_node function
            self.G.nodes[i]["Ignore Red"] = False
            self.G.nodes[i]["Tolerance"] = Tolerance[i]                      
        self._update_will_vote_values(self.G)

        # Build internal representation of the graph.
        nx.draw(self.G, node_color="Green", with_labels=1)

        # Generate user interface of the graph.
        plt.show()

    def _update_will_vote_values(self, graph): #Creates/Updates the voting/not voting arrays for every node in the graph
        NodesVoting = [] # A list of nodes that are going to vote
        NodesNotVoting = [] # A list of nodes that are NOT going to vote
        # global TotalVoting, TotalNotVoting
        for (p, d) in graph.nodes(data=True):
            if d['Certainty'] >= VoteThreshold: # If the node's certainty is higher or equal to the midpoint between the certainty intervals
                NodesVoting.append(True)
                d["Will Vote"] = True
            if d['Certainty'] < VoteThreshold: # If the node's certainty is lower than the midpoint between the certainty intervals
                NodesNotVoting.append(False)
                d["Will Vote"] = False
        # TotalVoting = len(NodesVoting)
        # TotalNotVoting = len(NodesNotVoting)
        # print("TotalVoting @ start: ", TotalVoting)
        # print("TotalNotVoting @ start: ", TotalNotVoting)
        return NodesVoting, NodesNotVoting

    def reset(self):
        global PLAYER, AI, turn
        # init game state
        self.G = nx.gnp_random_graph(NumberOfNodes, ProbabilityOfConnection)
 
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
        global reward #initalised at 0
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
            game_over = False
            self.get_score(self.score)
            if self.round_limit():
                game_over = True
                return game_over, self.score

            # 4. place new food or just move
            old_reward = reward
            reward = self._get_reward(old_reward,turn)
            
            # 5. update ui and clock
            self._update_ui()
            # self.update_graph(self.G)
            # self.clock.tick(SPEED)

            # 6. return game over and score

            return reward, game_over, self.score


    def get_score(self, score):
        global TotalVoting, TotalNotVoting
        if AI == blueTeam:
            if TotalVoting > TotalNotVoting:
                score = 1
            else:
                score = 0
        if AI == redTeam:
            if TotalNotVoting > TotalNotVoting:
                score = 1
        else:
                score = 0 
        return score

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
                    #TODO: UPDATE NODES HERE BISH

    def _update_voting_totals(self, node_id, PrevWillVote, action, team):
        global TotalVoting
        global TotalNotVoting
        node = self.G.nodes[node_id]
        if node["Will Vote"] and PrevWillVote != node["Will Vote"]:
            TotalVoting += 1 
        
        if node["Will Vote"] == False and PrevWillVote != node["Will Vote"]:
            TotalVoting -= 1

        
        if node["Certainty"] < LowCertainty:
            TotalNotVoting += 1
        
        
        # From Reds message potency, e.g. 1.x, x*10 becomes the chance of ignoring red team members.
        IgnoreRedchance = ((1 - action) * 10)
        # Green nodes only ignore Red when their certainty value is positive (leaning toward voting).
        if team == redTeam and node["Certainty"] > 0.0:
            # If the Green node doesn't tolerate Red's nonsense, they will ignore them. 
            if IgnoreRedchance >= node["Tolerance"]:
                node["Ignore Red"] = True
            # If they tolerate a bit, leave whether they ignore Red to chance (nonsense / tolerance of respective node).
            else:
                node["Ignore Red"] = random.random()<(IgnoreRedchance/node["Tolerance"])             

    def _move(self, action, team):
        global BudgetAUD, CurrentBalance, round, reward
        if team == blueTeam & action <= 4 & CurrentBalance > 0:
            for n in self.G.nodes: #add multiplier for each message level then affect blue budget
                print(" self.G.nodes[n]: ",  self.G.nodes[n]["Certainty"])
                PrevWillVote = self.G.nodes[n]["Will Vote"]
                self.G.nodes[n]["Certainty"] = self.G.nodes[n]["Certainty"] * multiplierDict[action]
                self._update_voting_totals(n, PrevWillVote, multiplierDict[action], blueTeam)
                # Subtract the cost of the move from the budget.
                CurrentBalance -= BudgetAUD*(multiplierDict[action]-1)
                # round += 1
        # Intrduce a foreign power into the game.   
        elif team == blueTeam and action == 5:
            # TODO: introduce_grey_agent()
            pass
        # Skip blue teams turn.
        elif team == blueTeam and action == 6:
            pass
                  

        if team == redTeam:
            for n in self.G.nodes: #add multiplier for each message level then affect blue budget
                PrevWillVote = self.G.nodes[n]["Will Vote"]
                self.G.nodes[n]["Certainty"] = (self.G.nodes[n]["Certainty"]) * (2 - multiplierDict[action])
                self._update_voting_totals(n, PrevWillVote, multiplierDict[action], redTeam)
                # round += 1
                # TODO: ADD MATHS

    def _get_reward(self, old_TeamVoting, team):
        reward = 0
        # global TotalVoting
        # curr_TeamVoting = TotalVoting
        # if old_TeamVoting == curr_TeamVoting: #no change
        #         reward = 0

        # if team == blueTeam:
        #     if old_TeamVoting > curr_TeamVoting: #define this variable 
        #         reward = 10 #  percentage increase in people voting is the multiplier
        #     if old_TeamVoting > curr_TeamVoting:
        #         reward = -10 * reward # percentage decrease in people voting is the multiplier
        # if team == redTeam:
        #     if old_TeamNotVoting > curr_TeamNotVoting: #define this variable 
        #         reward = 10 * X # percentage increase in people voting is the multiplier
        #     if old_TeamNotVoting > curr_TeamNotVoting:
        #         reward = -10 * X # percentage decrease in people voting is the multiplier
        # 
        #         

        return reward
