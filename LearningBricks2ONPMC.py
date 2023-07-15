import turtle as tr

import TabularRL
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

Coordinates = [[-3,9],[3,9],[-3,7],[3,7],[-3,5],[3,5],[0,8],[0,6]]

screen = tr.Screen()
screen.setup(width=780, height=650) # this should not be changed, to display the game correctly
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0)
paddle = Paddle(YPAD)
ball = Ball(YPAD)
bricks = Bricks(Coordinates, YPAD)

AI = Tabular(Coordinates, HGrid, VGrid)
N = 1000000 # number of episodes for training
N2 = 1000 # print average return of N2 number of episodes very N2 number of episodes
Episode, Returns = AI.Train(TabularRL.STRATEGY_ON_POLICY_E_SOFT_EVERY_VISIT, TabularRL.EPISODE_SETTING_GAME, N, N2, HGrid, VGrid, YPAD, paddle, ball, bricks, 0.02, None)

# Timesteps = [-x for x in Returns]

plt.scatter(Episode, Returns)
plt.xlabel('Training episode')
plt.ylabel('Average timesteps of last {} episodes'.format(N2))
plt.yscale('log')
plt.title('Convergence plot')
plt.savefig('Convergence_Bricks2_ONPMC.png')
plt.show()


Tabular.save_tabular_object(AI, 'Qtable_Bricks2_ONPMC')