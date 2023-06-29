import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Brick
import math
import time
 
# Have a grid of HGrid x VGrid 
HGrid = 15 # dont set below 5 otherwise the paddle is too large! it should also be an uneven number
VGrid = 10
YPAD = -225 # set the permanent Y position of the paddle

#define the position of the bricks. Recall that 1 Brick extends 3 x 1, make sure they dont overlap
Coordinates = [[0,9],[3,9],[-3,9]]

screen = tr.Screen()
screen.setup(width=780, height=600) # this should not be changed, to display the game correctly
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
########################### End of Fram definiton


paddle = Paddle(YPAD)
ball = Ball(YPAD)

# set the coordinate for Bricks

Bricks = []
for i in Coordinates:
    Bricks.append(Brick(i[0],i[1],YPAD))

playing_game = True
 
 
screen.listen()
screen.onkey(key='Left', fun=paddle.move_left)
screen.onkey(key='Right', fun=paddle.move_right)

 
while playing_game:
    ball.update(paddle, HGrid,VGrid,YPAD)
    paddle.update(HGrid)
    screen.update()
    
    time.sleep(0.2) # this defines the framerate

 
tr.mainloop()