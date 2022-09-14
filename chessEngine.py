import pygame as pg

'''
this class represents a piece of chees game
'''
class Piece:
    def __init__(self, id: str, scaled: tuple) -> None:
        self.id = id
        image = pg.image.load(f'images/{self.id}.png')
        self.image = pg.transform.scale(image, scaled)

'''
this class is responsible for storing all the information about
the current state of a chess game. It will also be responsible 
for determining the valid moves at the current state. It will also kepp 
a move log.
''' 
class GameState:
    def __init__(self, scaled: tuple) -> None:
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
        
