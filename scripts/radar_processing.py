import numpy as np
import networkx as nx
from src.radar import load_radar, radar_polar_to_cartesian

def load_and_process_radar(file_path, cart_resolution=0.2, cart_pixel_width=500):
    """Loads and processes radar data into a Cartesian image."""
    _, azimuths, _, fft_data, radar_resolution = load_radar(file_path)
    image = radar_polar_to_cartesian(azimuths, fft_data, radar_resolution, cart_resolution, cart_pixel_width)
    return np.squeeze(image)

def create_binned_image(image, bin_size=3, threshold=0.08):
    """Creates a binned image where bins are classified as 1 (blocked) or 0 (free)."""
    height, width = image.shape
    binned_height = height // bin_size
    binned_width = width // bin_size
    binned_image = np.zeros((binned_height, binned_width), dtype=int)

    # 0 for no obstacles and 1 for obstacles
    for i in range(binned_height):
        for j in range(binned_width):
            bin_pixels = image[i * bin_size:(i + 1) * bin_size, j * bin_size:(j + 1) * bin_size]
            binned_image[i, j] = 1 if np.any(bin_pixels > threshold) else 0

    return binned_image

def create_graph_from_binned_image(binned_image):
    """Creates a graph from the binned image."""
    binned_height, binned_width = binned_image.shape

    def is_valid_node(x, y):
        return 0 <= x < binned_height and 0 <= y < binned_width and binned_image[x, y] == 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    G = nx.Graph()

    for i in range(binned_height):
        for j in range(binned_width):
            if binned_image[i, j] == 0:
                G.add_node((i, j))
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if is_valid_node(ni, nj):
                        G.add_edge((i, j), (ni, nj))
    return G

