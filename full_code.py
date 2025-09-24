import pygame as pyg
import numpy as np
from config import array_vermelho
import pymsgbox

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

# Função para criar uma casa
def create_tile(color):
    return np.full((TILE_SIZE, TILE_SIZE, 3), color, dtype=np.uint8)

# Função para criar o tabuleiro
def create_checkerboard(width, height):
    board_rows = []
    casas_pretas = []
    for y in range(height):
        row_tiles = []
        for x in range(width):
            if (x + y) % 2 == 0:
                color = BLACK
                casas_pretas.append((x, y))
            else:
                color = WHITE
            tile = create_tile(color)
            row_tiles.append(tile)
        board_rows.append(np.hstack(row_tiles))
    board = np.vstack(board_rows)
    return board, casas_pretas

# Função para desenhar o tabuleiro
def desenha_mapa(mapa):
    superficie = pyg.surfarray.make_surface(mapa)
    janela.blit(superficie, (0, 0))

class Peça:
    def __init__(self, cor, tipo, sprite, posicao):
        self.cor = cor
        self.tipo = tipo
        self.sprite = sprite
        self.posicao = posicao  # coordenadas na grade (coluna, linha)
        self.selecionada = False

        # Corpo físico (rect) baseado na posição em pixels
        self.corpo = pyg.Rect(
            posicao[0] * TILE_SIZE,
            posicao[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

    def desenhar(self):
        janela.blit(self.sprite, self.corpo.topleft)

    def atualizar_eventos(self, eventos):
        for event in eventos:
            if event.type == pyg.MOUSEBUTTONDOWN:
                if self._clicado(pyg.mouse.get_pos()):
                    self.selecionada = True

            elif event.type == pyg.MOUSEBUTTONUP:
                self.selecionada = False

            elif event.type == pyg.MOUSEMOTION and self.selecionada:
                mouse_x, mouse_y = pyg.mouse.get_pos()
                grid_x = mouse_x // TILE_SIZE
                grid_y = mouse_y // TILE_SIZE
                self.posicao = (grid_x, grid_y)
                self.corpo.topleft = (grid_x * TILE_SIZE, grid_y * TILE_SIZE)

    def _clicado(self, mouse_pos):
        return self.corpo.collidepoint(mouse_pos)

    def checar_movimento(self, movimentos_permitidos):
        if self.posicao in movimentos_permitidos:
            self.desenhar()
        else:
            # Achando a casa preta mais próxima...
            px, py = self.posicao
            casa_mais_proxima = min(
                movimentos_permitidos,
                key=lambda c: (c[0] - px) ** 2 + (c[1] - py) ** 2
            )

            self.posicao = casa_mais_proxima
            self.corpo.topleft = (self.posicao[0] * TILE_SIZE, self.posicao[1] * TILE_SIZE)
            self.desenhar()

            print(f"Movimento ilegal. Peça movida para {self.posicao}")


# Preparação do tabuleiro e das peças
tabuleiro, casas_pretas = create_checkerboard(MAP_WIDTH, MAP_HEIGHT)

# Carregar sprite da peça
imagem = pyg.image.load(image_path)
imagem = pyg.transform.scale(imagem, (25, 25))

# Fatiamento das posições iniciais
n = 3
posicoes_superior = casas_pretas[:n]
posicoes_inferior = casas_pretas[-n:]

# Criando as peças
pecas = []
for pos in posicoes_superior:
    pecas.append(Peça("preto", "peao", imagem, pos))

for pos in posicoes_inferior:
    pecas.append(Peça("branco", "peao", imagem, pos))

# Exemplo de movimentos permitidos
movimentos_permitidos = casas_pretas

#Loop principal

running = True
while running:
    eventos = pyg.event.get()

    for event in eventos:
        if event.type == pyg.QUIT:
            running = False

    desenha_mapa(tabuleiro) # só uma vez

    for Peça in pecas:
        Peça.atualizar_eventos(eventos)
        Peça.checar_movimento(movimentos_permitidos)
        Peça.desenhar()

    pyg.display.flip() # só uma vez
