import pygame as pyg
import numpy  as np
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

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

# Clock para o pygame e para o UI Manager
clock = pyg.time.Clock()
manager = pygame_gui.UIManager(tamanho_janela)

# Configuração de cartas (pygame_gui)
imagens_cartas = {
    "carta_1": pyg.image.load("carta_1.png"),
    "carta_2": pyg.image.load("carta_2.png")
}

# Criando os botões de carta já com a imagem inicial
botoes_cartas = []
pos_x, pos_y = 50, 50
for idx, carta in enumerate(imagens_cartas):
    botao = pygame_gui.elements.UIButton(
        relative_rect=pyg.Rect(pos_x + idx*110, pos_y, 100, 150),
        text='',
        manager=manager,
        object_id=f"#carta_{idx+1}"
    )
    botoes_cartas.append(botao)


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
        self.corpo = pyg.Rect(
            posicao[0] * TILE_SIZE,
            posicao[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

    def desenhar(self):
        janela.blit(self.sprite, self.corpo.topleft)

    def _clicado(self, mouse_pos):
        return self.corpo.collidepoint(mouse_pos)

    def checar_movimento(self, movimentos_permitidos):
        if self.posicao in movimentos_permitidos:
            self.desenhar()
        else:
            px, py = self.posicao
            casa_mais_proxima = min(
                movimentos_permitidos,
                key=lambda c: (c[0] - px) ** 2 + (c[1] - py) ** 2
            )
            self.posicao = casa_mais_proxima
            self.corpo.topleft = (self.posicao[0] * TILE_SIZE, self.posicao[1] * TILE_SIZE)
            self.desenhar()

    def calcular_movimentos_possiveis(self, tabuleiro):
        movimentos = []
        x, y = self.posicao
        adjacentes = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
        for casa in adjacentes:
            if casa in tabuleiro:
                movimentos.append(casa)
        return movimentos

    def representar_selec(self, movimentos_permitidos, janela, tile_size):
        if self.selecionada:
            cinza = pyg.Surface((tile_size, tile_size))
            cinza.fill((128, 128, 128))
            px, py = self.posicao[0] * tile_size, self.posicao[1] * tile_size
            janela.blit(cinza, (px, py))
            for casa in movimentos_permitidos:
                self.diagonalproxima(casa, janela)

    def diagonalproxima(self, casa, janela, tile_size=TILE_SIZE):
        vermelho = pyg.Surface((tile_size, tile_size))
        vermelho.fill((128, 0, 0))
        px = casa[0] * tile_size
        py = casa[1] * tile_size
        janela.blit(vermelho, (px, py))


# Preparação do tabuleiro e das peças
tabuleiro, casas_pretas = create_checkerboard(MAP_WIDTH, MAP_HEIGHT)
imagem = pyg.image.load(image_path)
imagem = pyg.transform.scale(imagem, (25, 25))

n = 3
posicoes_superior = casas_pretas[:n]
posicoes_inferior = casas_pretas[-n:]

pecas = []
for pos in posicoes_superior:
    pecas.append(Peça("preto", "peao", imagem, pos))
for pos in posicoes_inferior:
    pecas.append(Peça("branco", "peao", imagem, pos))

movimentos_permitidos = casas_pretas


# Loop principal
jogador_atual = "superior"
peca_selecionada = None
running = True

while running:
    time_delta = clock.tick(60) / 1000.0
    eventos = pyg.event.get()
    for event in eventos:
        # Processa eventos do UI Manager primeiro
        manager.process_events(event)

        # Trata saída do jogo
        if event.type == pyg.QUIT:
            running = False

        # Clique do mouse
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if peca_selecionada is None:
                for peca in pecas:
                    if peca._clicado(pyg.mouse.get_pos()):
                        if (jogador_atual == "superior" and peca.posicao in posicoes_superior) or \
                                (jogador_atual == "inferior" and peca.posicao in posicoes_inferior):
                            peca.selecionada = True
                            peca_selecionada = peca

        # Movimentação do mouse enquanto arrasta peça
        elif event.type == pyg.MOUSEMOTION and peca_selecionada:
            mouse_x, mouse_y = pyg.mouse.get_pos()
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE
            peca_selecionada.posicao = (grid_x, grid_y)
            peca_selecionada.corpo.topleft = (grid_x * TILE_SIZE, grid_y * TILE_SIZE)

        # Soltar o mouse para "largar" a peça
        elif event.type == pyg.MOUSEBUTTONUP and peca_selecionada:
            peca_selecionada.selecionada = False
            peca_selecionada.checar_movimento(movimentos_permitidos)
            jogador_atual = "inferior" if jogador_atual == "superior" else "superior"
            peca_selecionada = None

    desenha_mapa(tabuleiro)

    if peca_selecionada:
        movimentos_possiveis = peca_selecionada.calcular_movimentos_possiveis(casas_pretas)
        peca_selecionada.representar_selec(movimentos_possiveis, janela=janela, tile_size=50)

    for peca in pecas:
        peca.desenhar()

    manager.update(time_delta)
    manager.draw_ui(janela)

    pyg.display.flip()