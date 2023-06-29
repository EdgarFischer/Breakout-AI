
from turtle import Turtle
 # !!note!!: The entire code is based on 1 Grid point having 50x50 pixels

# Have a grid of HGrid x VGrid NEEDS TO BE CONSISTENTLY SET IN THE BALL CLASS!!!!
#HGrid = 15 # dont set below 5 otherwise the paddle is too large!
#VGrid = 10
#YPAD = -225 # set the permanent Y position of the paddle

class Paddle(Turtle):
    def __init__(self,YPAD):
        super().__init__() # this creates a turtle object with default initialization
        self.color('steel blue')
        self.shape('square')
        self.penup() # Lifts the pen of the paddle, so it doesn't leave a trace when moving.
        self.shapesize(stretch_wid=2.5, stretch_len=12.5) # this defines the size of the paddle, note that the default tutrtle size is 20x20 pixels and the size od the paddle strech_wid*20 X stretch_len*20
        self.goto(x=0, y=YPAD) # x= 0 : paddle is at center of screen wrt x-axis, the bottom refers to -5 brigs or -250 pixels, due to the thickness of 50 pixels thats -225 pixels 
        self.speed = 0

    def move_left(self): # this lowers the speed by -1
        if self.speed == -2:
            self.speed +=0 # dont allow for the speed to go below -2
        else:
            self.speed +=-1

    def move_right(self): # this lowers the speed by -1
        if self.speed == 2:
            self.speed +=0 # dont allow for the speed to go below -2
        else:
            self.speed +=1
    
    def update(self,HGrid):
        MOVE_DIST = abs(self.speed) * 50 # recall that 50 pixels refer to 1 grid point
        if self.speed < 0:
            self.backward(MOVE_DIST)
        else:
            self.forward(MOVE_DIST)
        # lastly I check that it is impossible to exist the screen. Since the minimum allowed x value has to refer to -7.5 bricks = -375 pixels
        # (same for positive) the paddle must not violate these values. The paddle has a thickness of 5 bricks or 250 pixels, the x coordinate
        # refers to the center of the paddle. This means that the paddle cannot go below -250 or above 250
        MIN = -(HGrid/2)*50+2.5*50
        MAX = -1*MIN
        if self.xcor() < MIN:
            self.setx(MIN)
            self.speed =0
        elif self.xcor() > MAX:
            self.setx(MAX)
            self.speed =0

