from matplotlib import pyplot as plt
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# turn = random.randint(PLAYER, AI)

# TODO: Set these to None (before submission)
# User inputed Variables
NumberOfNodes = 20                                  # Population size of Green
ProbabilityOfConnection = 0.3                       # Determines connectivity of the graph
NumberOfGreyAgents = 5                              # Number of times Blue can introduce a foreign power to the population
RedSpyProportion = 0.5                              # How likely is a foreign to be bad 

# Certainty related variables
LowCertainty = -0.9                                 # The certainty below which the agents know a node will NOT vote in the election
HighCertainty = 0.9                                 # The certainty above which the agents know a node will vote in the election
VoteThreshold = (HighCertainty + LowCertainty) / 2  # A certainty level, above which a green node will vote in the election.

# Tolerance related variables
StandardTolerance = 10                              # Standard deviation - determines the spread of tolerances produced
AverageTolerance = 50                               # Mean - anchors the distribution
ToleranceFloat = np.random.normal(AverageTolerance, StandardTolerance, NumberOfNodes) # Creates a normal distribution of tolerance value's to be given to each member of the green population.
Tolerance = ToleranceFloat.astype(int) # Above ^^^ creates an array of floats, convert this into an array of integers.

# Agent related variables
PLAYER = 0                                          #
AI = 1                                              #
TotalVoting = 0                                     #
TotalNotVoting = 0                                  #
blueTeam    = 0                                     #
redTeam     = 1                                     #
multiplierDict = {                                  # Dictionary containing each move and it's corresponding potency value
    1:1.01,
    2:1.03,
    3:1.09,
    4:1.32,
    5:1.99
}

# Australian Liberal/Labour expenses on political advertisement in 2022
StartingBudgetAUD = 250000
CurrentBalance = StartingBudgetAUD

# RGB colours
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class AAAI_Game:
    # Stores user inputs from the commandline.
    # Creates a new graph using the inputs and intialise its' nodes.
    # Creates a GUI to display the game state to the user.
    def __init__(self):
        global NumberOfNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty, VoteThreshold
        self.NumberOfNodes = NumberOfNodes
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
    
    # Checks whether each and every node for whether it will eventually vote or not.
    # Returns a list of nodes that will vote.
    # Returns a list of nodes that will Not vote.
    def _update_will_vote_values(self, graph):
        # A list of nodes that are going to vote
        NodesVoting = []
        
        # A list of nodes that are NOT going to vote
        NodesNotVoting = []
        
        for (p, d) in graph.nodes(data=True):
            # If the node will vote
            if d['Certainty'] >= VoteThreshold:
                NodesVoting.append(True)
                d["Will Vote"] = True
            # If the node wont vote
            if d['Certainty'] < VoteThreshold:
                NodesNotVoting.append(False)
                d["Will Vote"] = False
        
        return NodesVoting, NodesNotVoting

    # This function restarts the game:
    #   Creates a new graph
    #   Initialises its' nodes
    #   Resets the scores
    #   Choses who will move first and what team they are on
    #   Creates a new GUI
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
        # Set Teams
        turn = random.randint(PLAYER, AI)
        if(PLAYER == redTeam):
            PLAYER = redTeam
            AI = blueTeam
        else:
            PLAYER = blueTeam
            AI = redTeam

    # If the game has run its' course, stop and return the current score.
    # Otherwise, play a move and update the GUI.
    def play_step(self, action, turn):
        # Plays a move based upon the users input
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

    # Checker function to see if the game has finished.
    def round_limit(self, round=0):
        if round > 20:
            return True
        return False
    
    # Helper function to keep the human player updated on the current game state.
    def _update_ui(self):
        # Build internal representation of the graph
        # nx.draw(G, node_color=color_map, with_labels=1)

        # # # Generate user interface of the graph
        # plt.show()
        # TODO LOW PRIORITY
        pass
    
    # More opinionated green people influence their less opinionated neighbours.
    def _green_interact(self):
        # Iterate through the array of green nodes
        for i in self.G.nodes(data="Certainty"):
            # Who are the current nodes neighbours?
            neighbors = nx.neighbors(self.G, i)
            # Iterate through the neighbours this node hasn't interacted with yet
            for j in neighbors:
                if neighbors[j] > i:
                    CurrentNodeCertainty = self.G.nodes[i]["Certainty"]
                    NeighbourNodeCertainty = self.G.nodes[j]["Certainty"]
                    # Move the less certain node halfway toward the more certain node
                    if abs(CurrentNodeCertainty) < abs(NeighbourNodeCertainty):
                        CurrentNodeCertainty = (CurrentNodeCertainty + NeighbourNodeCertainty)/2
                    else:
                        NeighbourNodeCertainty = (NeighbourNodeCertainty + CurrentNodeCertainty)/2

    # Updates the game state voting totals so reward/punishment may be decided for each agent.
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

    # Calls the relevant functions based upon the move selected by the player or agent.
    def _move(self, action, team):
        global BudgetAUD, CurrentBalance, round
        if team == blueTeam & action <= 5 & CurrentBalance > 0:
            for n in self.G.nodes: #add multiplier for each message level then affect blue budget
                print(" self.G.nodes[n]: ",  self.G.nodes[n]["Certainty"])
                PrevWillVote = self.G.nodes[n]["Will Vote"]
                self.G.nodes[n]["Certainty"] = self.G.nodes[n]["Certainty"] * multiplierDict[action]
                self._update_voting_totals(n, PrevWillVote, multiplierDict[action], blueTeam)
                # Subtract the cost of the move from the budget.
                CurrentBalance -= BudgetAUD*(multiplierDict[action]-1)
                # round += 1
        # Intrduce a foreign power into the game.   
        elif team == blueTeam & action == 6:
            # introduce_grey_agent()
            round += 1
        # Skip blue teams turn.
        elif team == blueTeam & action == 7:
            round += 1
        # TODO: ADD MATHS
                  

        if team == redTeam:
            for n in self.G.nodes: #add multiplier for each message level then affect blue budget
                PrevWillVote = self.G.nodes[n]["Will Vote"]
                self.G.nodes[n]["Certainty"] = (self.G.nodes[n]["Certainty"]) * (2 - multiplierDict[action])
                self._update_voting_totals(n, PrevWillVote, multiplierDict[action], redTeam)

    # Gifts a reasonable reward or punishment to the agent based upon changes to the voting totals.
    def _get_reward(self, old_TeamVoting, team):
        reward = 0
        global TotalVoting
        curr_TeamVoting = TotalVoting
        if old_TeamVoting == curr_TeamVoting: #no change
                reward = 0

        if team == blueTeam:
            if old_TeamVoting > curr_TeamVoting: #define this variable 
                reward = 10 #  percentage increase in people voting is the multiplier
            if old_TeamVoting > curr_TeamVoting:
                reward = -10 * reward # percentage decrease in people voting is the multiplier
        if team == redTeam:
            if old_TeamNotVoting > curr_TeamNotVoting: #define this variable 
                reward = 10 * X # percentage increase in people voting is the multiplier
            if old_TeamNotVoting > curr_TeamNotVoting:
                reward = -10 * X # percentage decrease in people voting is the multiplier
        return reward
