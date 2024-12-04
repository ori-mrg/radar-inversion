import matplotlib.pyplot as plt
from src.radar import load_radar, radar_polar_to_cartesian
radar_image_location = "./data/1547131046353776.png"

_, azimuths, _, fft_data, radar_resolution = load_radar(radar_image_location)
image = radar_polar_to_cartesian(azimuths, fft_data, radar_resolution, cart_resolution=0.2, cart_pixel_width=500)
plt.imshow(image)
plt.show()