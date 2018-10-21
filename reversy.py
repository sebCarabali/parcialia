#! -*- coding: utf-8 -*-

"""
 1. Inicializar tablero, con posiciones iniciales.
 2. Validar movimiento.

"""
AI_PLAYER = 1 # blancas
HUMAN_PLAYER = -1 # negros
EMPTY = 0
DEPTH = 2

class Reversi:

    def __init__(self):
        self.board = self.new_board()
        self.current_player = HUMAN_PLAYER
        self.no_moves = False
        self.check_for_winner = False
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
            if self.is_full_board(board):
                self.check_for_winner = True
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

    def actions(self, state, player):
        actions = []
        for x in range(8):
            for y in range(8):
                if len(self.is_valid(state, player, x, y)) > 0:
                    actions.append([x, y])
        return actions
    
    def make_copy(self, state):
        new_state = self.new_board()
        for x in range(8):
            for y in range(8):
                new_state[x][y] = state[x][y]
        return new_state

    def make_computer_move(self, state):
        if self.has_to_yield_turn(state, AI_PLAYER):
            self.change_player()
            self.no_moves = True
            return None
        else:
            move = self.minimax_decision(state, self.current_player)
            x, y = move
            self.no_moves = False
            self.make_move(state, self.current_player, x, y)
            self.change_player()

    def minimax_decision(self, state, player):
        other_player = AI_PLAYER if player == HUMAN_PLAYER else HUMAN_PLAYER
        move_list = self.actions(state, player)

        if len(move_list) == 0:
            return [-1, -1]
        else:
            best_score = -float("inf")
            best_move = [-1,-1]
            
            for x, y in move_list:
                state_copy = self.make_copy(state)
                self.make_move(state_copy, player, x, y)
                val = self.minimax_value(state_copy, player, other_player, 1)

                if val > best_score:
                    best_score = val
                    best_move = [x, y]
            
            return best_move

    def is_full_board(self, state):
        for x in range(8):
            for y in range(8):
                if state[x][y] == EMPTY:
                    return False
        return True

    def minimax_value(self, state, original_player, current_player, search_ply):
        if search_ply == DEPTH or self.is_full_board(state):
            return self.score(state, original_player)
        
        other_player = AI_PLAYER if current_player == HUMAN_PLAYER else HUMAN_PLAYER
        
        move_list = self.actions(state, current_player)

        if len(move_list) == 0:
            return self.minimax_value(state, original_player, other_player, search_ply + 1)
        else:
            best_score = -float("inf")
            if original_player != current_player:
                best_score = float("inf")
            
            for x, y in move_list:
                copy_state = self.make_copy(state)
                self.make_move(copy_state, current_player, x, y)
                val = self.minimax_value(copy_state, original_player, other_player, search_ply + 1)

                if original_player == current_player:
                    if val > best_score:
                        best_score = val
                else:
                    if val < best_score:
                        best_score = val
            return best_score

    def is_game_over(self):

        pass

    def has_to_yield_turn(self, state, player):
        has_to_yield = True
        possible_moves = self.actions(state, player)
        if len(possible_moves) > 0:
            has_to_yield = False
        return has_to_yield
    
    def get_board_score(self, state):
        bscore = 0
        wscore = 0

        for x in range(8):
            for y in range(8):
                if state[x][y] == AI_PLAYER:
                    wscore += 1
                elif state[x][y] == HUMAN_PLAYER:
                    bscore += 1
        return (bscore, wscore)

