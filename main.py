import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Bricks
import time
 
# Have a grid of HGrid x VGrid 
HGrid = 20 # dont set below 5 otherwise the paddle is too large!
VGrid = 10
YPAD = -225 # set the permanent Y position of the paddle

screen = tr.Screen()
screen.setup(width=780, height=600) # this should not be changed, to display the game correctly
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0)
 
paddle = Paddle(YPAD)
ball = Ball(YPAD)
 
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