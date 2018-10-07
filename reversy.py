#! -*- coding: utf-8 -*-

"""
 1. Inicializar tablero, con posiciones iniciales.
 2. Validar movimiento.

"""
AI_PLAYER = 1 # blancas
HUMAN_PLAYER = -1 # negros
EMPTY = 0

class Reversi:

    def __init__(self):
        self.board = self.new_board()
        self.current_player = HUMAN_PLAYER
        self.init_board()

    def new_board(self):
        return [[EMPTY for _ in range(8)] for _ in range(8)]

    def init_board(self):
        self.tile_flip(AI_PLAYER, 3, 3)
        self.tile_flip(AI_PLAYER, 4, 4)
        self.tile_flip(HUMAN_PLAYER, 3, 4)
        self.tile_flip(HUMAN_PLAYER, 4, 3)
    
    def tile_flip(self, player, x, y):
        self.board[x][y] = player
    
    def on_board(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def is_valid(self, board, player, xi, yi):
        # Validar que se encuentre en el tablero y que sea vacio.
        if not self.on_board(xi, yi) or board[xi][yi] != EMPTY:
            return []
        
        other_player = AI_PLAYER if player == HUMAN_PLAYER else HUMAN_PLAYER

        dirs = [[0, 1], [1, 1], [-1, 1], [0, -1], [-1, -1], [1, -1], [1, 0], [-1, 0]]
        to_change = []
        for xdir, ydir in dirs:
            x, y = xi, yi
            x += xdir
            y += ydir

            if not self.on_board(x, y):
                continue
            
            # Buscamos en la dirección mientras 
            while board[x][y] == other_player:
                x += xdir
                y += ydir
                if not self.on_board(x, y):
                    break
            # LLegó al final del tablero así que no se busca más en esa dirección.
            if not self.on_board(x, y):
                continue
            # Encontró una pieza del otro jugador
            if board[x][y] == player:
                while True:
                    x -= xdir
                    y -= ydir
                    if x == xi and y == yi:
                        break
                    to_change.append([x, y])
        
        return to_change
    
    def make_move(self, board, player, xi, yi):
        to_change = self.is_valid(board, player, xi, yi)
        if len(to_change) > 0:
            # Cambiando fichas.
            board[xi][yi] = player
            for x, y in to_change:
                board[x][y] = player
            return True
        else:
            return False
    
    def score(self, board, player):
        black_score = 0
        white_score = 0

        for x in range(8):
            for y in range(8):
                if board[x][y] == AI_PLAYER:
                    white_score += 1
                elif board[x][y] == HUMAN_PLAYER:
                    black_score += 1
        
        if player == AI_PLAYER:
            return white_score - black_score
        else:
            return black_score - white_score

    
    def change_player(self):
        self.current_player = AI_PLAYER if self.current_player == HUMAN_PLAYER else HUMAN_PLAYER

