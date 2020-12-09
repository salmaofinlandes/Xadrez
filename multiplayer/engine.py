"""
Engine.py:
- guarda toda a informação sobre o estado atual do tabuleiro
- implementa a lógica de movimentação das peças (assim como xeque, xeque-mate, roque, en passant)
- guarda um registo dos movimentos feitos por cada jogador

"""

class Engine:
	def __init__(self):
	
		self.board=[
			["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
			["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
			["__", "__", "__", "__", "__", "__", "__", "__"], 
			["__", "__", "__", "__", "__", "__", "__", "__"],  # Tabuleiro é uma matrix bidemensional
			["__", "__", "__", "__", "__", "__", "__", "__"],  # 1ª letra representa a cor (b,w) 
			["__", "__", "__", "__", "__", "__", "__", "__"],  # 2ª letra representa o tipo (tower(T), knight(N), bishop(B), queen(Q), king(K), pawn(P) 
			["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
			["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
		
		self.moveFunction = {'P': self.getPawnMoves,'R': self.getRookMoves,'N': self.getKnightMoves,
							 'B': self.getBishopMoves,'Q': self.getQueenMoves,'K': self.getKingMoves}
		
		self.whiteMove = True
		self.log = []
		self.whiteKing = (7,4)
		self.blackKing = (0,4)
		self.checkMate = False
		self.staleMate = False
		
	def makeMove(self, move): # toma um movimento como parametro e executa-o (nao funciona com roque, en passant nem promocao de peoes)
		self.board[move.startRow][move.startCol] = "__"
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.log.append(move)
		self.whiteMove = not self.whiteMove # troca a vez de jogar
		if move.pieceMoved == "wK":
			self.whiteKing = (move.endRow, move.endCol)
		elif move.pieceMoved == "bK":
			self.blackKing = (move.endRow, move.endCol)
		
		#pawn promotion
		if move.isPawnPromotion:
			self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q' # promocao a uma rainha
		
		
		
		
	def undoMove(self):
		if len(self.log) != 0: #ter a certeza que existe um mov para voltar atras
			move = self.log.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteMove = not self.whiteMove
			if move.pieceMoved == "wK":
				self.whiteKing = (move.startRow, move.startCol)
			elif move.pieceMoved == "bK":
				self.blackKing = (move.startRow, move.startCol)
			
	
	
	# Todos os movimentos considerando os xeques
	def getValidMoves(self):
		# 1 - gerar todos os movimentos válidos
		moves = self.getAllPossibleMoves()
		# 2 - para cada movimento, faze-lo
		for i in range(len(moves)-1, -1, -1): # mover os elementos a partir do fim
			self.makeMove(moves[i])
			self.whiteMove = not self.whiteMove
			# 3 - gerar todos os movimentos do openente
			# 4 - para cada movimento do oponente, ver se eles atacam o rei
			if self.inCheck():
				moves.remove(moves[i]) # 5 - se atacarem o rei, nao sao validos
			self.whiteMove = not self.whiteMove	
			self.undoMove()
		
		if len(moves) == 0: #xeque-mate ou afogado
			if self.inCheck:
				self.checkMate = True
				if self.whiteMove:
					print("pretas ganharam por xeque mate")
				else:
					print("brancas ganharam por xeque mate")
			else:
				self.staleMate = True
		else:
			self.checkMate = False
			self.staleMate = False		
			
		return moves
		
	def inCheck(self):
		if self.whiteMove:
			return self.squareUnderAttack(self.whiteKing[0],self.whiteKing[1])
		else:
			return self.squareUnderAttack(self.blackKing[0],self.blackKing[1])
	
	def squareUnderAttack(self,r,c):
		self.whiteMove = not self.whiteMove # mudar a vez de jogar
		oppMoves = self.getAllPossibleMoves()
		self.whiteMove = not self.whiteMove
		for move in oppMoves:
			if move.endRow == r and move.endCol == c:
				return True
		return False
		
		
	
	# Todos os movimentos sem considerar xeques
	def getAllPossibleMoves(self):
		moves = []
		for r in range(len(self.board)): #nº de linhas 
			for c in range(len(self.board[r])): # nº de colunas
				turn = self.board[r][c][0] # primeiro caracter de cada elemento
				if (turn == "w" and self.whiteMove) or (turn == "b" and not self.whiteMove):
					piece = self.board[r][c][1]
					self.moveFunction[piece](r,c,moves) # chama a funcao de movimento correspondente à peca
					
		return moves				
	
	
	# Movimentos de pecas individuais
	
	# Movimentos possiveis de um peao e adiciona os à lista de mov possiveis
	def getPawnMoves(self,r, c, moves):
		if self.whiteMove: #brancas a jogar
			if self.board[r-1][c] == "__": #verfica o quadrado a frente
				moves.append(Move((r,c), (r-1,c), self.board))
				if r == 6 and self.board[r-2][c] == "__": # verifica 2 quadrados à frente e se o peao nao saiu da linha de partida	
					moves.append(Move((r,c), (r-2, c), self.board))
			if c-1 >= 0:
				if self.board[r-1][c-1][0] == "b": # peca inimiga a esquerda para capturar		
					moves.append(Move((r,c), (r-1, c-1), self.board))
			if c+1 <= 7:
				if self.board[r-1][c+1][0] == "b": # peca inimiga a direita para capturar		
					moves.append(Move((r,c), (r-1, c+1), self.board))	
		else: # pretas a jogar
			if self.board[r+1][c] == "__":
				moves.append(Move((r,c), (r+1, c), self.board))
				if r == 1 and self.board[r+2][c] == "__":
					moves.append(Move((r,c), (r+2, c), self.board))
			if c-1 >= 0:
				if self.board[r+1][c-1][0] == "w": 	
					moves.append(Move((r,c), (r+1, c-1), self.board))
			if c+1 <= 7:
				if self.board[r+1][c+1][0] == "w": 		
					moves.append(Move((r,c), (r+1, c+1), self.board))	
		
	# Movimentos possiveis de uma torre e adiciona os à lista de mov possiveis
	def getRookMoves(self,r, c, moves):
		if self.whiteMove:
		
			enemy = 'b'
		else:
			enemy = 'w'	
		for i in range(1,7):
			if r-i >= 0:
				if self.board[r-i][c] == "__":
					moves.append(Move((r,c),(r-i,c), self.board))
				elif self.board[r-i][c][0] == enemy:
					moves.append(Move((r,c),(r-i,c), self.board))
					break	
				else:
					break
		for i in range(1,7):
			if r+i <= 7:
				if self.board[r+i][c] == "__":
					moves.append(Move((r,c),(r+i,c), self.board))
				elif self.board[r+i][c][0] == enemy:
					moves.append(Move((r,c),(r+i,c), self.board))
					break	
				else:
					break
		for i in range(1,7):
			if c-i >= 0:
				if self.board[r][c-i] == "__":
					moves.append(Move((r,c),(r,c-i), self.board))
				elif self.board[r][c-i][0] == enemy:
					moves.append(Move((r,c),(r,c-i), self.board))
					break	
				else:
					break
		for i in range(1,7):
			if c+i <= 7:
				if self.board[r][c+i] == "__":
					moves.append(Move((r,c),(r,c+i), self.board))
				elif self.board[r][c+i][0] == enemy:
					moves.append(Move((r,c),(r,c+i), self.board))
					break	
				else:
					break
				
			
	
	# Movimentos possiveis de um cavalo e adiciona os à lista de mov possiveis
	def getKnightMoves(self,r, c, moves):
		if self.whiteMove:
			enemy = 'b'
		else:
			enemy = 'w'	
		if r-2 >= 0:
			if c-1 >= 0:
				if self.board[r-2][c-1] == "__" or self.board[r-2][c-1][0] == enemy:
					moves.append(Move((r,c),(r-2,c-1),self.board))
			if c+1 <= 7:
				if self.board[r-2][c+1] == "__" or self.board[r-2][c+1][0] == enemy:
					moves.append(Move((r,c),(r-2,c+1),self.board))							
		if r+2 <= 7:
			if c-1 >= 0:
				if self.board[r+2][c-1] == "__" or self.board[r+2][c-1][0] == enemy:
					moves.append(Move((r,c),(r+2,c-1),self.board))
			if c+1 <= 7:
				if self.board[r+2][c+1] == "__" or self.board[r+2][c+1][0] == enemy:
					moves.append(Move((r,c),(r+2,c+1),self.board))						
		if c-2 >= 0:
			if r-1 >= 0:
				if self.board[r-1][c-2] == "__" or self.board[r-1][c-2][0] == enemy:
					moves.append(Move((r,c),(r-1,c-2), self.board))
			if r+1 <= 7:
				if self.board[r+1][c-2] == "__" or self.board[r+1][c-2][0] == enemy:
					moves.append(Move((r,c),(r+1,c-2), self.board))
		if c+2 <= 7:
			if r-1 >= 0:
				if self.board[r-1][c+2] == "__" or self.board[r-1][c+2][0] == enemy:
					moves.append(Move((r,c),(r-1,c+2), self.board))
			if r+1 <= 7:
				if self.board[r+1][c+2] == "__" or self.board[r+1][c+2][0] == enemy:
					moves.append(Move((r,c),(r+1,c+2), self.board))
								
		
	# Movimentos possiveis de uma bispo e adiciona os à lista de mov possiveis
	def getBishopMoves(self,r, c, moves):
		if self.whiteMove:
			enemy = 'b'
		else:
			enemy = 'w'
			
		for i in range(1,7):
			if r-i >= 0 and c-i >= 0:
				if self.board[r-i][c-i] == "__":
					moves.append(Move((r,c),(r-i,c-i), self.board))
				elif self.board[r-i][c-i][0] == enemy:
					moves.append(Move((r,c),(r-i,c-i), self.board))
					break
				else:
					break
		
		for i in range(1,7):
			if r-i >= 0 and c+i <= 7:
				if self.board[r-i][c+i] == "__":
					moves.append(Move((r,c),(r-i,c+i), self.board))
				elif self.board[r-i][c+i][0] == enemy:
					moves.append(Move((r,c),(r-i,c+i), self.board))
					break
				else:
					break
					
		for i in range(1,7):
			if r+i <= 7 and c-i >= 0:
				if self.board[r+i][c-i] == "__":
					moves.append(Move((r,c),(r+i,c-i), self.board))
				elif self.board[r+i][c-i][0] == enemy:
					moves.append(Move((r,c),(r+i,c-i), self.board))
					break
				else:
					break
					
		for i in range(1,7):
			if r+i <= 7 and c+i <= 7:
				if self.board[r+i][c+i] == "__":
					moves.append(Move((r,c),(r+i,c+i), self.board))
				elif self.board[r+i][c+i][0] == enemy:
					moves.append(Move((r,c),(r+i,c+i), self.board))
					break
				else:
					break
		
							 
	# Movimentos possiveis da rainha e adiciona os à lista de mov possiveis
	def getQueenMoves(self,r, c, moves):
		self.getRookMoves(r,c,moves)
		self.getBishopMoves(r,c,moves)
		
	# Movimentos possiveis do rei e adiciona os à lista de mov possiveis
	def getKingMoves(self,r, c, moves):
		i = 1
		if self.whiteMove:
			enemy = 'b'
		else:
			enemy = 'w'
		if r-i >= 0 and c-i >= 0:
			if self.board[r-i][c-i] == "__":
				moves.append(Move((r,c),(r-i,c-i), self.board))
			elif self.board[r-i][c-i][0] == enemy:
				moves.append(Move((r,c),(r-i,c-i), self.board))
		
		if r-i >= 0 and c+i <= 7:
			if self.board[r-i][c+i] == "__":
				moves.append(Move((r,c),(r-i,c+i), self.board))
			elif self.board[r-i][c+i][0] == enemy:
				moves.append(Move((r,c),(r-i,c+i), self.board))
					
		
		if r+i <= 7 and c-i >= 0:
			if self.board[r+i][c-i] == "__":
				moves.append(Move((r,c),(r+i,c-i), self.board))
			elif self.board[r+i][c-i][0] == enemy:
				moves.append(Move((r,c),(r+i,c-i), self.board))
				
		
		if r+i <= 7 and c+i <= 7:
			if self.board[r+i][c+i] == "__":
				moves.append(Move((r,c),(r+i,c+i), self.board))
			elif self.board[r+i][c+i][0] == enemy:
				moves.append(Move((r,c),(r+i,c+i), self.board))
				

		if r-i >= 0:
			if self.board[r-i][c] == "__":
				moves.append(Move((r,c),(r-i,c), self.board))
			elif self.board[r-i][c][0] == enemy:
				moves.append(Move((r,c),(r-i,c), self.board))
				
		if r+i <= 7:
			if self.board[r+i][c] == "__":
				moves.append(Move((r,c),(r+i,c), self.board))
			elif self.board[r+i][c][0] == enemy:
				moves.append(Move((r,c),(r+i,c), self.board))
				
		if c-i >= 0:
			if self.board[r][c-i] == "__":
				moves.append(Move((r,c),(r,c-i), self.board))
			elif self.board[r][c-i][0] == enemy:
				moves.append(Move((r,c),(r,c-i), self.board))
				
		if c+i <= 7:
			if self.board[r][c+i] == "__":
				moves.append(Move((r,c),(r,c+i), self.board))
			elif self.board[r][c+i][0] == enemy:
				moves.append(Move((r,c),(r,c+i), self.board))
				
	
	
	
		 
class Move:
	
	ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1,"8": 0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4, "f":5, "g":6, "h":7}
	colsToFiles = {v: k for k, v in filesToCols.items()}
	
	def __init__(self, startSq, endSq, board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1] 
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
		self.isPawnPromotion = False
		if (self.pieceMoved == "wP" and self.endRow ==0) or (self.pieceMoved == "bP" and self.endRow ==7):
			self.isPawnPromotion = True
			
		
	def __eq__(self, other):
		if isinstance(other, Move):
			return self.moveID == other.moveID
		return False	
	
		
	def Notation(self):
		return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
		
	def getRankFile(self,r ,c):
		return self.colsToFiles[c] + self.rowsToRanks[r]
		
		
		
		
		
		
		
		
		
		
		
		
		
