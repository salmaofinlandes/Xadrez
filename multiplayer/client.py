"""
Main.py	
																											
- lida com o input		
- mostra o objeto 'Engine' através de uma interface grafica utilizando a biblioteca pygame 																				
"""
import socket
import pickle
import select
import sys
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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number") 
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port))

turn = server.recv(2048).decode()

if turn == "0":
	print("JOGADOR 1 - BRANCAS")
elif turn == "1":
	print("JOGADOR 2 - PRETAS")	

print(turn)

def debug(gs):
	if gs.whiteMove:
		print("WhiteToMove")
	else:
		print("BlackToMove")
			

def load_img():
	pieces=["wP", "bP", "wN", "bN", "wB", "bB", "wR", "bR", "wQ", "bQ", "wK", "bK"]
	for piece in pieces:
		IMG[piece] = pg.transform.scale(pg.image.load("images/"+piece+".png"), (SQUARE, SQUARE)) # carrega as img no tamanho desejado



def main():
	global turn
	pg.init()
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Xadrez")
	clock = pg.time.Clock()
	screen.fill(pg.Color("white"))
	gs = Engine()
	
	validMoves = gs.getValidMoves() # lista de mov validos usada para comparar mov do user aos válidos
	moveMade = False # variavel usada para nao ter que chamar o metodo getAllValidMoves() a cada frame 
					 # melhorando a performance significativamente
	
	
	load_img()
	running = True
	sqSelected = () # mantem registo do ultimo clique do utilizador. Vazia inicialmente
	playerClicks = [] # mantem o registo dos 2 ultimos cliques do utilizador. len(playerClicks) <= 2
	# Main game loop
	while running:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
			
			# manipula os cliques de rato
			elif e.type == pg.MOUSEBUTTONDOWN:
				location = pg.mouse.get_pos() # coordenadas (x,y) do rato
				col = location[0]//SQUARE 
				row = location[1]//SQUARE
				print(gs.board[row][col])
				if sqSelected == (row, col): # verfica se o utilizador clicou duas vezes no mesmo quadrado.
					sqSelected = () # de seleciona
					playerClicks = [] # limpa o registo dos ultimos 2 cliques
				else:		
					sqSelected = (row, col)
					playerClicks.append(sqSelected)
					
				if len(playerClicks) == 2: # verifica se a lista já está cheia
					move = Move(playerClicks[0], playerClicks[1], gs.board) #gera o objeto "move"
					for i in range(len(validMoves)):
						if move == validMoves[i]: # movimento é valido
							if gs.whiteMove and turn == "0":
								#print("white moved")
								print(move.Notation())
								gs.makeMove(move)
								data = str(move.startRow)+str(move.startCol)+str(move.endRow)+str(move.endCol)
								print("data sending to server:",data[0] + data[1] + data[2] + data[3])
								server.send(data.encode())
								moveMade = True 
								sqSelected = () # reset ao click do utilizador
								playerClicks = [] # reset à lista de cliques
							
							elif not(gs.whiteMove) and turn == "1":
								#print("black moved")
								print(move.Notation())
								gs.makeMove(move)
								data = str(move.startRow)+str(move.startCol)+str(move.endRow)+str(move.endCol)
								print("data sending to server:",data[0] + data[1] + data[2] + data[3])
								server.send(data.encode())
								moveMade = True 
								sqSelected = () # reset ao click do utilizador
								playerClicks = [] # reset à lista de cliques
										
						
						if not moveMade:
							playerClicks = [sqSelected]
			
			# desfazer movimento (desativado na versao multiplayer para nao causar bugs)		
			"""
			elif e.type == pg.KEYDOWN:
				if e.key == pg.K_z: # voltar atras quando a tecla "z" é clicada
					gs.undoMove()
					moveMade = True # atualiza a lista de movimentos validos
			"""
		
			
		draw_game_state(screen, gs)
		clock.tick(15) # programa corre a um max de 15 fps
		pg.display.flip() # atualiza o conteudo do display inteiro
		
		if gs.whiteMove and turn == "1":
			print("white to move")
			print("waiting for msg")
			msg = server.recv(2048).decode()
			print("data received from the server:", msg)
			gs.makeMove(Move((int(msg[0]), int(msg[1])), (int(msg[2]), int(msg[3])), gs.board))
			moveMade = True
			print("move made")
			debug(gs)		
		elif not(gs.whiteMove) and turn == "0":
			print("black to move")
			print("waiting for msg")
			msg = server.recv(2048).decode()
			print("data received from the server:", msg)
			gs.makeMove(Move((int(msg[0]), int(msg[1])), (int(msg[2]), int(msg[3])), gs.board))
			moveMade = True		
		
		
		if moveMade: # se o movimento tiver sido realizado chama a funcao getValidMoves()
			validMoves = gs.getValidMoves()
			moveMade = False
		
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
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
			 
