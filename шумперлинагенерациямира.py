from numpy import floor
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from random import randint
import numpy as np

noise = PerlinNoise(octaves=1, seed=randint(-10000, 10000))
amp = 6
period = 24
terrain_width = 250

#landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]
landscale = np.zeros((terrain_width, terrain_width))

for position in range(terrain_width ** 2):
    x = floor(position / terrain_width)
    z = floor(position % terrain_width)
    y = floor(noise([x / period, z / period]) * amp)
    landscale[int(x)][int(z)] = int(y)
plt.imshow(landscale)
plt.show()
