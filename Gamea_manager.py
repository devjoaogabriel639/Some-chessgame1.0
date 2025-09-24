import time
import logging
from collections import deque, namedtuple
import random

import pygame as pyg
from codigo_descongelado import Peça,eventos, create_checkerboard, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT


class GameManager:
    def __init__(self):
        for peca in self.pecas:
            peca.atualizar_eventos(eventos)

        # Criar o tabuleiro e casas pretas

        self.tabuleiro, self.casas_pretas = create_checkerboard(MAP_WIDTH, MAP_HEIGHT)

        # Definir quantidade inicial de peças por lado
        n = 3

        # Posicionamento inicial dos jogadores
        self.posicoes_superior = self.casas_pretas[:n]
        self.posicoes_inferior = self.casas_pretas[-n:]

        # Carregar sprite da peça
        image_path = r"C:\Users\devjo\OneDrive\Imagens\133523046783312876.jpg"
        sprite = pyg.image.load(image_path)
        self.sprite = pyg.transform.scale(sprite, (25, 25))

        # Criar peças
        self.pecas = []
        for pos in self.posicoes_superior:
            self.pecas.append(Peça("preto", "peao", self.sprite, pos))
        for pos in self.posicoes_inferior:
            self.pecas.append(Peça("branco", "peao", self.sprite, pos))

        # Jogador inicial
        self.jogador_atual = "superior"


