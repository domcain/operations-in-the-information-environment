from data_structure import AdjNode, Graph
import random

NumberOfRedAgents = 1
NumberOfBlueAgents = 1
NumberOfGreenNodes = None
ProbabilityOfConnection = None
NumberOfGreyAgents = None
RedSpyProportion = None
LowCertainty = None
HighCertainty = None
TotalNumberOfNodes = NumberOfGreenNodes + NumberOfGreyAgents + NumberOfRedAgents + NumberOfBlueAgents

teams = [greenTeam, blueTeam, redTeam, greyTeam]
greenTeam   = 0
blueTeam    = 1
redTeam     = 2
greyTeam    = 3

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

def random_yes_no(percent):
    return random.randrange(1) < percent

def assign_team():
    global teams, greenTeam, blueTeam, redTeam, greyTeam
    count = 0
    while count < TotalNumberOfNodes:
        
        count += 1
    return team

user_input()
newgraph = Graph(NumberOfGreenNodes)

# Function to create the graph, and assign relevent values 
# to each node in the process
def populate_edges(Graph):
    for i in range(NumberOfGreenNodes):
        # Appropriately assign randomised values to each node
        Graph.team = greenTeam
        Graph.certainty = random.uniform(LowCertainty, HighCertainty)
        Graph.willVote = random_yes_no(0.3)
        Graph.ignoreRed = random_yes_no(0.1)
        for j in range(NumberOfGreenNodes):
            Graph.add_edge(i,j)
            print(Graph.add_edge(i, j))
    return newgraph
                
# Driver program to the above graph class    
populate_edges(newgraph)
newgraph.print_graph()