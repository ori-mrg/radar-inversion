import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from src.radar import load_radar, radar_polar_to_cartesian
from src.path_planner import PathPlanner

# Load radar image
radar_image_location = "./data/1547131046353776.png"
_, azimuths, _, fft_data, radar_resolution = load_radar(radar_image_location)
image = radar_polar_to_cartesian(azimuths, fft_data, radar_resolution, cart_resolution=0.2, cart_pixel_width=500)

# Remove singleton channel dimension
image = np.squeeze(image)
print(f"Image shape after squeezing: {image.shape}")

# Display the radar image
plt.imshow(image, cmap='gray')
plt.title("Radar Image")
plt.show()

# Parameters for binning
bin_size = 3
threshold = 0.08

# Determine binned image dimensions
height, width = image.shape
binned_height = height // bin_size
binned_width = width // bin_size

# Create binned image
binned_image = np.zeros((binned_height, binned_width), dtype=int)

for i in range(binned_height):
    for j in range(binned_width):
        # Extract the bin
        bin_pixels = image[i * bin_size:(i + 1) * bin_size, j * bin_size:(j + 1) * bin_size]
        # Classify bin as 1 if any pixel exceeds the threshold, otherwise 0
        binned_image[i, j] = 1 if np.any(bin_pixels > threshold) else 0

# Function to validate a node
def is_valid_node(x, y):
    return 0 <= x < binned_height and 0 <= y < binned_width and binned_image[x, y] == 0

# Neighboring directions
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Create the graph from the binned image
G = nx.Graph()

for i in range(binned_height):
    for j in range(binned_width):
        if binned_image[i, j] == 0:  # Only consider nodes with value 0
            G.add_node((i, j))  # Add node for the bin
            for dx, dy in directions:
                ni, nj = i + dx, j + dy
                if is_valid_node(ni, nj):
                    G.add_edge((i, j), (ni, nj))  # Add edge to neighboring nodes

# Plot the binned image and graph
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(binned_image, cmap='gray')
plt.title("Binned Image")
plt.axis('off')

plt.subplot(1, 2, 2)
pos = {(i, j): (j, -i) for i, j in G.nodes()}  # Map node positions to grid layout
nx.draw(G, pos, node_size=10, node_color="blue", edge_color="gray", with_labels=False)
plt.title("Graph Representation")
plt.axis('equal')
plt.show()

# Randomly select valid start and goal nodes
nodes = list(G.nodes)
start = (149, 95) # (95, -149)
goal = (33, 75) # (81, 13) (75, -33)

print(f"Start Node: {start}, Goal Node: {goal}")

# Initialize the PathPlanner
planner = PathPlanner(G, start=start, goal=goal)

# Run the search
path = planner.run_search()
if path:
    print("Path:", path)

    # Visualize the graph with the path
    plt.figure(figsize=(10, 5))
    nx.draw(G, pos, node_size=10, node_color="blue", edge_color="gray", with_labels=False)
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=20, node_color="green")
    plt.title("Path Highlighted on Graph")
    plt.axis('equal')
    plt.show()
else:
    print("No path found!")
