from collections import deque


class Kruskal:
    def __init__(self, graph):
        self.graph = graph
        self.parent = [i for i in range(graph.number_of_vertices)]
        self.size = [0 for i in range(len(self.parent))]
        self.weight = 0

    def find(self, vertex):
        if self.parent[vertex] == vertex:
            return vertex
        self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, xr, yr):
        if self.size[xr] <= self.size[yr]:
            self.parent[xr] = self.parent[yr]
            self.size[yr] += self.size[xr]
        else:
            self.parent[yr] = self.parent[xr]
            self.size[xr] += self.size[yr]

    def apply(self):
        edges = self.graph.sort_edges()
        result = []
        for edge in edges:
            if len(result) == (len(self.parent) - 1):
                break
            xr = self.find(edge[0] - 1)
            yr = self.find(edge[1] - 1)

            if xr != yr:
                self.union(xr, yr)
                self.weight += edge[2]
                result.append(edge)
        return result


class Graph:

    def __init__(self, number_of_vertices=0):
        self.vertices = []
        self.edges = []
        self.number_of_edges = 0
        self.number_of_vertices = 0
        self.terminals = {}
        self.first_terminal = None

    def sort_edges(self):
        self.edges.sort(key=lambda edge: edge[2])
        return self.edges

    def print_edges(self):
        for edge in self.edges:
            print(edge)

    def read_file(self, filename):
        file = open(filename)
        f = iter(file)
        # find graph info
        while next(f)[:13] != 'SECTION Graph':
            continue

        # number of nodes
        self.number_of_vertices = int(next(f).split(' ')[1])
        # self.vertices = [i for i in range(1, self.number_of_vertices + 1)]

        # edges
        self.number_of_edges = int(next(f).split(' ')[1])
        for i in range(self.number_of_edges):
            e = next(f).split(' ')
            u = int(e[1])
            v = int(e[2])
            w = int(e[3])
            self.edges.append([u, v, w])
        # terminals
        e = 0
        while e != 'Section Terminals\n':
            e = next(f)
        number_of_terminals = int(next(f).split(' ')[1])
        # first shows if node is terminal second shows if it was visited in bfs
        terminals = []
        for i in range(self.number_of_vertices + 1):
            terminals.append([False, False])

        self.first_terminal = int(next(f).split(' ')[1])
        terminals[self.first_terminal][0] = True

        for i in range(1, number_of_terminals):
            terminals[int(next(f).split(' ')[1])][0] = True
        self.terminals = terminals
        file.close()


class Steiner:
    def __init__(self, edges, graph):
        self.edges = edges
        self.root = None
        self.result = []
        self.weight = 0
        self.first_terminal = graph.first_terminal
        self.vertices_info = graph.terminals
        self.graph = [deque() for i in range(graph.number_of_vertices + 1)]

    def add_edge(self, u, v, weight):
        self.graph[u].append([v, weight])
        self.graph[v].append([u, weight])

    def apply(self):
        self.create_tree(self.first_terminal)
        self.delete_edges(self.root)
        self.show_results(self.root)
        return self.result, self.weight

    def delete_edges(self, root):
        if not root.children:
            if self.vertices_info[root.value][0]:
                return 1
            return 0
        summation = 0

        # check first child
        while not summation and root.children:
            summation += self.delete_edges(root.children)
            if summation:
                break
            root.delete_first_child()

        curr = root.children
        while curr and curr.next:
            res = self.delete_edges(curr.next)
            summation += res
            if not res:
                curr.delete_next()
                continue
            curr = curr.next
        if self.vertices_info[root.value][0]:
            return summation + 1
        return summation

    def create_tree(self, s):
        for edge in self.edges:
            self.add_edge(edge[0], edge[1], edge[2])

        # unvisited is specified in self.vertices_info

        # Create a queue for BFS
        queue = deque()

        # Mark the source node as
        # visited and enqueue it
        self.root = Node(s)
        self.vertices_info[s][1] = True
        queue.append(self.root)
        while queue:

            # Dequeue a vertex
            vertex = queue.popleft()

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[vertex.value]:
                if not self.vertices_info[i[0]][1]:
                    new = Node(i[0])
                    vertex.add_child(new, i[1])
                    queue.append(new)
                    self.vertices_info[i[0]][1] = True

    def show_results(self, root):
        if not root.children:
            return
        curr = root.children
        while curr:
            self.result.append([root.value, curr.value])
            self.weight += curr.weight
            self.show_results(curr)
            curr = curr.next


class Node:
    def __init__(self, value):
        self.next = None
        self.value = value
        self.children = None
        self.weight = None
        self.last_child = None

    def add_child(self, node, weight):
        node.weight = weight
        if not self.children:
            self.children = node
            self.last_child = node
            return
        curr = self.children
        # while curr.next:
        #     curr = curr.next
        # curr.next = node
        last = self.last_child
        last.next = node
        self.last_child = node

    def delete_next(self):
        self.next = self.next.next

    def delete_first_child(self):
        self.children = self.children.next
