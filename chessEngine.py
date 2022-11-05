from typing import List
import pygame as pg

'''
this class is responsible for storing all the information about
the current state of a chess game. It will also be responsible 
for determining the valid moves at the current state. It will also kepp 
a move log.
''' 

class Move:
    # Maps keys to values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, start, end, board) -> None:
        self.startRow, self.startCol = start
        self.endRow, self.endCol = end
        self.pieceMoved = None
        if (0 <= self.startRow <= 7 and 0 <= self.startCol <= 7):
            self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = None
        if (0 <= self.endRow <= 7 and 0 <= self.endCol <= 7):
            self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 \
                    + self.endRow * 10 + self.endCol
    
    '''
    overriding the equals method
    '''
    def __eq__(self, __o: object) -> bool:
        if (not isinstance(__o, Move)):
            return False
        return self.moveId == __o.moveId
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + \
                self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

'''
this class represents a piece of chees game
'''
class Piece:
    def __init__(self, id: str, scaled: tuple) -> None:
        self.id = id
        image = pg.image.load(f'images/{self.id}.png')
        self.image = pg.transform.scale(image, scaled)

    def movesPawn(self, whiteToMove, r, c, board) -> List[Move]:
        moves = []
        if (whiteToMove and self.id == 'wp'):
            if (board[r-1][c] == '--'):
                moves.append(Move((r, c), (r-1, c), board))
            if (board[r-2][c] == '--' and r == 6):
                moves.append(Move((r, c), (r-2, c), board))
            if (c-1 >= 0):
                if (board[r-1][c-1] != '--'):
                    if (board[r-1][c-1].id[0] == 'b'):
                        moves.append(Move((r, c), (r-1, c-1), board))
            if (c+1 <= 7):
                if (board[r-1][c+1] != '--'):
                    if (board[r-1][c+1].id[0] == 'b'):
                        moves.append(Move((r, c), (r-1, c+1), board))
        elif ((not whiteToMove) and self.id == 'bp'):
            if (board[r+1][c] == '--'):
                moves.append(Move((r, c), (r+1, c), board))
            if (board[r+2][c] == '--' and r == 1):
                moves.append(Move((r, c), (r+2, c), board))
            if (c+1 >= 0):
                if (board[r+1][c-1] != '--'):
                    if (board[r+1][c-1].id[0] == 'w'):
                        moves.append(Move((r, c), (r+1, c-1), board))
            if (c+1 <= 7):
                if (board[r+1][c+1] != '--'):
                    if (board[r+1][c+1].id[0] == 'w'):
                        moves.append(Move((r, c), (r+1, c+1), board))
        return moves
    
    def movesRock(self, whiteToMove, r, c, board) -> List[Move]:
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemyColor = ["w", "b"][whiteToMove]
        moves = []
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if (0 <= endRow <= 7 and 0 <= endCol <= 7):
                    endPiece = board[endRow][endCol]
                    if (endPiece == '--'):
                        moves.append(Move((r, c), (endRow, endCol), board))
                    elif (endPiece.id[0] == enemyColor):
                        moves.append(Move((r, c), (endRow, endCol), board))
                        break
                    else:
                        break
                else:
                    break
        if (whiteToMove and self.id[0] == 'w'):
            return moves
        elif ((not whiteToMove) and self.id[0] == 'b'):
            return moves
        else:
            return []
        
    def movesKnight(self, whiteToMove, r, c, board) -> List[Move]:
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                      (1, -2), (1, 2), (2, -1), (2, 1)]
        allyColor = ["b", "w"][whiteToMove]
        moves = []
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if (0 <= endRow <= 7 and 0 <= endCol <= 7):
                endPiece = board[endRow][endCol]
                if (endPiece == '--'):
                     moves.append(Move((r, c), (endRow, endCol), board))
                elif (endPiece.id[0] != allyColor):
                    moves.append(Move((r, c), (endRow, endCol), board))
        if (whiteToMove and self.id[0] == 'w'):
            return moves
        elif ((not whiteToMove) and self.id[0] == 'b'):
            return moves
        else:
            return []
        
    def movesBishop(self, whiteToMove, r, c, board) -> List[Move]:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemyColor = ["w", "b"][whiteToMove]
        moves = []
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if (0 <= endRow <= 7 and 0 <= endCol <= 7):
                    endPiece = board[endRow][endCol]
                    if (endPiece == '--'):
                        moves.append(Move((r, c), (endRow, endCol), board))
                    elif (endPiece.id[0] == enemyColor):
                        moves.append(Move((r, c), (endRow, endCol), board))
                        break
                    else:
                        break
                else:
                    break
        if (whiteToMove and self.id[0] == 'w'):
            return moves
        elif ((not whiteToMove) and self.id[0] == 'b'):
            return moves
        else:
            return []
    
    def movesQueen(self, whiteToMove, r, c, board) -> List[Move]:
        moves = []
        moves.extend(self.movesBishop(whiteToMove, r, c, board) +
                     self.movesRock(whiteToMove, r, c, board))
        if (whiteToMove and self.id[0] == 'w'):
            return moves
        elif ((not whiteToMove) and self.id[0] == 'b'):
            return moves
        else:
            return []
        
    def movesKing(self, whiteToMove, r, c, board) -> List[Move]:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), 
                      (1, 1), (1, 0), (1, -1), (0, -1)]
        allyColor = ["b", "w"][whiteToMove]
        moves = []
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if (0 <= endRow <= 7 and 0 <= endCol <= 7):
                endPiece = board[endRow][endCol]
                if (endPiece == '--'):
                     moves.append(Move((r, c), (endRow, endCol), board))
                elif (endPiece.id[0] != allyColor):
                    moves.append(Move((r, c), (endRow, endCol), board))
        if (whiteToMove and self.id[0] == 'w'):
            return moves
        elif ((not whiteToMove) and self.id[0] == 'b'):
            return moves
        else:
            return []
    
    def moves(self, whiteToMove: bool,r: int, c: int,
              board: List[List[object]]) -> List[Move]:
        moves = []
        match self.id[1]:
            case 'p':
                moves.extend(self.movesPawn(whiteToMove, r, c, board))
            case 'R':
                moves.extend(self.movesRock(whiteToMove, r, c, board))
            case 'N':
                moves.extend(self.movesKnight(whiteToMove, r, c, board))
            case 'B':
                moves.extend(self.movesBishop(whiteToMove, r, c, board))
            case 'Q':
                moves.extend(self.movesQueen(whiteToMove, r, c, board))
            case 'K':
                moves.extend(self.movesKing(whiteToMove, r, c, board))
        return moves
            
    
    
    
class GameState:
    
    def __init__(self, scaled: tuple) -> None:
        '''
        Board is an 8x8 2d list.
        
        The firts character represents the color of the piece,
        'b' black and 'w' white. 
        
        The Second character represents the type pf the piece,
        King 'K', Queen 'Q', Bishop 'B', Knigth 'N', Castle 'R',
         Pawn 'p'.
         
         '--' represents an empty space with no piece.
        '''
        bp, wp = Piece('bp', scaled), Piece('wp', scaled)
        bQ, wQ = Piece('bQ', scaled), Piece('wQ', scaled)
        bB, wB = Piece('bB', scaled), Piece('wB', scaled)
        bK, wK = Piece('bK', scaled), Piece('wK', scaled)
        bN, wN = Piece('bN', scaled), Piece('wN', scaled)
        bR, wR = Piece('bR', scaled), Piece('wR', scaled)
        __ = '--' # Represents empty square
        self.board = [
            [bR, bN, bB, bQ, bK, bB, bN, bR],
            [bp, bp, bp, bp, bp, bp, bp, bp],
            [__, __, __, __, __, __, __, __],
            [__, __, __, __, __, __, __, __],
            [__, __, __, __, __, __, __, __],
            [__, __, __, __, __, __, __, __],
            [wp, wp, wp, wp, wp, wp, wp, wp],
            [wR, wN, wB, wQ, wK, wB, wN, wR]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
    
    def makeMove(self, move: Move) -> None:
        self.board[move.startRow][move.startCol] = '--' # empty square
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove # swap players
        # Update the king's location if moved
        if (move.pieceMoved.id == 'wK'):
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif (move.pieceMoved.id == 'bK'):
            self.blackKingLocation = (move.endRow, move.endCol)
    '''
    Undo the last move made
    '''
    def undoMove(self):
        # Make sure that there is a move to undo
        if (len(self.moveLog) != 0):
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if (move.pieceMoved.id == 'wK'):
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif (move.pieceMoved.id == 'bK'):
                self.blackKingLocation = (move.endRow, move.endCol)
            
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if (self.inCheck()):
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if (len(moves) == 0): # either checkmate or staleMate
            if (self.inCheck()):
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves
    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if (self.whiteToMove):
            return self.squareUnderAttack(*self.whiteKingLocation)
        else:
            return self.squareUnderAttack(*self.blackKingLocation)
    
    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponent's turn
        
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if ((move.endRow, move.endCol) == (r, c)):
                return True
        return False
    
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if (self.board[r][c] != '--'):
                    piece = self.board[r][c]
                    moves.extend(piece.moves(self.whiteToMove, r, c, self.board))
        return moves
    
   