from turtle import Turtle
 
class Brick(Turtle):
    def __init__(self, x_cor, y_cor,YPAD): #note that x_cor, y_cor refer to the discrete grid ~15x10. The bottom left refers to the coordinate , the center of the paddle, 
        # by definition is in the position (0,1)
        super().__init__()
        self.penup()
        self.color('salmon')
        self.shape('square')
        self.shapesize(stretch_wid=2.35, stretch_len=7.35) # not that stretch_len should be set to 7.5 because a brick has len 7.5. 7.35 is only set optically fo ensure
        # the bricks are visually separated even if directly next to each other. This has no effect on caclculations.
        self.goto(x=x_cor*50, y=y_cor*50+YPAD)
 

