# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 09:31:26 2018

@author: eumartinez

"""


from tkinter import *
from reversy import *

class App:
       
    def __init__(self, master, game):
        self.frame = Frame(master)
        self.frame.pack()
        self.height=600
        self.width=600
        self.grid_column=8
        self.grid_row=8
        self.game = game # Reversi Game
        self.canvas = Canvas(self.frame, height=self.height, width=self.width)
        self.cellwidth = int(self.canvas["width"])/self.grid_column
        self.cellheight = int(self.canvas["height"])/self.grid_row
        self.draw_grid()
        self.canvas.pack()
        self.pos=(0,0)
        self.drawChips()
        
        
        def handler(event, self=self):
            return self.__onClick(event)
        
        self.canvas.bind('<Button-1>', handler)
        
        
        self.hi_there = Button(self.frame, text="Jugar", command=self.start_Game)
        self.hi_there.pack(side=LEFT)
        
    
    def draw_grid(self):
        for i in range(self.grid_row):
            for j in range(self.grid_column):
                x1 = i * self.cellwidth
                y1 = j * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
        
        
    def drawChip(self):
        x=self.pos[1]*self.cellwidth
        y=self.pos[0]*self.cellheight
        if(self.game.current_player == HUMAN_PLAYER):
            self.canvas.create_oval(x,y,x+self.cellwidth,y+self.cellheight, fill='black')
        else:
            self.canvas.create_oval(x,y,x+self.cellwidth,y+self.cellheight, fill='white')
            
    
    def drawChips(self):
        for i in range(8):
            for j in range(8):
                val=self.game.board[i][j]
                print
                x=j*self.cellwidth
                y=i*self.cellheight
                if(val == HUMAN_PLAYER):
                    self.canvas.create_oval(x,y,x+self.cellwidth,y+self.cellheight, fill='black')
                elif(val == AI_PLAYER):
                    self.canvas.create_oval(x,y,x+self.cellwidth,y+self.cellheight, fill='white')
            
    def __onClick(self, event):
        
            i=int(event.y/self.cellheight)
            j=int(event.x/self.cellwidth)
            self.pos =(i,j)
            if self.game.make_move(self.game.board, self.game.current_player, i , j):
                self.game.change_player()
            else:
                print("Error")
            
            self.drawChips()
        
       
    
    def  start_Game(self):
        print('start game')
        
        
r = Reversi()
root = Tk()
app = App(root, r)
root.mainloop()