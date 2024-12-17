import yaml
import numpy as np
import matplotlib.pyplot as plt

# Load the YAML-like radar data file
file_path = '../data/fft_data.csv'  # Update with your file path
data_blocks = []  # To store parsed data from multiple YAML documents

# Parse the YAML content
with open(file_path, 'r') as f:
    docs = yaml.safe_load_all(f)
    for doc in docs:
        if doc:
            data_blocks.append(doc)

print(f"Total data blocks parsed: {len(data_blocks)}")

# Initialize storage arrays
angles = []
azimuths = []
data_arrays = []

# Extract and clean the data
for block in data_blocks:
    angle = block.get('angle', None)
    azimuth = block.get('azimuth', None)
    data = block.get('data', [])

    if angle is not None and azimuth is not None and len(data) > 0:
        try:
            clean_data = [
                float(item) for item in data
                if isinstance(item, (int, float)) or 
                   (isinstance(item, str) and item.replace('.', '', 1).isdigit())
            ]
            if len(clean_data) == 0:
                continue

            angles.append(angle)
            azimuths.append(azimuth)  # Raw azimuth values, no mod yet
            data_arrays.append(np.array(clean_data, dtype=float))
        except ValueError:
            continue

# Convert to numpy arrays
azimuths = np.array(azimuths, dtype=int)
data_arrays = np.array(data_arrays, dtype=object)

# Define the set of required odd azimuths (mod 400)
required_odd_azimuths = set(range(1, 400, 2))  # [1, 3, 5, ..., 399]

# Find the first full sweep by checking azimuths
valid_indices = []
valid_azimuths = []
odd_azimuths_seen = set()

for i, az in enumerate(azimuths % 400):
    if az in required_odd_azimuths:
        if az not in odd_azimuths_seen:
            valid_indices.append(i)
            valid_azimuths.append(azimuths[i])
            odd_azimuths_seen.add(az)
    
    if odd_azimuths_seen == required_odd_azimuths:
        break

# Validate the results
if len(odd_azimuths_seen) < len(required_odd_azimuths):
    print("Warning: Not all required odd azimuths were found.")
else:
    print("All required odd azimuths found.")

print(f"Length of valid indices: {len(valid_indices)}")
print(f"Length of valid azimuths: {len(valid_azimuths)}")

# Extract valid data arrays for the first sweep
valid_data = [data_arrays[i] for i in valid_indices]
valid_azimuths = [azimuths[i] for i in valid_indices]

# No padding needed since each message should contain exactly 128 bins
normalized_data = []

for idx, d in enumerate(valid_data):
    try:
        clean_array = np.array(d, dtype=float)
        normalized = clean_array / 255.0  # Normalize (ensure no division errors)
        normalized_data.append(normalized)
    except Exception as e:
        print(f"Warning: Issue with data at index {idx} - {e}")
        continue

# Convert to a 2D numpy array
if len(normalized_data) > 0:
    normalized_data = np.vstack(normalized_data)  # Stack into 2D array
else:
    raise ValueError("No valid data to plot.")

# Map azimuth mod 400 to y-axis
azimuth_mod_400 = [az % 400 for az in valid_azimuths]

# Visualization of the first full sweep
plt.figure(figsize=(12, 6))
plt.imshow(
    normalized_data, 
    aspect='auto', 
    cmap='gray', 
    extent=[0, 128, 0, 400]  # X: bin index (0-128), Y: azimuth mod 400 (0-400)
)
plt.colorbar(label='Normalized Amplitude (0-1)')
plt.xlabel('Bin Index')
plt.ylabel('Azimuth Index (Mod 400)')
plt.title('Radar Data - First Full Sweep (Azimuth Modulo 400)')
plt.tight_layout()
plt.savefig('raw_radar_data')
plt.show()

# Convert polar coordinates (radius, azimuth) to Cartesian coordinates
radius = np.arange(128) * 0.175  # 128 bins, each 0.175 meters apart
theta = np.deg2rad(np.array(azimuth_mod_400))  # Convert azimuths to radians

# Create a Cartesian grid
cart_resolution = 0.2  # meters per pixel
cart_pixel_width = 500  # pixels
cartesian_image = np.zeros((cart_pixel_width, cart_pixel_width))

cart_min_range = (cart_pixel_width // 2) * cart_resolution
coords = np.linspace(-cart_min_range, cart_min_range, cart_pixel_width)
Y, X = np.meshgrid(coords, -coords)
sample_range = np.sqrt(Y**2 + X**2)
sample_angle = np.arctan2(Y, X)
sample_angle[sample_angle < 0] += 2 * np.pi

# Map polar data to Cartesian coordinates
azimuth_step = theta[1] - theta[0]
sample_u = np.clip((sample_range - radius[0]) / (radius[1] - radius[0]), 0, len(radius) - 1)
sample_v = (sample_angle - theta[0]) / azimuth_step

for i in range(cartesian_image.shape[0]):
    for j in range(cartesian_image.shape[1]):
        cartesian_image[i, j] = normalized_data[
            int(sample_v[i, j] % len(theta)), 
            int(sample_u[i, j])
        ]

# Cartesian visualization
plt.figure(figsize=(20, 20))
plt.imshow(cartesian_image, cmap='gray', origin='lower', extent=[-cart_min_range, cart_min_range] * 2)
plt.colorbar(label='Normalized Amplitude (0-1)')
plt.title('Radar Data - First Full Sweep (Cartesian Projection)')
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.tight_layout()
plt.savefig('raw_radar_cartesian_data', dpi=1000)
plt.show()
