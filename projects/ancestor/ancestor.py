import sys
sys.path.insert(0, '../graph')
from util import Queue
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
    # Iterate through ancestors list
        #for each tuple:
        #   if tuple[0] not in self.vertices, add tuple[0]
        #   if tuple[1] not in self.vertices, add tuple[1]
        #   self.add_edge(tuple[1], tuple[0])
    g = Graph()
    for pair in ancestors:
        if pair[0] not in g.vertices:
            g.add_vertex(pair[0])
        if pair[1] not in g.vertices:
            g.add_vertex(pair[1])
        g.add_edge(pair[1], pair[0])

    # once the graph is built, bft to explore the graph and see what we get...
    q = Queue()
    q.enqueue(starting_node)
    # keep track of visited nodes
    visited = set()
    # repeat until queue is empty
    while q.size() > 0:

        # dequeue first vert
        current_vertex = q.dequeue()

        # if it's not visited:
        if current_vertex not in visited:
            visited.add(current_vertex)
        # add neighbors to queue
            for next_vertex in g.get_neighbors(current_vertex):
                q.enqueue(next_vertex)
    for vertex in visited:
        print(vertex)

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
earliest_ancestor(test_ancestors, 6)