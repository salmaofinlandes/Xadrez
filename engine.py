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
		
		self.WhiteMove = True
		self.log = []
		
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = "__"
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.log.append(move)
		self.WhiteMove = not self.WhiteMove # troca a vez de jogar 
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
		
		
	def Notation(self):
		return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
		
	def getRankFile(self,r ,c):
		return self.colsToFiles[c] + self.rowsToRanks[r]
		
		
		
		
		
		
		
		
		
		
		
		
		
