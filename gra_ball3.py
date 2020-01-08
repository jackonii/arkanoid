#!/usr/bin/python3

'''
Arkanoid game
Mouse click to start the game.
Cursors Right Left to control the paddle.
When 10 points acquired game adds extra 2 ball.
When 1 last life left the paddle will grow to 1,5 of its size.

'''

from tkinter import *

import random, time

class Ball():
    def __init__(self, canvas, paddle, wall, color):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.paddle = paddle
        self.wall = wall
        self.wait = False
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.score = 0
        self.life = 3
        punk_pos_x = self.canvas_width - 80
        punk_pos_y = self.canvas_height - 20
        self.center_pos_x = self.canvas_width/2
        self.center_pos_y = self.canvas_height/2
        self.canvas.move(self.id, self.center_pos_x, self.center_pos_y)
        self.text_id = self.canvas.create_text(punk_pos_x,punk_pos_y, text='Points: {}'.format(self.score), font=("Arial", 15))
        self.textgo_id = self.canvas.create_text(self.center_pos_x,self.center_pos_y, font=("Courier", 60))
        self.text_life_id = self.canvas.create_text(40, punk_pos_y, text='Lifes: {}'.format(self.life), font=("Arial", 15))

    def hit_paddle(self, pos):
        pos_paddle = self.canvas.coords(self.paddle.id)
        if pos[2] >= pos_paddle[0] and pos[0] <= pos_paddle[2]:
            if pos[3] >= pos_paddle[1] and pos[3] <= pos_paddle[3]:
                #self.score += 1
                return True
        return False

    def hit_block(self, pos):
        for block in self.wall.blocks:
            if pos[0] <= block.pos_block[2] and pos[2] >= block.pos_block[0]:
                if pos[1] <= block.pos_block[3] and pos[1] >= block.pos_block[1]:
                    self.wall.blocks.remove(block)
                    self.canvas.delete(block.id)
                    self.score += 1
                    return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if self.wait == True:
            self.x = 0
            self.y = 0
            self.lost_life()
        else:
            if pos[1] <= 0:
                self.y = 3
            if pos[3] >= self.canvas_height:
                #self.hit_bottom = True
                self.life -= 1
                self.lifes_update()
                self.time_start = time.time()
                self.lost_life()
                #self.y = 0
                #self.x = 0
            if self.hit_paddle(pos) == True:
                self.y = -3
            if self.hit_block(pos) == True:
                self.y = self.y*(-1)

            if pos[0] <= 0:
                self.x = 3
            if pos[2] >= self.canvas_width:
                self.x = -3

    def points(self):
        self.canvas.itemconfigure(self.text_id, text='Points: {}'.format(self.score))

    def lifes_update(self):
        self.canvas.itemconfigure(self.text_life_id, text='Lifes: {}'.format(self.life))

    def game_over(self):
        self.canvas.itemconfigure(self.textgo_id, text="GAME OVER")

    def lost_life(self):
        self.canvas.coords(self.id, self.center_pos_x, self.center_pos_y, self.center_pos_x+15, self.center_pos_y+15)
        if time.time() - self.time_start <= 3:
            self.wait = True
        else:
            self.wait = False
            self.y = -3
            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]



class Paddle():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.paddle_start_poz_x = self.canvas_width/2
        self.paddle_start_poz_y = self.canvas.winfo_height() - 50
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, self.paddle_start_poz_x, self.paddle_start_poz_y)
        self.x = 0
        self.start = False
        self.grown = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Button-1>', self.run)


    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def turn_right(self, evt):
        self.x = 5

    def turn_left(self, evt):
        self.x = -5

    def run(self, evt):
        self.start = True

    def paddle_grow(self):
        paddle_poz = self.canvas.coords(self.id)
        if paddle_poz[0] < self.paddle_start_poz_x:
            self.canvas.coords(self.id, paddle_poz[0], paddle_poz[1], paddle_poz[2] + 50, paddle_poz[3])
        else:
            self.canvas.coords(self.id, paddle_poz[0] - 50, paddle_poz[1], paddle_poz[2], paddle_poz[3])
        #self.canvas.scale(self.id, 0, 0, 1.5, 1)
        self.grown = True

class Blocks():
    def __init__(self, canvas, x=0, y=0, color='red'):
        self.canvas = canvas
        self.blocks = []
        #self.color = color
        self.id = canvas.create_rectangle(0, 0, 62, 20, fill=color)
        self.x = x
        self.y = y
        self.canvas.move(self.id, self.x, self.y)
        self.pos_block = self.canvas.coords(self.id)

    def rem_block(self, id):
        self.canvas.delete(id)

class Wall():
    def __init__(self, canvas):
        self.blocks = []
        self.canvas = canvas

    def populate(self, count):
        self.canvas_width = self.canvas.winfo_width()
        self.x = 0
        self.y = 0
        color_gen = self.change_color()
        for i in range(count):
            self.blocks.append(Blocks(canvas, self.x, self.y, color=next(color_gen)))
            self.x += 67
            if self.x > self.canvas_width - 50:
                self.y += 50
                self.x = 0
    def change_color(self):
        colour = ['red', 'green', 'blue', 'cyan', 'pink', 'orange']
        while True:
            for color in colour:
                random.shuffle(colour)
                yield color

tk = Tk()
tk.title("Game")
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

wall = Wall(canvas)
wall.populate(48)
paddle = Paddle(canvas, 'green')
ball = Ball(canvas, paddle, wall, 'red')

while True:
    if paddle.start == True:
        if ball.life > 0:
            ball.points()
            ball.lifes_update()
            ball.draw()
            paddle.draw()
            if ball.life <= 1 and paddle.grown == False:
                paddle.paddle_grow()
        else:
            ball.game_over()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)



#tk.mainloop()
