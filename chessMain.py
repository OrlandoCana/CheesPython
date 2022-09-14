'''
This file is responsible for handling user input 
and displaying the current game state object.

create by OrlandoCana
'''

import pygame as pg
import chessEngine

WIDTH = HEIGHT = 512 
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

def main() -> None:
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('White'))
    gs = chessEngine.GameState((SQ_SIZE, SQ_SIZE))
    running = True
    while running:
        for event in pg.event.get():
            if (event.type == pg.QUIT):
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()
        
'''
Responsible for all the graphics within a current game state
'''
def drawGameState(screen, gs) -> None:
    drawBoard(screen)
    drawPieces(screen, gs.board)
    
'''
Draw the squares on the board
'''
def drawBoard(screen) -> None:
     colors = [pg.Color('light gray'), pg.Color('dark red')]
     for r in range(DIMENSION):
         for c in range(DIMENSION):
             color = colors[(r+c)%2]
             pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, 
                                                 SQ_SIZE, SQ_SIZE))
     
 
'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board) -> None:
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if (piece != '--'): # Not empty square
                screen.blit(piece.image, pg.Rect(c*SQ_SIZE, r*SQ_SIZE,
                                                   SQ_SIZE, SQ_SIZE))
                
if (__name__ == '__main__'):
    main()
    