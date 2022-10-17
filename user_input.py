# from data_structure import AdjNode, Graph
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
greenTeam   = 2
greyTeam    = 3

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
TotalNumberOfNodes = (NumberOfGreenNodes + NumberOfGreyAgents + NumberOfRedAgents + NumberOfBlueAgents)

G = nx.complete_graph(TotalNumberOfNodes)
color_map = ['blue' if nodes == blueTeam else 'red' if nodes == redTeam else 'green' for nodes in G]

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

# def random_yes_no(percent):
#     return random.randrange(1) < percent

# # function to decide which team a node should be assigned according to a set distribution
# def assign_team():
#     global teams, greenTeam, blueTeam, redTeam, greyTeam
#     count = 0
#     # while we haven't assigned each node a team
#     while count < TotalNumberOfNodes:
        
#         count += 1
#     return team

# user_input()
# newgraph = Graph(NumberOfGreenNodes)

# # Function to create the graph, and assign relevent values 
# # to each node in the process
# def populate_edges(Graph):
#     for i in range(NumberOfGreenNodes):
#         # Appropriately assign randomised values to each node
#         Graph.team = greenTeam
#         Graph.certainty = random.uniform(LowCertainty, HighCertainty)
#         Graph.willVote = random_yes_no(0.3)
#         Graph.ignoreRed = random_yes_no(0.1)
#         for j in range(NumberOfGreenNodes):
#             Graph.add_edge(i,j)
#             print(Graph.add_edge(i, j))
#     return newgraph
                
# # Driver program to the above graph class    
# populate_edges(newgraph)
# newgraph.print_graph()