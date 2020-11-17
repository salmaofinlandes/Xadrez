"""
Main.py	
																											
- lida com o input		
- mostra o objeto 'Engine' através de uma interface grafica utilizando a biblioteca pygame 																				
"""
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
# resolve o erro: 'ALSA lib pcm.c:8526:(snd_pcm_recover) underrun occurred'

import pygame as pg 
from engine import Engine, Move # importar a classe Engine

#declaracao de constantes
IMG={}
WIDTH = 512 # potencia de 2, logo vai ser divisivel por 8 com resto 0 
HEIGHT = 512
DIM = 8 # 8X8
SQUARE = 512//8 # tamanho de cada quadrado individual

def load_img():
	pieces=["wP", "bP", "wN", "bN", "wB", "bB", "wR", "bR", "wQ", "bQ", "wK", "bK"]
	for piece in pieces:
		IMG[piece] = pg.transform.scale(pg.image.load("images/"+piece+".png"), (SQUARE, SQUARE)) # carrega as img no tamanho desejado



def main():
	pg.init()
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Xadrez")
	clock = pg.time.Clock()
	screen.fill(pg.Color("white"))
	gs = Engine()
	load_img()
	running = True
	sqSelected = () # mantem registo do ultimo clique do utilizador. Vazia inicialmente
	playerClicks = [] # mantem o registo dos 2 ultimos cliques do utilizador. len(playerClicks) <= 2
	# Main game loop
	while running:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
			elif e.type == pg.MOUSEBUTTONDOWN:
				location = pg.mouse.get_pos() # coordenadas (x,y) do rato
				col = location[0]//SQUARE 
				row = location[1]//SQUARE
				if sqSelected == (row, col): # verfica se o utilizador clicou duas vezes no mesmo quadrado.
					sqSelected = () # de seleciona
					playerClicks = [] # limpa o registo dos ultimos 2 cliques
				else:	
					sqSelected = (row, col)
					playerClicks.append(sqSelected)
				if len(playerClicks) == 2: # verifica se a lista já está cheia
					move = Move(playerClicks[0], playerClicks[1], gs.board)
					print(move.Notation())
					gs.makeMove(move)
					sqSelect = () # reset ao click do utilizador
					playerClicks = []
					
		draw_game_state(screen, gs)
		clock.tick(15) # programa corre a um max de 15 fps
		pg.display.flip() # atualiza o conteudo do display inteiro
		
		
		
def draw_game_state(screen, gs):
	draw_board(screen) 
	draw_pieces(screen, gs.board)


#desenhar o tabuleiro

def draw_board(screen):
	colors = [pg.Color("white"), pg.Color("grey")]
	for r in range(DIM):
		for c in range(DIM):
			color = colors[((r+c)%2)]
			pg.draw.rect(screen, color, pg.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))


# desenhar as pecas
			
def draw_pieces(screen, board):
	for r in range(DIM):
		for c in range(DIM):
			piece = board[r][c]		
			if piece != "__": # verifica se existe uma peça nesse lugar ou se está vazio ("__")
				screen.blit(IMG[piece], pg.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))
				
if __name__ == "__main__":
	main()		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
			 
