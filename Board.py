# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 09:31:26 2018

@author: eumartinez

"""


from tkinter import *
from reversy import *
from tkinter import messagebox


class App:

    def __init__(self, master, game):
        self.frame = Frame(master)
        self.frame.pack()
        self.height = 600
        self.width = 600
        self.grid_column = 8
        self.grid_row = 8
        self.game = game  # Reversi Game
        self.canvas = Canvas(self.frame, height=self.height, width=self.width)
        self.cellwidth = int(self.canvas["width"])/self.grid_column
        self.cellheight = int(self.canvas["height"])/self.grid_row
        self.draw_grid()
        self.canvas.pack()
        self.pos = (0, 0)
        self.sv = StringVar()
        self.sv.set("white: 2 ===== black: 2")
        self.drawChips()
        self.lbl_score = Label(self.frame, textvariable=self.sv)

        def handler(event, self=self):
            return self.__onClick(event)

        self.canvas.bind('<Button-1>', handler)

        self.hi_there = Button(self.frame, text="Jugar",
                               command=self.start_Game)
        self.hi_there.pack(side=LEFT)
        self.lbl_score.pack(side=RIGHT)

    def draw_grid(self):
        for i in range(self.grid_row):
            for j in range(self.grid_column):
                x1 = i * self.cellwidth
                y1 = j * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")

    def drawChip(self):
        x = self.pos[1]*self.cellwidth
        y = self.pos[0]*self.cellheight
        if(self.game.current_player == HUMAN_PLAYER):
            self.canvas.create_oval(
                x, y, x+self.cellwidth, y+self.cellheight, fill='black')
        else:
            self.canvas.create_oval(
                x, y, x+self.cellwidth, y+self.cellheight, fill='white')

    def drawChips(self):
        for i in range(8):
            for j in range(8):
                val = self.game.board[i][j]
                print
                x = j*self.cellwidth
                y = i*self.cellheight
                if(val == HUMAN_PLAYER):
                    self.canvas.create_oval(
                        x, y, x+self.cellwidth, y+self.cellheight, fill='black')
                elif(val == AI_PLAYER):
                    self.canvas.create_oval(
                        x, y, x+self.cellwidth, y+self.cellheight, fill='white')

    def __onClick(self, event):
        if self.game.check_for_winner:
            sn, sb = self.game.get_board_score(self.game.board)
            messagebox.showinfo("Info", "Juego terminado, puntajes humano = {}, ai = {}.".format(
                sn, sb
            ))
            if sb > sn:
                messagebox.showinfo("Info", "Ganan ai")
            elif sb < sn:
                messagebox.showinfo("Info", "Ganan humano")
            else:
                messagebox.showinfo("Info", "Empate")
            return None

        i = int(event.y/self.cellheight)
        j = int(event.x/self.cellwidth)
        self.pos = (i, j)
        if self.game.no_moves and self.game.has_to_yield_turn(self.game.board, HUMAN_PLAYER):
            messagebox.showinfo(
                "Info", "Juego terminado, no hay movimientos válidos.")
            return None
        if self.game.current_player == HUMAN_PLAYER:
            if self.game.has_to_yield_turn(self.game.board, HUMAN_PLAYER):
                self.game.no_moves = True
                self.game.change_player()
                self.game.make_computer_move(self.game.board)
                return None
            elif self.game.make_move(self.game.board, self.game.current_player, i, j):
                self.game.no_moves = False
                self.game.change_player()
                self.game.make_computer_move(self.game.board)
            else:
                messagebox.showerror("Error", "Movimiento invalido.")
        score = self.game.get_board_score(self.game.board)
        self.sv.set("white: {} ===== black: {}".format(
            score[1],
            score[0]
        ))
        self.drawChips()

    def start_Game(self):
        print('start game')


r = Reversi()
root = Tk()
app = App(root, r)
root.mainloop()
