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

Coordinates = [[0,9],[3,9],[-3,9],[1,8],[4,8],[-2,8],[0,7],[3,7],[-3,7],[0,6]]

screen = tr.Screen()
screen.setup(width=780, height=650) # this should not be changed, to display the game correctly
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0)
paddle = Paddle(YPAD)
ball = Ball(YPAD)
bricks = Bricks(Coordinates, YPAD)

AI = Tabular(Coordinates, HGrid, VGrid)
N = 1000 # number of episodes for training
N2 = 50 # print average return of N2 number of episodes very N2 number of episodes
MAX = 50000 # maximum number of time steps, this is necessary to avoid a poor policy having an infinite game
E=0 # possible epsilon for epsilon greedy. Has to be set to 0 to guarante convergence
Episode, Returns =AI.Train(N, N2, HGrid, VGrid, YPAD, paddle, ball, bricks, E, True, MAX)

Timesteps = [-x for x in Returns]

plt.scatter(Episode, Timesteps)
plt.xlabel('Training episode')
plt.ylabel('Average timesteps of last 1000 episodes')
plt.yscale('log')
plt.title('Convergence plot')
plt.savefig('ConvergenceQTable1.png')
plt.show()


Tabular.save_tabular_object(AI, 'Qtable1')