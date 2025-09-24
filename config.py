import pygame as pyg

import numpy as np

pyg.init()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (139, 0, 0)
TILE_SIZE = 50
MAP_WIDTH = 5
MAP_HEIGHT = 5

image_path = r"C:\Users\devjo\OneDrive\Imagens\133523046783312876.jpg"

# Janela
tamanho_janela = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE
janela = pyg.display.set_mode(tamanho_janela)

array_vermelho = np.full((2, 2, 3), RED, dtype=np.uint8)  # 2D

