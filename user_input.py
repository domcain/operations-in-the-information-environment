import random
import networkx as nx
import matplotlib.pyplot as plt

NumberOfRedAgents = 1
NumberOfBlueAgents = 1
NumberOfGreenNodes = None
ProbabilityOfConnection = None
NumberOfGreyAgents = None
RedSpyProportion = None
LowCertainty = None
HighCertainty = None
blueTeam    = 0
redTeam     = 1

# A function that iteratively asks the user for input parameters that will be used to construct the graph 
def user_input():
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

user_input()

# Variable used to construct the graph 
TotalNumberOfNodes = (NumberOfGreenNodes + NumberOfGreyAgents + NumberOfRedAgents + NumberOfBlueAgents)

# Create the graph
G = nx.complete_graph(TotalNumberOfNodes)

# Assign colours to the graph
color_map = ['blue' if nodes == blueTeam else 'red' if nodes == redTeam else 'green' for nodes in G]

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
    G.nodes[i]["Certainty"] = random.uniform(LowCertainty,HighCertainty)
    G.nodes[i]["Will Vote"] = False
    G.nodes[i]["Ignore Red"] = False

# Build internal representation of the graph
nx.draw(G, node_color=color_map, with_labels=1)

# Generate user interface of the graph  
plt.show()