from queue import PriorityQueue

class PathPlanner:
    """Construct a PathPlanner Object"""
    def __init__(self, graph, start=None, goal=None):
        """Initialize the PathPlanner with a graph, start, and goal nodes"""
        self.graph = graph
        self.start = start
        self.goal = goal
        self.path = self.run_search() if start is not None and goal is not None else None

    def heuristic_cost_estimate(self, node, goal):
        """Manhattan distance heuristic for grid-based graphs"""
        x1, y1 = node
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current):
        """Reconstructs path from goal to start"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    def run_search(self):
        """Run A* algorithm to find the shortest path"""
        if self.start not in self.graph.nodes or self.goal not in self.graph.nodes:
            raise ValueError("Start or goal node not in the graph!")

        # A* algorithm initialization
        open_set = PriorityQueue() # Store nodes to be explored prioritised by f-score
        open_set.put((0, self.start))
        came_from = {} # Dictionary for each node points to the node it was reached from
        
        # g score to hold the cost of reaching each node from the start node
        g_score = {node: float('inf') for node in self.graph.nodes}
        g_score[self.start] = 0

        # f score to hold the estimated total cost from start to goal through each node
        f_score = {node: float('inf') for node in self.graph.nodes}
        f_score[self.start] = self.heuristic_cost_estimate(self.start, self.goal)

        while not open_set.empty():
            _, current = open_set.get()

            if current == self.goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.graph.neighbors(current):
                tentative_g_score = g_score[current] + 1  # Assuming uniform edge weights
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic_cost_estimate(neighbor, self.goal)
                    open_set.put((f_score[neighbor], neighbor))

        print("No path found!")
        return None
