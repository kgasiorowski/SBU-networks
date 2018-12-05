CSE310 Homework 3 Readme

Kuba Gasiorowski
10977237

Bellman-Ford Algorithm program

Simply run the program from the command line, and give the file name which contains
the graph's edges. The file must reside in the same directory as the program. The 
program creates a graph object and populates it with the file. It then runs the 
algorithm on the set of edges, which populates both the array of lowest distances 
from x, as well as the predecessor which has the lowest cost for that node according 
to the algorithm.

The program then prints the distance, and using the list of predecessors it traces back
from the destination node to the source and prints out the path it generates. Note that
in this version of the script, 'x' and 'y' are hard-coded but can be easily changed
to represent any other node in the graph.

Note: This script was written using Python 3.