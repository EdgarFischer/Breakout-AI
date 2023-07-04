import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Bricks
import math

 
# Have a grid of HGrid x VGrid 
HGrid = 15 # dont set below 5 otherwise the paddle is too large! it should also be an uneven number
VGrid = 11
YPAD = -275 # set the permanent Y position of the paddle

#define the position of the bricks. Recall that 1 Brick extends 3 x 1, make sure they dont overlap
Coordinates = [[0,9],[3,9],[-3,9],[1,8],[4,8],[-2,8],[0,7],[3,7],[-3,7],[0,6]]

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
########################### End of Fram definiton


paddle = Paddle(YPAD)
ball = Ball(YPAD)
bricks = Bricks(Coordinates, YPAD)
# set the coordinate for Bricks

playing_game = True
 
 
screen.listen()
screen.onkey(key='Left', fun=paddle.move_left)
screen.onkey(key='Right', fun=paddle.move_right)

 
def playing_game():
    tr.ontimer(playing_game, 200)
    ball.update(paddle, bricks, HGrid,VGrid,YPAD)
    paddle.update(HGrid)
    screen.update()

    if bricks.all_bricks_disappeared():
        print("GAME WON!")
        # TODO game is won! Put here the code what happens in this case!



tr.ontimer(playing_game,200)
tr.mainloop()