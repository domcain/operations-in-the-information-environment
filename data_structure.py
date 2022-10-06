import user_input

NumberOfGreenNodes = user_input.get('NumberOfGreenNodes')
ProbabilityOfConnection = user_input.get('ProbabilityOfConnection')
NumberOfGreyAgents = user_input.get('NumberOfGreyAgents')
RedSpyProportion = user_input.get('RedSpyProportion')
Certainty = user_input.get('Certainty')

# A class to represent the adjacency list of the nodes
class AdjNode:
    def __init__(self, data, team, certainty, connections, ):
        self.vertex = data
        self.team = team
        self.certainty = certainty
        self.connections = connections
        self.next = None

# A class to represent a graph. A graph is the list of the adjacency lists.
# Size of the array will be the no. of the vertices "V"
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
                newgraph.add_edge(self,i,j)
                

    # Function to print the graph
    def print_graph(self):
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.newgraph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")


# Driver program to the above graph class
if __name__ == "__main__":
    V = 5
    newgraph = Graph(V, NumberOfGreenNodes)
    newgraph.create_graph()

    newgraph.print_graph()