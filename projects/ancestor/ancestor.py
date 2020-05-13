from util import Queue, Stack
class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set() # set of edges

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Vertex does not exist in graph")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

def earliest_ancestor(ancestors, starting_node):
    g = Graph() # instance of Graph
    # Iterate through ancestors list and add all the given IDs as vertices
    for pair in ancestors:
        if pair[0] not in g.vertices:
            g.add_vertex(pair[0])
        if pair[1] not in g.vertices:
            g.add_vertex(pair[1])
        g.add_edge(pair[1], pair[0]) # connects the vertices as indicated by given tuples

    #------- DFT Setup -------#
    stack = Stack()
    stack.push(starting_node)
    visited = set()
    potential_paths = []

    def dft(starting_vertex, visited, path):
        if starting_vertex not in visited:
            visited.add(starting_vertex) #marks vertex as visited
            path = path + [starting_vertex] #creates a copy of path
            for next_vertex in g.get_neighbors(starting_vertex):
                dft(next_vertex, visited, path) #recursive call of dft
        # the first path found will be the longest/deepest
        if len(potential_paths) == 0:
            potential_paths.append(path) #add the longest path to list of potential paths
        elif len(potential_paths) > 0:
            # there might be a second path of equal length,
            # we'll need to save it too in case it has a lower index
            if len(path) == len(potential_paths[0]):
                potential_paths.append(path)
        # we can ignore the rest of the results of the DFT
        # since they'll be partial or shorter paths

    #------- Call DFT -------#
    dft(starting_node, visited, potential_paths)

    #------- Checks to return the correct last-node -------#
    # potential_paths now contains 1 or 2 lists which are the longest possible paths
    # if only one path, return the last node
    if len(potential_paths) == 1:
        output = potential_paths[0][-1]
    # if two possible paths,
    # return the last-node with the lower index value
    else:
        if potential_paths[0][-1] < potential_paths[1][-1]:
            output = potential_paths[0][-1]
        else:
            output = potential_paths[1][-1]
    # if last-node is same as starting-node, no ancestors
    # return -1 as per spec
    if output == starting_node:
        output = -1
    return output

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors, 2))