# # A class to represent the adjacency list of the nodes
# from user_input import NumberOfGreenNodes

class AdjNode:
    def __init__(self, data, WillVote, team, certainty, friends):
        self.vertex = data
        self.IgnoreRed = False
        self.WillVote = WillVote
        self.team = team
        self.certainty = certainty
        self.connections = friends
        self.next = None

# A class to represent a graph. A graph is the list of the adjacency lists.
# Size of the array will be the number of the vertices "V"
class Graph:
    def __init__(self, NumberOfGreenNodes):
        self.V = NumberOfGreenNodes
        self.newgraph = [None] * self.V

    # Function to add an edge in an undirected graph
    def add_edge(self, src, dest):
        # Adding the node to the source node
        node = AdjNode(dest)
        node.next = self.newgraph[src]
        self.newgraph[src] = node

        # Adding the source node to the destination as
        # it is the undirected graph
        node = AdjNode(src)
        node.next = self.newgraph[dest]
        self.newgraph[dest] = node

    # Function to create the graph
    def create_graph(self):
        for i in range(self.V):
            for j in range(self.V):
                self.add_edge(i,j)
                

    # Function to print the graph
    def print_graph(self):
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.newgraph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")