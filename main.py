import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Bricks
from TabularRL import Tabular
import math
 
# Have a grid of HGrid x VGrid 
HGrid = 11 # dont set below 5 otherwise the paddle is too large! it should also be an uneven number
VGrid = 11 # has to be an uneven number!
YPAD = -275 # set the permanent Y position of the paddle

#define the position of the bricks. Recall that 1 Brick extends 3 x 1, make sure they dont overlap
# IMPORTANT: bricks must have a minimum distance from wall and paddle of 2 empty blocks. Otherwise, collision check order will not work!
Coordinates = [[0,9],[3,9],[-3,9]]

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

# set the initial state of the game, this refers to the indices of the QA table

XB = 1
YB = 1
VBX = 1
VBY = 1
XP = 2 
VP = 2
BRICKS = 0

#Tabular.set_state(XB, YB, VBX, VBY, XP, VP, BRICKS, YPAD,HGrid, ball, paddle, bricks)

#alternatively set a random initial state

#XB, YB, VBX, VBY, XP, VP, BRICKS = Tabular.randome_state(HGrid, VGrid, bricks)
#Tabular.set_state(XB, YB, VBX, VBY, XP, VP, BRICKS, YPAD,HGrid, ball, paddle, bricks)


############## end of setting state


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

Test = Tabular(Coordinates, HGrid, VGrid)
N = 500000 # number of episodes for training
N2 = 1000 # print average return of N2 number of episodes very N2 number of episodes
E=0.1
Test.Train(N, N2, HGrid, VGrid, YPAD, paddle, ball, bricks, 0.1, True)

def playing_gameAI():

    # Scheduling the next time iteration already here to ensure 5 fps.
    # This also means that the function calls below in this loop MUST COMFORTABLY have less runtime than 200ms!
    tr.ontimer(playing_gameAI, 100)
    screen.update()
    Test.single_timestep(HGrid, VGrid, YPAD, paddle, ball, bricks, 0)
    

    if bricks.all_bricks_disappeared():
        print("GAME WON!")
        # game is won!



# We work with timers here, since using the main thread with sleep calls will mess up the UI as the thread gets unnecessarily blocked
tr.ontimer(playing_gameAI,200)
tr.mainloop()

# TODO @Edgar put your AI code here, outside the playing_game function to not run into UI issues.
#  As outlined above, use the all_bricks_disappeared function to check if a game is won. Also, simply use paddle.moveX functions to interact with the game; no special interface needed

