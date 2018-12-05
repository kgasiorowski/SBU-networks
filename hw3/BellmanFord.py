# CSE310 Homework 3
# Kuba Gasiorowski
# 109776237


class Graph:

    def __init__(self, __filename):
        self.vertList = []  # Here is the list of vertices
        self.edge_list = []  # Here is the list of edges
        self.dist = {}  # Dictionary of distances from designated source node
        self.predecessors = {}  # Dictionary of lowest-cost predecessors per each node

        # Populate the graph with text file
        with open(__filename, 'r') as file:

            line = file.readline()
            while line:
                # Extract the values we need from each line
                parsedInput = [x.strip() for x in line.split(',')]
                src_node = parsedInput[0]
                dest_node = parsedInput[1]
                edge_weight = int(parsedInput[2])

                # If src is a new node, add it to the list
                if src_node not in self.vertList:
                    self.vertList.append(src_node)

                # If dest is a new node, add it to the list
                if dest_node not in self.vertList:
                    self.vertList.append(dest_node)
                # Finally add the whole edge to the graph
                self.edge_list.append([src_node, dest_node, edge_weight])
                # Read the next line
                line = file.readline()

    # Runs the bellman ford algorithm on the graph
    def run_bellman_ford(self, initial_node):

        # Init distance vector
        self.dist = {}
        for vertex in self.vertList:
            self.dist[vertex] = float("inf")

        # Init predecessor array for path finding
        self.predecessors = {}
        for vertex in self.vertList:
            self.predecessors[vertex] = '-'

        # Initialize the origin node to 0, so the algorithm knows where to start
        self.dist[initial_node] = 0

        for i in range(len(self.vertList) - 1):  # Iterate v-1 times
            for src_node, dest_node, edge_weight in self.edge_list:  # For each edge
                if self.dist[src_node] != float("Inf") and self.dist[src_node] + edge_weight < self.dist[dest_node]:
                    self.dist[dest_node] = self.dist[src_node] + edge_weight  # Update distance
                    self.predecessors[dest_node] = src_node  # Update predecessors array

    # Returns the raw distance from the source to the destination node
    def get_dist_to(self, dest_node):
        if dest_node not in self.vertList:
            return

        return self.dist[dest_node]

    # Returns the path from the source to the destination node
    def get_path_to(self, dest_node):
        if dest_node not in self.vertList:
            return

        nodepath = []

        # Traces back from destination to source. '-' means source has been reached
        while dest_node is not '-':
            nodepath.append(dest_node)
            dest_node = self.predecessors[dest_node]

        # Return the array reversed
        return reversed(nodepath)


if __name__ == "__main__":

    filename = input("Enter the graph file: ")

    # Initialize a graph
    try:
        g = Graph(filename)
    except FileNotFoundError:
        print("Error: File was not found")
        exit(0)

    # Run bellman-ford on the graph
    g.run_bellman_ford('x')

    # Get the stats
    dist = g.get_dist_to('y')
    path = g.get_path_to('y')

    print("Shortest distance from x to y: {0}".format(dist))
    print("Shortest path from x to y: ", end='')

    for node in path:
        print("{0} ".format(node), end='')
