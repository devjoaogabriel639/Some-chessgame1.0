import pygame as pyg
import numpy as np

# Inicialização
pyg.init()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TILE_SIZE = 50
MAP_WIDTH = 5
MAP_HEIGHT = 5
canto_superior = (0, 0)

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


# Classe Peça
class Peça:
    def __init__(self, cor, tipo, sprite, posicao):
        self.cor = cor
        self.tipo = tipo
        self.sprite = sprite
        self.posicao = posicao
        self.selecionada = False

    def desenhar(self):
        x, y = self.posicao
        janela.blit(self.sprite, (x * TILE_SIZE, y * TILE_SIZE))

    def atualizar_eventos(self, eventos):
        for event in eventos:
            if event.type == pyg.MOUSEBUTTONDOWN:
                mouse_pos = pyg.mouse.get_pos()
                if self._clicado(mouse_pos):
                    self.selecionada = True

            elif event.type == pyg.MOUSEBUTTONUP:
                self.selecionada = False

            elif event.type == pyg.MOUSEMOTION and self.selecionada:
                mouse_x, mouse_y = pyg.mouse.get_pos()
                self.posicao = (mouse_x // TILE_SIZE, mouse_y // TILE_SIZE)

    def _clicado(self, mouse_pos):
        tile_x = mouse_pos[0] // TILE_SIZE
        tile_y = mouse_pos[1] // TILE_SIZE
        return (tile_x, tile_y) == self.posicao


# Preparação do tabuleiro e das peças
tabuleiro, casas_pretas = create_checkerboard(MAP_WIDTH, MAP_HEIGHT)

# Carregar sprite da peça
imagem = pyg.image.load(image_path)

superficie = pyg.transform.scale(imagem, (25, 25))

# Fatiamento para posições
n = 3
posicoes_superior = casas_pretas[:n]
posicoes_inferior = casas_pretas[-n:]

# Criando peças
pecas = []
for pos in posicoes_superior:
    pecas.append(Peça("preto", "peao", imagem, pos))

for pos in posicoes_inferior:
    pecas.append(Peça("branco", "peao", imagem, pos))

# Loop principal
running = True
while running:

    eventos = pyg.event.get()
    for event in eventos:
        if event.type == pyg.QUIT:
            running = False


    # Atualiza lógica de todas as peças
    for peca in pecas:
        peca.atualizar_eventos(eventos)
        pyg.display.flip()

# Desenhar o tabuleiro e as peças
desenha_mapa(tabuleiro)
for peca in pecas:
    desenha_mapa(tabuleiro)
    peca.desenhar()

    janela.blit(superficie, canto_superior, )

    pyg.display.flip()

pyg.quit()
