from matplotlib import pyplot as plt
import random
from collections import namedtuple
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp


# User inputed Variables
NumberOfNodes = 30  # Population size of Green
ProbabilityOfConnection = 0.4  # Determines connectivity of the graph
NumberOfGreyAgents = (
    5  # Number of times Blue can introduce a foreign power to the population
)
RedSpyProportion = 0.75  # How likely is a foreign power to be bad

# Certainty related variables:
# LowCertainty is the certainty below which the agents know a node will NOT vote in the election
# HighCertainty is the certainty above which the agents know a node will vote in the election
# # A certainty level, above which a green node will  vote in the election.
#
LowCertainty = -0.3
HighCertainty = 0.3
VoteThreshold = (
    HighCertainty + LowCertainty
) / 2  # A certainty level, above which a green node will vote in the election.
MaxCertainty = 1.0
MinCertainty = -1.0

# Tolerance related variables:
# Standard deviation determines the spread of tolerances produced
# Average tolerance sets the mean, anchoring the distribution
# ToleranceFloat creates a normal distribution of tolerance value's to be given to each member of the green population.
# Tolerance converts array of floats into an array of integers.
StandardTolerance = 9
AverageTolerance = 60
ToleranceFloat = np.random.normal(AverageTolerance, StandardTolerance, NumberOfNodes)
Tolerance = ToleranceFloat.astype(int)

# TODO: uncomment to set the turns when testing
# self.PLAYER = 0
# self.AI = 1

TotalVoting = 0  #
TotalNotVoting = 0  #
blueTeam = 0  #
redTeam = 1  #
multiplierDict = (
    {  # Dictionary containing each move and it's corresponding potency value
        0: 0.01,
        1: 0.03,
        2: 0.09,
        3: 0.33,
        4: 0.99,
    }
)

reward = 0

# Australian Liberal/Labour expenses on political advertisement in 2022
StartingBudgetAUD = 250000
CurrentBalance = StartingBudgetAUD
CostOfMove = 0

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
        global NumberOfNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty, VoteThreshold, StandardTolerance, AverageTolerance

        NumberOfNodes = int(input("Enter the population of Greenland: "))
        ProbabilityOfConnection = float(
            input(
                "Enter the probability of a connection between any given Greenlander: "
            )
        )
        NumberOfGreyAgents = int(input("Enter Number of Foreign Agents: "))
        RedSpyProportion = float(
            input("Enter the proportion of Red Spies within the Foreign Agents: ")
        )
        LowCertainty, HighCertainty = [
            float(x)
            for x in input(
                "Enter the uncertainty interval of the Greenlanders. (e.g. [-0.1,0.1] or [-0.5,0.7]): "
            ).split(",")
        ]
        self.NumberOfNodes = NumberOfNodes
        self.NumberOfGreyAgents = NumberOfGreyAgents
        self.score = 0
        self.isGrey = False
        self.round = 0
        self.AI = 0
        self.PLAYER = 1
        self.WhoWon = self.AI
        VoteThreshold = (HighCertainty + LowCertainty) / 2
        ToleranceFloat = np.random.normal(
            AverageTolerance, StandardTolerance, self.NumberOfNodes
        )  # Creates a normal distribution of tolerance value's to be given to each member of the green population.
        Tolerance = ToleranceFloat.astype(int)

        print(
            "Population of Greenland: " + str(NumberOfNodes) + "\n",
            "Probability of a connection between any given Greenlander: "
            + str(ProbabilityOfConnection)
            + "\n",
            "Number of Foreign Agents: " + str(NumberOfGreyAgents) + "\n",
            "Proportion of Red Spies among the Foreign Agents: "
            + str(RedSpyProportion)
            + "\n",
            "Uncertainty interval of the Greenlanders: "
            + str(LowCertainty)
            + ", "
            + str(HighCertainty)
            + "\n",
        )

        # Create the graph.
        self.G = nx.gnp_random_graph(NumberOfNodes, ProbabilityOfConnection)

        # Initialise the graph, assign each node the relevent information.
        for i in self.G.nodes:
            self.G.nodes[i]["Team"] = "Green"
            self.G.nodes[i]["Certainty"] = random.uniform(LowCertainty, HighCertainty)
            self.G.nodes[i]["Will Vote"] = None  # add update_node function
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
        NodesVoting.clear()
        # A list of nodes that are NOT going to vote
        NodesNotVoting = []
        NodesNotVoting.clear()

        for (p, d) in graph.nodes(data=True):
            # If the node will vote
            if d["Certainty"] >= VoteThreshold:
                NodesVoting.append(True)
                d["Will Vote"] = True
            # If the node wont vote
            if d["Certainty"] < VoteThreshold:
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
        global turn, TotalVoting, TotalNotVoting, StartingBudgetAUD, CurrentBalance, Tolerance

        print("\nNEW GAME\n")
        # init game state
        self.G.clear()
        plt.clf()
        nx.draw(self.G, node_color="Green", with_labels=1)

        self.G = nx.gnp_random_graph(NumberOfNodes, ProbabilityOfConnection)
        ToleranceFloat = np.random.normal(
            AverageTolerance, StandardTolerance, self.NumberOfNodes
        )  # Creates a normal distribution of tolerance value's to be given to each member of the green population.
        Tolerance = ToleranceFloat.astype(int)

        for i in self.G.nodes:
            self.G.nodes[i]["Team"] = "Green"
            self.G.nodes[i]["Certainty"] = random.uniform(LowCertainty, HighCertainty)
            self.G.nodes[i]["Will Vote"] = None
            self.G.nodes[i]["Ignore Red"] = False
            self.G.nodes[i]["Tolerance"] = Tolerance[i]
        self._update_will_vote_values(self.G)

        # Build internal representation of the graph.
        nx.draw(self.G, node_color="Green", with_labels=1)

        # Generate user interface of the graph.
        plt.show()

        self.round = 0
        TotalVoting = 0
        TotalNotVoting = 0
        StartingBudgetAUD = 250000
        CurrentBalance = StartingBudgetAUD
        self.NumberOfGreyAgents = NumberOfGreyAgents

        # TODO  Add this back for randomising who is what team, Comment out for testing
        self.PLAYER = random.randint(blueTeam, redTeam)
        if self.PLAYER == redTeam:
            self.PLAYER = redTeam
            self.AI = blueTeam
        else:
            self.PLAYER = blueTeam
            self.AI = redTeam
        turn = redTeam

        # TODO: add back for testing
        # self.AI = 0  # TODO: CHANGE ME to 0 for Blue and 1 for Red
        # self.PLAYER = 1  # TODO: CHANGE ME to 0 for Blue and 1 for Red
        return self.PLAYER, self.AI

    # If the game has run its' course, stop and return the current score.
    # Otherwise, play a move and update the GUI.
    def play_step(self, action, turn):
        global TotalVoting, TotalNotVoting
        print("\n\nVoting: ", TotalVoting)
        print("Not Voting: ", TotalNotVoting, "\n\n")

        old_TeamVoting = TotalVoting
        old_TeamNotVoting = TotalNotVoting

        if self.round_limit(self.round):
            game_over = True
            reward = self._get_reward(
                old_TeamVoting, old_TeamNotVoting, turn, game_over
            )
            return reward, game_over, self.score

        # Plays a move based upon the users input
        if turn == self.PLAYER:
            # self._move(action, self.PLAYER) #TODO: Possibly remove this as it plays on behalf of the player?
            game_over = False
            self.round += 0.5

            if self.round_limit(self.round):
                game_over = True
                reward = self._get_reward(
                    old_TeamVoting, old_TeamNotVoting, turn, game_over
                )
                return game_over

            self._update_ui()
            # self.update_graph(self.G)
            if self.isGrey == True:
                self.isGrey = False
            return game_over

        if turn == self.AI:
            self._move(action, self.AI)  # Choose move (update the head)
            # 3. check if game over
            game_over = False
            self.score = self.get_score(self.score)

            # 4. place new food or just move
            # old_reward = reward
            reward = self._get_reward(
                old_TeamVoting, old_TeamNotVoting, turn, game_over
            )

            # 5. update ui and clock
            self._update_ui()
            # self.update_graph(self.G)
            # self.clock.tick(SPEED)
            if self.isGrey == True:
                self.isGrey = False

            self.round += 0.5
            # If Game is finished
            if self.round_limit(self.round):
                game_over = True
                reward = self._get_reward(
                    old_TeamVoting, old_TeamNotVoting, turn, game_over
                )
                return reward, game_over, self.score

            # 6. return game over and score

            return reward, game_over, self.score

    def get_score(self, score):
        global TotalVoting, TotalNotVoting
        if self.AI == blueTeam:
            # if TotalVoting > TotalNotVoting:
            #     score += 1
            # else:
            # score = -1

            score = TotalVoting - TotalNotVoting
        if self.AI == redTeam:
            #     if TotalNotVoting > TotalVoting:
            #         score += 1
            # else:
            #         score = -1

            score = TotalNotVoting - TotalVoting
        return score

    # Checker function to see if the game has finished.
    def round_limit(self, round):
        if round >= 7:  # ELECTION WEEK!
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
        for i in self.G.nodes():
            # Who are the current nodes neighbours?
            neighbors = list(self.G.neighbors(i))
            # Iterate through the neighbours this node hasn't interacted with yet
            for j in range(len(neighbors)):
                if neighbors[j] > i:
                    CurrentNodeCertainty = self.G.nodes[i]["Certainty"]
                    NeighbourNodeCertainty = self.G.nodes[neighbors[j]]["Certainty"]
                    # Move the less certain node halfway toward the more certain node
                    if abs(CurrentNodeCertainty) < abs(NeighbourNodeCertainty):
                        CurrentNodeCertainty = (
                            CurrentNodeCertainty + NeighbourNodeCertainty
                        ) / 2
                    else:
                        NeighbourNodeCertainty = (
                            NeighbourNodeCertainty + CurrentNodeCertainty
                        ) / 2

    # Updates the game state voting totals so reward/punishment may be decided for each agent.
    def _update_voting_totals(self, node_id, PrevCertainty, action, team):
        global TotalVoting
        global TotalNotVoting
        node = self.G.nodes[node_id]

        if node["Certainty"] <= LowCertainty and PrevCertainty > LowCertainty:
            TotalNotVoting += 1

        if PrevCertainty <= LowCertainty and node["Certainty"] > LowCertainty:
            TotalNotVoting -= 1

        if node["Certainty"] >= HighCertainty and PrevCertainty < HighCertainty:
            TotalVoting += 1

        if PrevCertainty >= HighCertainty and node["Certainty"] < HighCertainty:
            TotalVoting -= 1

        if node["Certainty"] > HighCertainty and node["Certainty"] < LowCertainty:
            pass

    def _who_hates_red(self, action, node_id):
        node = self.G.nodes[node_id]
        # From Reds message potency, e.g. 1.x, x*10 becomes the chance of ignoring red team members.
        IgnoreRedchance = action * 10
        # Green nodes only ignore Red when their certainty value is positive (leaning toward voting).
        # If the Green node doesn't tolerate Red's nonsense, they will ignore them.
        if IgnoreRedchance >= node["Tolerance"]:
            node["Ignore Red"] = True
        # If they tolerate a bit, leave whether they ignore Red to chance (nonsense / tolerance of respective node).
        else:
            node["Ignore Red"] = random.random() < (IgnoreRedchance / node["Tolerance"])
        return node["Ignore Red"]

    # Calls the relevant functions based upon the move selected by the player or agent.
    def _calc_valid_move(self, action):
        if action == 6:
            return True
        if action > 5:
            return False
        if action == 5 and self.NumberOfGreyAgents != 0:
            return True
        if action == 5 and self.NumberOfGreyAgents == 0:
            return False
        temp_CostOfMove = StartingBudgetAUD * multiplierDict[action]
        if CurrentBalance >= temp_CostOfMove:
            return True
        if CurrentBalance < temp_CostOfMove and self.NumberOfGreyAgents == 0:
            return 6
        if CurrentBalance == 0:
            return 6
        if action == 6:
            return True
        else:
            print("You do not have enough money :( Try another move\n")
            return False

    def _move(self, action, team):
        global StartingBudgetAUD, CurrentBalance, round, reward, MaxCertainty, MinCertainty
        if action <= 4:

            if team == blueTeam:
                CostOfMove = StartingBudgetAUD * multiplierDict[action]
                if CurrentBalance >= CostOfMove:
                    for (
                        n
                    ) in (
                        self.G.nodes
                    ):  # add multiplier for each message level then affect blue budget
                        PrevWillVote = self.G.nodes[n]["Will Vote"]
                        PrevCertainty = self.G.nodes[n]["Certainty"]
                        self.G.nodes[n]["Certainty"] += (
                            abs(self.G.nodes[n]["Certainty"]) * multiplierDict[action]
                        )
                        if self.G.nodes[n]["Certainty"] > HighCertainty:
                            self.G.nodes[n]["Will Vote"] = True

                        if self.G.nodes[n]["Certainty"] < LowCertainty:
                            self.G.nodes[n]["Will Vote"] = True

                        if self.G.nodes[n]["Certainty"] > MaxCertainty:
                            self.G.nodes[n]["Certainty"] = MaxCertainty
                    self._update_voting_totals(
                        n, PrevCertainty, multiplierDict[action], blueTeam
                    )
                    # Subtract the cost of the move from the budget.
                    if self.isGrey == False:
                        CurrentBalance -= CostOfMove
                    self._green_interact()

                    # round += 1
            # Intrduce a foreign power into the game.
        elif team == blueTeam and action == 5 and self.isGrey == False:
            self.isGrey = True
            grey_type = 0
            # TODO: introduce_grey_agent()
            if self.PLAYER == 0:
                if random.random() > RedSpyProportion:
                    grey_type = blueTeam
            if self.PLAYER == 1:
                if random.random() < RedSpyProportion:
                    grey_type = redTeam
            grey_action = random.randint(0, 4)
            self.NumberOfGreyAgents -= 1
            self.play_step(grey_action, grey_type)

        # Skip blue teams turn.
        elif team == blueTeam and action == 6:
            pass

        if team == redTeam:
            for (
                n
            ) in (
                self.G.nodes
            ):  # add multiplier for each message level then affect blue budget
                PrevCertainty = self.G.nodes[n]["Certainty"]

                if self.isGrey == False and not self._who_hates_red(action, n):
                    self.G.nodes[n]["Certainty"] -= (
                        abs(self.G.nodes[n]["Certainty"]) * multiplierDict[action]
                    )

                if self.G.nodes[n]["Certainty"] < MinCertainty:
                    self.G.nodes[n]["Certainty"] = MinCertainty
            self._green_interact()
            self._update_voting_totals(
                n, PrevCertainty, multiplierDict[action], redTeam
            )

    # Gifts a reasonable reward or punishment to the agent based upon changes to the voting totals.
    def _get_reward(self, old_TeamVoting, old_TeamNotVoting, team, game_over):
        global TotalVoting, TotalNotVoting
        # Give a big reward if AI wins, otherwise give negative reinforcement
        if game_over:
            if self.AI == blueTeam:
                if TotalVoting > TotalNotVoting:
                    reward = 100
                    self.WhoWon = self.AI
                    # AI WINS !
                    return reward
                if TotalVoting < TotalNotVoting:
                    reward = -100
                    self.WhoWon = self.PLAYER
                    # AI LOSES !
                    return reward
            if self.AI == redTeam:
                if TotalVoting > TotalNotVoting:
                    reward = -100
                    self.WhoWon = self.PLAYER
                    # AI LOSES !
                    return reward
                if TotalVoting < TotalNotVoting:
                    reward = 100
                    self.WhoWon = self.AI
                    # AI WINS !
                    return reward

        # Reset the reward from the previous player
        reward = 0

        curr_TeamVoting = TotalVoting
        curr_TeamNotVoting = TotalNotVoting

        # Safety net for diving by 0
        if old_TeamVoting == 0:
            old_TeamVoting = 1
        if old_TeamNotVoting == 0:
            old_TeamNotVoting = 1

        # calculate how big the reward Would be:
        PercentageChangeInVoters = curr_TeamVoting / old_TeamVoting
        PercentageChangeInNonVoters = curr_TeamNotVoting / old_TeamNotVoting

        # More people (appear to be?) voting
        if old_TeamVoting < curr_TeamVoting:
            if team == blueTeam:
                reward += 10 * PercentageChangeInVoters
            if team == redTeam:
                reward -= 10 * PercentageChangeInVoters

        # Less people (appear to be?) voting
        if old_TeamVoting > curr_TeamVoting:
            if team == blueTeam:
                reward -= 10 * PercentageChangeInVoters
            if team == redTeam:
                reward += 10 * PercentageChangeInVoters

        # More people (appear to be?) NOT voting
        if old_TeamNotVoting > curr_TeamNotVoting:
            if team == blueTeam:
                reward += 10 * PercentageChangeInNonVoters
            if team == redTeam:
                reward -= 10 * PercentageChangeInNonVoters

        # Less people (appear to be?) NOT voting
        if old_TeamNotVoting > curr_TeamNotVoting:
            if team == blueTeam:
                reward += 10 * PercentageChangeInNonVoters
            if team == redTeam:
                reward -= 10 * PercentageChangeInNonVoters
        return reward
