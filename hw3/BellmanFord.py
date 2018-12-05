class Graph:

    def __init__(self, filename):
        self.vertList = []
        self.graph = []  # default dictionary to store graph
        self.dist = {}
        self.predecessors = {}  # keep track of predecessors here

        # Populate the graph with text file
        with open(filename, 'r') as file:
            line = file.readline()

            while line:
                parsedInput = [x.strip() for x in line.split(',')]
                self.add_edge(parsedInput[0], parsedInput[1], int(parsedInput[2]))
                line = file.readline()

    def add_edge(self, src, dest, weight):

        if src not in self.vertList:
            self.vertList.append(src)

        if dest not in self.vertList:
            self.vertList.append(dest)

        self.graph.append([src, dest, weight])

    def bellman_ford(self, src):

        # Init distance vector
        self.dist = {}
        for vertex in self.vertList:
            self.dist[vertex] = float("inf")

        # Init predecessor array for path finding
        self.predecessors = {}
        for vertex in self.vertList:
            self.predecessors[vertex] = '-'

        self.dist[src] = 0

        for i in range(len(self.vertList) - 1):  # Iterate v-1 times
            for src, dest, weight in self.graph:  # For each edge
                if self.dist[src] != float("Inf") and self.dist[src] + weight < self.dist[dest]:
                    self.dist[dest] = self.dist[src] + weight  # Update distance
                    self.predecessors[dest] = src  # Update predecessors array

    def print_arrs(self):
        print("Vertex   Distance from Source")
        for key, value in self.dist.items():
            print("{0} \t\t {1}".format(key, value))

        print()

        print("Dest Src")
        for key, value in self.predecessors.items():
            print("{} {}".format(key, value))

    def get_dist_to(self, __node):
        if __node not in self.vertList:
            return

        return self.dist[__node]

    def print_path_to(self, dest):
        if dest not in self.vertList:
            return

        nodepath = []

        while dest is not '-':
            nodepath.append(dest)
            dest = self.predecessors[dest]

        return reversed(nodepath)

if __name__ == "__main__":

    # Initialize a graph
    g = Graph('test.txt')

    # Run bellman_ford on the graph
    g.bellman_ford('x')

    # Get the stats
    dist = g.get_dist_to('y')
    path = g.print_path_to('y')

    print("Shortest distance from x to y: {0}".format(dist))
    print("Shortest path from x to y: ", end='')

    for node in path:
        print("{0} ".format(node), end='')
