from data_structure import AdjNode, Graph

NumberOfGreenNodes = None
ProbabilityOfConnection = None
NumberOfGreyAgents = None
RedSpyProportion = None
LowCertainty = None
HighCertainty = None


def user_input():
    global NumberOfGreenNodes, ProbabilityOfConnection, NumberOfGreyAgents, RedSpyProportion, LowCertainty, HighCertainty
    NumberOfGreenNodes = int(input("Enter the size of the Green Team: "))
    ProbabilityOfConnection = float(
        input("Enter the probability of a connection between any given green player: ")
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
    # print(
    #     "Size of the Green Team: " + NumberOfGreenNodes + "\n",
    #     "Probability of a connection between any given green player: " + ProbabilityOfConnection + "\n",
    #     "Number of agents in the Grey Team: " + NumberOfGreyAgents + "\n",
    #     "Proportion of Red Spies within the Grey Team: " + RedSpyProportion + "\n",
    #     "Certainty interval of the Green Team: " + Certainty + "\n"
    # )


user_input()
newgraph = Graph(NumberOfGreenNodes)
# Function to create the graph
def populate_edges(Graph):
    for i in range(NumberOfGreenNodes):
        for j in range(NumberOfGreenNodes):
            Graph.add_edge(i, j)
            print(Graph.add_edge(i, j))
    return newgraph


# Driver program to the above graph class
populate_edges(newgraph)
newgraph.print_graph()
