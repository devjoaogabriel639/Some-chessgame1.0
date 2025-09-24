import pygame as pyg
from config import  janela, tamanho_janela, TILE_SIZE
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

    def checar_movimento(self, movimentos_permitidos):
        if self.posicao in movimentos_permitidos:
            self.desenhar()
        else:
            print(f"Movimento ilegal para peça em {self.posicao}")





