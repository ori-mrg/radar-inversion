import random
from .radar_processing import load_and_process_radar, create_binned_image, create_graph_from_binned_image
from .visualisation import plot_radar_image, plot_binned_image_and_graph, plot_path_on_graph
from src.path_planner import PathPlanner

# Parameters
radar_image_location = "./data/1547131046353776.png"
bin_size = 3
threshold = 0.08

# Step 1: Load and process radar image
image = load_and_process_radar(radar_image_location)
print(f"Image shape after squeezing: {image.shape}")
plot_radar_image(image)

# Step 2: Create binned image
binned_image = create_binned_image(image, bin_size, threshold)

# Step 3: Create graph from binned image
G = create_graph_from_binned_image(binned_image)

# Step 4: Visualize the binned image and graph
plot_binned_image_and_graph(binned_image, G)

# Step 5: Randomly select valid start and goal nodes
nodes = list(G.nodes)
start = (149, 95)
goal = (33, 75)
# start = random.choice(nodes)
# goal = random.choice(nodes)

print(f"Start Node: {start}, Goal Node: {goal}")

# Step 6: Find a path using PathPlanner
planner = PathPlanner(G, start=start, goal=goal)
path = planner.run_search()

# Step 7: Visualize the path
if path:
    print("Path:", path)
    plot_path_on_graph(G, path)
else:
    print("No path found!")
