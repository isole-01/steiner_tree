# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.
from collections import defaultdict


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node, weight):
        self.children.append([node, weight])

def preorder(root):
# This class represents a directed graph
# using adjacency list representation
class Graph:

    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.root = None

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    # Function to print a BFS of graph
    def BFS(self, s):

        # Mark all the vertices as not visited
        visited = {}
        for i in self.graph:
            visited[i] = False

        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        self.root = Node(s)
        visited[s] = True
        queue.append(self.root)
        while queue:

            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print(s, end=" ")

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s.value]:
                if not visited[i]:
                    new = Node(i)
                    s.add_child(new, 1)
                    queue.append(new)
                    visited[i] = True


# Driver code

# Create a graph given in
# the above diagram
g = Graph()
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 2)
g.addEdge(2, 3)
g.addEdge(3, 4)
g.addEdge(10, 0)

g.BFS(0)

print("Following is Breadth First Traversal"
      " (starting from vertex 2)")
# This code is contributed by Neelam Yadav
