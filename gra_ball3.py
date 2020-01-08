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

class Game():
    '''Game canvas configuration and game variables like score and life '''
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        punk_pos_x = self.canvas_width - 80
        punk_pos_y = self.canvas_height - 20
        self.score = 0
        self.life = 3
        self.text_id = self.canvas.create_text(punk_pos_x, punk_pos_y, text='Points: {}'.format(self.score), font=("Arial", 15))
        self.text_life_id = self.canvas.create_text(40, punk_pos_y, text='Lifes: {}'.format(self.life), font=("Arial", 15))


    def points(self):
        '''refresh amount of points printed on canvas'''
        self.canvas.itemconfigure(self.text_id, text='Points: {}'.format(self.score))

    def lifes_update(self):
        '''refresh amount of lifes printed on canvas'''
        self.canvas.itemconfigure(self.text_life_id, text='Lifes: {}'.format(self.life))

class Ball():
    '''Ball object with all ball condisions '''
    def __init__(self, canvas, paddle, wall, color):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.paddle = paddle
        self.wall = wall
        self.wait = False #It is used when life is lost. It change to True for 3 ->def lost_life()
        self.is_multi_ball = False #it is used when there is more then 1 ball in play ->def multi_ball()
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.center_pos_x = self.canvas_width/2
        self.center_pos_y = self.canvas_height/2
        self.canvas.move(self.id, self.center_pos_x, self.center_pos_y)
        self.textgo_id = self.canvas.create_text(self.center_pos_x, self.center_pos_y, font=("Courier", 60))



    def hit_paddle(self, pos):
        '''Check if the Class Ball object is touching the paddle '''
        pos_paddle = self.canvas.coords(self.paddle.id)
        if pos[2] >= pos_paddle[0] and pos[0] <= pos_paddle[2]:
            if pos[3] >= pos_paddle[1] and pos[3] <= pos_paddle[3]:

                return True
        return False

    def hit_block(self, pos):
        '''Check if the Class Ball object is touching the the block '''
        for block in self.wall.blocks:
            if pos[0] <= block.pos_block[2] and pos[2] >= block.pos_block[0]:
                if pos[1] <= block.pos_block[3] and pos[1] >= block.pos_block[1]:
                    self.wall.blocks.remove(block) #Removes hitted block object from all blacks list
                    self.canvas.delete(block.id) #Removes hiited block from canvas
                    game.score += 1 #Add one point
                    game.points() #update points printed on canvas
                    return True
        return False

    def draw(self):
        '''Ball movements'''
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if self.wait == True: #after losing life condition is True for 3 sec.
            self.x = 0
            self.y = 0
            self.lost_life()
        else:
            if pos[1] <= 0:
                self.y = 3
            if pos[3] >= self.canvas_height:
                #self.hit_bottom = True
                if len(balls) == 1:
                    game.life -= 1
                    game.lifes_update()
                    self.time_start = time.time() #Record time for 3 sec. delay
                    self.lost_life()
                else:

                    self.canvas.delete(self.id)
                    balls.remove(self)
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

    def game_over(self):
        '''Game over printed on canvas '''
        self.canvas.delete(self.id) # Removes ball from canvas
        self.canvas.itemconfigure(self.textgo_id, text="GAME OVER") #Prints Game Over on canvas

    def lost_life(self):
        '''lost life actions'''
        self.canvas.coords(self.id, self.center_pos_x, self.center_pos_y, self.center_pos_x+15, self.center_pos_y+15)
        #Moves ball in the middle of the canvas
        if time.time() - self.time_start <= 3: #Condition for 3sec. delay
            self.wait = True
        else: #Afer 3sec. delay random direction is set
            self.wait = False
            self.y = -3
            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]

    def multi_ball(self):
        '''Adds extra 2 balls to the game '''
        balls.append(Ball(canvas, paddle, wall, 'blue'))
        balls.append(Ball(canvas, paddle, wall, 'yellow'))
        self.is_multi_ball = True

class Paddle():

    def __init__(self, canvas, color):
        '''Initializing paddle'''
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.paddle_start_poz_x = self.canvas_width/2
        self.paddle_start_poz_y = self.canvas.winfo_height() - 50
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, self.paddle_start_poz_x, self.paddle_start_poz_y)
        self.x = 0
        self.evt = None
        self.start = False
        self.grown = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyRelease-Left>', self.no_turn)
        self.canvas.bind_all('<KeyRelease-Right>', self.no_turn)
        self.canvas.bind_all('<Button-1>', self.run)


    def draw(self):
        '''Paddle movements '''
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0: #If at the canvas border condition
            self.x = 0
        if pos[2] >= self.canvas_width: #If at the canvas border condition
            self.x = 0

    def no_turn(self, evt):
        '''If key released action'''
        self.evt = None

    def turn_right(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[2] < self.canvas_width: #If not at the canvas border condition
            self.x = 5
            self.evt = evt
            #self.canvas.move(self.id, self.x, 0)

    def turn_left(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[0] > 0: #If not at the canvas border condition
            self.x = -5
            self.evt = evt
        #self.canvas.move(self.id, self.x, 0)

    def run(self, evt):
        '''Click mouse button at the beginnig action '''
        self.start = True

    def paddle_grow(self):
        '''Resize a paddle x1.5'''
        paddle_poz = self.canvas.coords(self.id)
        if paddle_poz[0] < self.paddle_start_poz_x: #if paddle on the left side of canvas
            self.canvas.coords(self.id, paddle_poz[0], paddle_poz[1], paddle_poz[2] + 50, paddle_poz[3])
        else: #if paddle on the right side of canvas
            self.canvas.coords(self.id, paddle_poz[0] - 50, paddle_poz[1], paddle_poz[2], paddle_poz[3])
        #self.canvas.scale(self.id, 0, 0, 1.5, 1)
        self.grown = True # Set True if grown

class Blocks():
    ''' Block objects'''
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
        '''Remove block from canvas'''
        self.canvas.delete(id)

class Wall():
    '''Wall of blocks objects '''
    def __init__(self, canvas):
        self.blocks = []
        self.canvas = canvas

    def populate(self, count):
        '''Populate self.blocks list with class Blocks objects. Every block with
        specific position on canvas
        '''
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
        '''Random color generator '''
        colour = ['red', 'green', 'blue', 'cyan', 'pink', 'orange']
        while True:
            for color in colour:
                random.shuffle(colour)
                yield color

tk = Tk()
tk.title("Arkanoid")
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

game = Game(canvas)
wall = Wall(canvas)
wall.populate(48) # draw wall of specific number of bricks
paddle = Paddle(canvas, 'green')
balls = []
balls.append(Ball(canvas, paddle, wall, 'red')) # Ball is created as list element because
                                                # there can by more than 1 ball in the game
                                                # at the same time

while True:
    if paddle.start == True: # If mouse click
        if game.life > 0: # If there are 1 or more lifes left condition
            for ball in balls: # There can be more than one ball
                #game.points()
                #game.lifes_update()
                ball.draw()
            if paddle.evt != None: #Paddle control. If key released paddle.evt set to None -> no drow (paddle movement)
                if paddle.evt.keysym == 'Right':
                    paddle.draw()
                elif paddle.evt.keysym == 'Left':
                    paddle.draw()

            if game.life <= 1 and paddle.grown == False: #if 1 life left condition
                paddle.paddle_grow() #paddle will grow 1.5 times
            if game.score == 10 and balls[0].is_multi_ball == False: #If 10 points acquired. is_multi_ball variable prevent from mutiple ball multiplications
                balls[0].multi_ball() #create additional 2 ball and set is_multi_ball to True
        else:
            balls[0].game_over()
    #tk.update_idletasks()
    tk.update()
    time.sleep(0.01)



#tk.mainloop()
