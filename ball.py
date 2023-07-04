from turtle import Turtle
from paddle import Paddle
import random
 
MOVE = 50 # recall that 1 Brick spans a distance of 50 pixel

class Ball(Turtle):
    def __init__(self,YPAD):
        super().__init__()
        self.shape('square')
        self.color('white')
        self.penup()
        self.goto(0, YPAD+50)
        self.vx = random.randint(-2, 2) # random initial x velocity between -2 and 2
        self.vy = 1 # the initial y velocity is always exactly 1
        self.shapesize(stretch_wid=2.5, stretch_len=2.5)
    
    def wall_collision(self,paddle,bricks,HGrid,VGrid,YPAD): #check if the ball would collide with the wall and adjust speed and position in this case note that x has to be between -350 and 350 and y cannot exceed 275
        A= False
        MIN = -(HGrid/2)*50+0.5*50
        MAX = -1*MIN
        MINY= YPAD
        MAXY= YPAD + VGrid*50

        if self.ycor() + self.vy * MOVE < MINY:
            self.vx = random.randint(-2, 2)  # random initial x velocity between -2 and 2
            self.vy = 1  # the initial y velocity is always exactly 1
            self.setx(0)
            self.sety(YPAD + 50)
            paddle.speed = 0
            paddle.goto(x=0, y=YPAD)
            bricks.reset()
            return True
        if self.xcor()+self.vx*MOVE < MIN:
            self.setx(MIN)
            self.vx=-1*self.vx # reverse x velocity
            A = True
        if self.ycor()+self.vy*MOVE > MAXY:
            self.sety(MAXY)
            self.vy=-1*self.vy # reverse y velocity
            A = True
        if self.xcor()+self.vx*MOVE > MAX:
            self.setx(MAX)
            self.vx=-1*self.vx # reverse x velocity
            A = True
        return A
    
    def paddle_collision(self, paddle, YPAD): #check if the ball would collide with the paddle and adjust speed and position in this case
        A= True
        # !!!Important note: The x-coodinate of the paddle has to be updated last!, and only then can this function check for a collision on the current time step!!!
        # First I define the position of the 5 bricks of the paddle
        P1 = paddle.xcor()-100 # this is the center of the very left brick of the paddle
        P2 = P1+50
        P3 = P2+50
        P4 = P3+50
        P5 = P4+50 # this is the center of the very right brick of the paddle

        # Next I define the speed the the ball has after hitting. There are 5 possibilities, each corresponding to one possible speed after collision
        #the position is not changed only the speed upon collision with the paddle, because the absolute speed is always 1 in y direction
        # note that for the speed I follow the picture in the instruction
        # if self.ycor() < YPAD +75 and abs(self.xcor()+50 - P1)<35  and self.vx > 0: #does it hit left pixel?
        #     self.vy = 1
        #     self.vx = -2
        if abs(self.ycor() + (self.vy * MOVE) - YPAD) < 35 and abs(self.xcor() - P1)<35: #does it hit left pixel?
            self.vy = 1
            self.vx = -2 
        elif abs(self.ycor() + (self.vy * MOVE) - YPAD) < 35 and abs(self.xcor() - P2)<35:
            self.vy = 1
            self.vx = -1
        elif abs(self.ycor() + (self.vy * MOVE) - YPAD) < 35 and abs(self.xcor() - P3)<35:
            self.vy = 1
            self.vx = 0
        elif abs(self.ycor() + (self.vy * MOVE) - YPAD) < 35 and abs(self.xcor() - P4)<35:
            self.vy = 1
            self.vx = 1   
        elif abs(self.ycor() + (self.vy * MOVE) - YPAD) < 35 and abs(self.xcor() - P5)<35:
            self.vy = 1
            self.vx = 2
        # elif self.ycor() < YPAD +75 and abs(self.xcor()-50 - P5)<35 and self.vx < 0:
        #     self.vy = 1
        #     self.vx = 2
        else:
            A=False
        return A


    def update(self, paddle, bricks, HGrid, VGrid, YPAD): # this function defines the position update and also detects possible collisions
        # first I check for collisions with the paddle
        # The paddle has the highest priority, if a collision with the paddle happens, this is used to determine the ball
        # everything else is not checked anymore
        B = False
        A = self.paddle_collision(paddle, YPAD)
        if not A:
            B = self.wall_collision(paddle,bricks,HGrid,VGrid,YPAD)

        if not B and not A:
            bricks.check_for_collisions(self)

        self.setx(self.xcor()+self.vx*MOVE)
        self.sety(self.ycor()+self.vy*MOVE)

