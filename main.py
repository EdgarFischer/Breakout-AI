import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Bricks
from TabularRL import Tabular
import math
import numpy as np
import random
import matplotlib.pyplot as plt
 
# Have a grid of HGrid x VGrid 
HGrid = 15 # dont set below 5 otherwise the paddle is too large! it should also be an uneven number
VGrid = 11 # has to be an uneven number!
YPAD = -275 # set the permanent Y position of the paddle

#define the position of the bricks. Recall that 1 Brick extends 3 x 1, make sure they dont overlap
# IMPORTANT: bricks must have a minimum distance from wall and paddle of 2 empty blocks. Otherwise, collision check order will not work!
Coordinates = [[0,9],[3,9],[-3,9],[1,8],[4,8],[-2,8],[0,7],[3,7],[-3,7],[0,6]]
AI = Tabular.load_tabular_object('Qtable_Bricks3_ONPMC') # load the correct AI here

screen = tr.Screen()
screen.setup(width=780, height=650) # this should not be changed, to display the game correctly
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0)

#This adds a frame to the game. This is soley for asthetics and has no real effect
LEFT = tr.Turtle()
LEFT.penup()
LEFT.color('lightblue')
LEFT.shape('square')
LEFT.goto(-50*math.ceil(HGrid/2), YPAD+50*VGrid/2)
LEFT.shapesize(stretch_wid=2.5*(1+VGrid), stretch_len=2.5)
RIGHT = tr.Turtle()
RIGHT.penup()
RIGHT.color('lightblue')
RIGHT.shape('square')
RIGHT.goto(50*math.ceil(HGrid/2), YPAD+50*VGrid/2)
RIGHT.shapesize(stretch_wid=2.5*(1+VGrid), stretch_len=2.5)
TOP = tr.Turtle()
TOP.penup()
TOP.color('lightblue')
TOP.shape('square')
TOP.goto(0, YPAD+50*(1+VGrid))
TOP.shapesize(stretch_wid=2.5, stretch_len=2.5*(2+HGrid))
########################### End of Frame definiton


paddle = Paddle(YPAD)
ball = Ball(YPAD)
bricks = Bricks(Coordinates, YPAD)
# set the coordinate for Bricks


playing_game = True
 
 
screen.listen()
screen.onkey(key='Left', fun=paddle.move_left)
screen.onkey(key='Right', fun=paddle.move_right)
 
def playing_game():
    # Scheduling the next time iteration already here to ensure 5 fps.
    # This also means that the function calls below in this loop MUST COMFORTABLY have less runtime than 200ms!
    tr.ontimer(playing_game, 200)
    ball.update(paddle, bricks, HGrid,VGrid,YPAD)
    paddle.update(HGrid)
    screen.update()

    if bricks.all_bricks_disappeared():
        print("GAME WON!")
        # game is won!

Return = 0
last_vx = -2
returnsarr = [[],[],[],[],[]]
def playing_gameAI():
    global Return
    global last_vx
    # Scheduling the next time iteration already here to ensure 5 fps.
    # This also means that the function calls below in this loop MUST COMFORTABLY have less runtime than 200ms!
    tr.ontimer(playing_gameAI, 7)
    move,reset,state = AI.single_timestep(HGrid, VGrid, YPAD, paddle, ball, bricks, 0, resolve_random=True)
    if reset:
        print("GAME LOST!")
        Return -= 250
        returnsarr[last_vx + 2].append(Return)
        print(returnsarr)
        Return = 0
        ball.reset_game(paddle, bricks, YPAD)
        last_vx += 1
        if last_vx == 3:
            last_vx = -2
        ball.vx = last_vx
        screen.update()
        return
    Return += -1
    if bricks.all_bricks_disappeared():
        print("GAME WON!")
        returnsarr[last_vx+2].append(Return)
        print(returnsarr)
        Return = 0
        ball.reset_game(paddle, bricks, YPAD)
        last_vx += 1
        if last_vx == 3:
            last_vx = -2
        ball.vx = last_vx
    screen.update()


# We work with timers here, since using the main thread with sleep calls will mess up the UI as the thread gets unnecessarily blocked
ball.vx = -2
tr.ontimer(playing_gameAI,200)
tr.mainloop()


# Average Return for Bricks1ONP: [-58.97058824, -65.79411765, -53.35294118, -65.82352941, -65.29411765]
# Return for Bricks1OFFP: [-50, -50, -50, -58, -50]
# Average Return for Bricks2ONP: [-57.76470588, -53.11764706, -53.52941176, -47.29411765, -57.58823529]
# Return for Bricks2OFFP: [-44, -54, -48, -41, -44]
# Average Return for Bricks3ONP: [-261,  -83.36666667,  -87.73333333,  -90.66666667,-261]
# Return for Bricks3OFFP: [-96, -92, -88, -78, -85]


