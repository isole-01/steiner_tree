from collections import deque
from collections import defaultdict


class Kruskal:
    def __init__(self, graph):
        self.graph = graph
        self.parent = [i for i in range(len(graph.get_vertices()))]
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

    def get_vertices(self):
        return self.vertices

    def sort_edges(self):
        self.edges.sort(key=lambda edge: edge[2])
        return self.edges

    def print_edges(self):
        for edge in self.edges:
            print(edge)

    def read_file(self, filename):
        file = open('PUC/' + filename)
        f = iter(file)
        # find graph info
        while next(f)[:13] != 'SECTION Graph':
            continue

        # number of nodes
        self.number_of_vertices = int(next(f).split(' ')[1])
        self.vertices = [i for i in range(1, self.number_of_vertices + 1)]

        # edges
        self.number_of_edges = int(next(f).split(' ')[1])
        for i in range(self.number_of_edges):
            e = next(f).split(' ')
            u = int(e[1])
            v = int(e[2])
            w = int(e[3])
            if u > v:
                self.edges.append([v, u, w])
            else:
                self.edges.append([u, v, w])
        # terminals
        e = 0
        while e != 'Section Terminals\n':
            e = next(f)
        number_of_terminals = int(next(f).split(' ')[1])
        terminals = {}

        for i in range(number_of_terminals):
            terminals[int(next(f).split(' ')[1])] = True
        self.terminals = terminals
        file.close()


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node, weight):
        self.children.append([node, weight])


class Steiner:
    def __init__(self, edges, terminals):
        self.edges = edges
        self.terminals = terminals
        self.graph = defaultdict(list)

    def add_edge(self, u, v, weight):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def remove_edge(self, u, v):
        self.graph[u].remove(v)
        self.graph[v].remove(u)

    def remove_leaf(self, key):
        ls = self.graph[key]
        if len(ls) != 1 or key in self.terminals:
            return
        nextKey = ls[0]
        self.remove_edge(key, ls[0])
        return self.remove_leaf(nextKey)

    def apply(self):
        for edge in self.edges:
            self.add_edge(edge[0], edge[1], edge[2])
        for key in self.graph:
            self.remove_leaf(key)
        print(self.graph)
