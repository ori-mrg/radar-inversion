import matplotlib.pyplot as plt
import networkx as nx

def plot_radar_image(image):
    """Plots the radar image."""
    plt.imshow(image, cmap='gray')
    plt.title("Radar Image")
    plt.show()

def plot_binned_image_and_graph(binned_image, graph):
    """Plots the binned image and its corresponding graph."""
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(binned_image, cmap='gray')
    plt.title("Binned Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    pos = {(i, j): (j, -i) for i, j in graph.nodes()}  # Grid layout
    nx.draw(graph, pos, node_size=10, node_color="blue", edge_color="gray", with_labels=False)
    plt.title("Graph Representation")
    plt.axis('equal')
    plt.show()

def plot_path_on_graph(graph, path):
    """Highlights the path on the graph."""
    pos = {(i, j): (j, -i) for i, j in graph.nodes()}  # Grid layout
    plt.figure(figsize=(10, 5))
    nx.draw(graph, pos, node_size=10, node_color="blue", edge_color="gray", with_labels=False)

    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="red", width=2)
        nx.draw_networkx_nodes(graph, pos, nodelist=path, node_size=20, node_color="green")

    plt.title("Path Highlighted on Graph")
    plt.axis('equal')
    plt.show()
