import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # Add users
        for i in range(0, num_users):
            self.add_user(f"User {i}")
        # Create Frienships
        # Generate all possible friendship combinations
        possible_friendships = []
        # Avoid duplicates by ensuring the first number is smaller than the second
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))
        # Shuffle the possible friendships
        random.shuffle(possible_friendships)
        # Create friendships for the first X pairs of the list
        # X is determined by the formula: num_users * avg_friendships // 2
        # Need to divide by 2 since each add_friendship() creates 2 friendships
        count_add_friendship_calls = 0
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])
            count_add_friendship_calls += 1
        print("add_friendship() calls: ", count_add_friendship_calls)

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        q.enqueue(starting_vertex)
        # keep track of visited nodes
        visited = {}
        # repeat until queue is empty
        while q.size() > 0:

            # dequeue first vert
            current_vertex = q.dequeue()

            # if it's not visited:
            if current_vertex not in visited:
                visited[current_vertex] = self.friendships[current_vertex]
            # add neighbors to queue
                # print(f"friendships of {current_vertex}: ", self.friendships[current_vertex])
                for next_vertex in self.friendships[current_vertex]:
                    q.enqueue(next_vertex)
        return visited

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """

        # keep track of visited nodes
        visited = []
        queue = [[starting_vertex]]

        if starting_vertex == destination_vertex:
            return [starting_vertex]

        # repeat until queue is empty
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node not in visited:
                neighbors = self.friendships[node]
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    if neighbor == destination_vertex:
                        return new_path
                visited.append(node)

        return []

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        network = self.bft(user_id) # sub-graph island containing user
        connections = {} # store the final output
        for connection in network:
            connections[connection] = self.bfs(user_id, connection)
        self.network_percentage(network, connections)
        return connections

    def network_percentage(self, network, connections):
        print("Number of users", len(self.users))
        print("Number of connections: ", len(network))
        percentage = int((len(network) / len(self.users)) * 100)
        print(f"Percentage of Network: {percentage}%")

        lengths = []
        for connection in connections:
            lengths.append(len(connections[connection]) - 1)
            # print(connections[connection])
        average = sum(lengths) // len(lengths)
        print(f"Average Degrees of separation: {average}")




if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    sg.users
    # print("Friendships: ", sg.friendships)
    connections = sg.get_all_social_paths(1)
    # print("Connections: ", connections)
