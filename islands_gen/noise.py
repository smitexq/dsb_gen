import math
from random import randint

from PIL import Image
import numpy as np
from opensimplex import OpenSimplex

"""
Генератор шума:
scale - растягивает шум, чем меньше, тем резче и детальнее шум
"""
def generate_heightmap(size: int, scale: int, seed:int):
    noise = OpenSimplex(seed)
    heightmap = np.zeros((size, size)) #карта высот
    h, l = 0, 0
    for x in range(size):
        for y in range(size):
            nx, ny = x / scale, y / scale
            heightmap[x, y] = noise.noise2(nx, ny)
            if heightmap[x, y] > 0.8:
                h += 1
            if heightmap[x, y] < -0.8:
                l += 1
    # print(f"h: {h}, l: {l}")
    return heightmap


"""
Получение высоты по карте шума
"""
def get_height(noise_heightmap, x, y, can_down=False, is_nether = False):
    h = noise_heightmap[int(2047 + x)//16, int(2047 + y)//16]
    if can_down:
        if -0.55 < h <= -0.3:
            # h -= 0.4
            h -= 0.25 + randint(5, 15)/100

    m, h = 1 if h >= 0 else -1, abs(h)

    raw_height = min(200, max(-50, int(58 + m * math.tan((math.pi *h)/2)*math.exp(h)*(15/(1 + math.exp(-h))))))
    if not is_nether:
        return raw_height
    else:
        # сжатие диапазона
        old_min, old_max = -50, 200
        new_min, new_max = 10, 140

        return int(new_min + (raw_height - old_min) * (new_max - new_min) / (old_max - old_min))

"""
Визуальная картинка шума
"""
def draw_heightmap(image: Image, heightmap, scale=16):
    hm = (heightmap + 1) * 48
    hm = hm.clip(0, 255).astype(np.uint8)
    hm = np.repeat(np.repeat(hm, scale, axis=0), scale, axis=1)

    image.paste(Image.fromarray(hm, "L").convert("RGB"))