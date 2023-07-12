import numpy as np
import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Bricks
import math
import random
import pickle
import os

STRATEGY_EXPLORING_STARTS_FIRST_VISIT = 'exploring_starts_first_visit'
STRATEGY_ON_POLICY_E_SOFT_FIRST_VISIT = 'on_policy_e_soft_first_visit'
STRATEGY_ON_POLICY_E_SOFT_EVERY_VISIT = 'on_policy_e_soft_every_visit'
EPISODE_SETTING_CAPPED = 'episode_setting_capped'
EPISODE_SETTING_GAME = 'episode_setting_game'

class Tabular:   # the tabular object creates a state-action table with all possibilities
    def __init__(self,Coordinates, HGrid, VGrid):
        N = len(Coordinates)
        self.QA = np.zeros((HGrid, VGrid+1, 5, 2, HGrid-4, 5, 2**N, 3), dtype=np.int32)   
        self.AReturns = np.zeros((HGrid, VGrid+1, 5, 2, HGrid-4, 5, 2**N, 3,), dtype=np.int32) #average returns
        self.COUNTER = np.zeros((HGrid, VGrid+1, 5, 2, HGrid-4, 5, 2**N, 3,), dtype=np.int32)
        # QA will be the value function for state action pairs. For easier accessbility
        # I use a multidimensional tensor to save all state action pais using the numpy library
        # the logic is as follows:
        # 1. The first entry is the x-position of the ball
        # 2. the second entry the y-position of the ball
        # 3. speed of ball in x direction
        # 4. speed of ball in y direction
        # 5. position of paddle (only x direction relevant)
        # 6. x-speed of paddle
        # 7. does brick exist y/bn
        # 8. take action left / right / none

        # note that the COUNTER simply counts how often states have occured. This is important
        # for updating averages without having to save all elements that have occurred.

    # Save Tabular object to a file in the current working directory
    @staticmethod
    def save_tabular_object(tabular_obj, file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'wb') as file:
            pickle.dump(tabular_obj, file)

    # Load Tabular object from a file in the current working directory
    @staticmethod
    def load_tabular_object(file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'rb') as file:
            tabular_obj = pickle.load(file)
        return tabular_obj

    @staticmethod
    def get_brick_existence(bricks): # checks which brick is still in the game
        N = len(bricks.brick_array)
        output = np.zeros(N, dtype=np.int32) 
        i = 0
        for brick in bricks.brick_array:
            if brick.isvisible(): # check if brick is still in the game 1 = yes 0 = no
                output[i] = 1
            i = i+1
        # so far output contains N entries with 1 (brick there) of 0 (not there). I want to convert that into a single number
        # for which I interpret that as a base 2 representation of a natural number
        OUT = 0
        i=0
        reversed_output = output[::-1] # note that the last element refers to 0 or 1, second last to 2 or 0 etc thats why I reverse the array
        for k in reversed_output:
            OUT += reversed_output[i]*2**(i)
            i = i+1
        return int(OUT)
    
    @staticmethod
    def get_paddle_pos(paddle, HGrid): # note that the paddle position is so far saved in pixel position, not on the game grid of HGrid x VGrid
        # I want the very left part of the paddle to define its position, such that its position then runs from 1 to HGrid-5
        Shift = math.ceil(HGrid/2)
        X = paddle.xcor()//50 + Shift-2 # the minus 2 comes from the fact that the minimum position of the center has to be 3, which is what the xcor refers to
        # however since I want to save X as the position of the left corner (which is always 2 left from the center) I have to subtract 2
        return X
    
    @staticmethod
    def get_ball_pos(ball, HGrid, YPad): # note that the paddle position is so far saved in pixel position, not on the game grid of HGrid x VGrid
        # the smallest x value is now 1 and the largest HGrid, same for y axis
        ShiftX = math.ceil(HGrid/2)
        ShiftY = 1# note that usually the smallest y values is ypad, if I ad -ypad to all first, it is 1,,
        X = ball.xcor()//50 + ShiftX
        Y = (ball.ycor()-YPad)//50 + ShiftY
        return [X, Y]
    
    def get_state(self, ball, paddle, HGrid, YPad, Bricks): # get the state in index representation for the QA as in the constructor
        [XB, YB] = Tabular.get_ball_pos(ball, HGrid, YPad)
        VBX = ball.vx +2 # +2 because the lowest speed should be 1 for the table, so that entry 0 corresponds to speed -2
        VBY = 0 if ball.vy <0 else 1 # note this returns an array index not the actual speed
        XP =  Tabular.get_paddle_pos(paddle, HGrid) # paddle position
        VP = paddle.speed +2# paddle speed
        BRICKS = Tabular.get_brick_existence(Bricks)

        state = np.array([XB-1, YB-1, VBX, VBY, XP-1, VP, BRICKS]) # -1 because indices have to start at 0

        return state
    
    @staticmethod
    def set_state(XB, YB, VBX, VBY, XP, VP, BRICKS, YPad,HGrid, ball, paddle, Bricks): # this allows to inizialize the state of the system in the format of the output of the get_state function
        XB = XB +1 # recall that the smallest actual position is 1, and not 0 as the state inidices that is given to the function
        YB = YB +1
        XP = XP +1
        ShiftX = math.ceil(HGrid/2)
        ShiftY = 1# note that usually the smallest y values is ypad, if I ad -ypad to all first, it is 1,,
        ball.setx((XB-ShiftX)*50) # this is a straight forward inversion of the formula in the get_ball_pos function
        ball.sety((YB-ShiftY)*50+YPad)
        ball.vx = VBX-2
        ball.vy = -1 if VBY == 0 else 1
        paddle.setx((XP-ShiftX+2)*50)
        paddle.speed = VP-2

        # next I want to set which brick is visible and which is not, this is slightly more complicated, based on the inversion of the brick_existence function
        # first I convert the BRICKS index back to its binary form
        N = len(Bricks.brick_array)
        output = np.zeros(N, dtype=np.int32) 
        for i in range(0, N):
            if BRICKS >= 2 ** (N - i - 1):
                BRICKS = BRICKS - 2 ** (N - i - 1)
                output[i] = 1
            else:
                output[i] = 0

        # next I use the binary form output to set which bricks are active and which are not
        i=0
        for brick in Bricks.brick_array:
            if output[i] == 1: # this means brick should be visible
                brick.showturtle()
            else:
                brick.hideturtle() # check if brick is still in the game
            i = i+1 

    @staticmethod
    def randome_state(HGrid, VGrid, Bricks): # create a random state of the game
        N = len(Bricks.brick_array)
        XB = random.randint(0, HGrid-1) # random position of ball
        YB = random.randint(0, VGrid-1)
        VBX = random.randint(0, 4)
        VBY = random.randint(0, 1)
        XP = random.randint(0, HGrid-5)
        VP = random.randint(0, 4)
        BRICKS =random.randint(0, 2**N-1)

        return XB, YB, VBX, VBY, XP, VP, BRICKS

    def Egreedy_move(self, ball, paddle, HGrid, YPad, Bricks, E, debug=False): # take an epsilon greedy action, E is the probability of a random action
        # first I need to retreive the state of the game
        state = self.get_state(ball, paddle, HGrid, YPad, Bricks)
        Left = np.append(state, 0).astype(int) # possible actions Left, Right or no paddle movement change
        Right = np.append(state, 1).astype(int)
        Zero = np.append(state, 2).astype(int)

        LeftQ = self.QA[tuple(Left)]
        RightQ = self.QA[tuple(Right)]
        ZeroQ = self.QA[tuple(Zero)]     

        max_value = np.max(np.array([LeftQ, RightQ, ZeroQ]))
        max_indices = np.where(np.array([LeftQ,RightQ,ZeroQ]) == max_value)[0]
        random_index = random.choice(max_indices)

        # if debug:
        #     print("For state {} we have action values {}|{}|{}. Choosing {}!".format(state, LeftQ, RightQ, ZeroQ, random_index))

        # with E probability, we choose a random action among ALL action (including the one that we would've picked anyways)
        if random.random() < E: # random move with probability E
            return random.randint(0, 2), state
        else:
            return random_index, state
        
    def single_timestep(self,  HGrid, VGrid, YPad, paddle, ball, Bricks, E, debug=False): # this function computes a single step of an episode
        #the first check which move to do with the paddle
        Move, state = self.Egreedy_move(ball, paddle, HGrid, YPad, Bricks, E, debug=debug)

        if Move == 0:
            paddle.move_left()
        elif Move == 1:
            paddle.move_right()

        reset = ball.update(paddle, Bricks, HGrid, VGrid, YPad)
        paddle.update(HGrid)

        return Move, reset, state

    def OnP_Episode(self, strategy, episode_setting, HGrid, VGrid, YPad, paddle, ball, bricks, E, maximum_timesteps):
        ball.reset_game(paddle, bricks, YPad)
        SA = []  # these are the state-action pairs for this episode
        # We assume here we will win. So the initial reward is +250
        reward = 250
        timestep = 0
        while self.get_state(ball, paddle, HGrid, YPad, bricks)[-1] != 0:
            if episode_setting == EPISODE_SETTING_CAPPED and timestep > maximum_timesteps:
                # We ran into the timestep limit. So we subtract 250 from the reward again because the beginning assumption was violated
                reward -= 250
                break
            move, reset, previous_state = self.single_timestep(HGrid, VGrid, YPad, paddle, ball, bricks, E, debug=timestep < 3)
            state_action = previous_state.tolist()
            state_action.append(move)
            state_action = tuple(int(x) for x in state_action)
            SA.append(state_action)
            if reset and episode_setting == EPISODE_SETTING_GAME:
                # We lost. So we subtract 250 from the reward again because the beginning assumption was violated
                reward -= 250
                break
            timestep += 1

        reversed_SA = SA[::-1]  # lastly I update the QA table
        for i in range(len(reversed_SA)):
            reward -= 1
            current_sa = reversed_SA[i]
            if strategy == STRATEGY_ON_POLICY_E_SOFT_EVERY_VISIT or current_sa not in reversed_SA[(i + 1):]:
                Sum = self.AReturns[current_sa] * self.COUNTER[current_sa]
                Sum += reward
                self.COUNTER[current_sa] += 1  # state has occured one more time
                self.AReturns[current_sa] = Sum / self.COUNTER[current_sa]  # new average Return
                self.QA[current_sa] = self.AReturns[current_sa]  # new average Return

        return reward

    def ES_Episode(self, HGrid, VGrid, YPad, paddle, ball, Bricks, E, MAX): #play a full episode and update QA in the end
        
        # first I initialize a random start in the middle of the episode, as is typical for an exploring start training mechanism
        XB, YB, VBX, VBY, XP, VP, BRICKS = Tabular.randome_state(HGrid, VGrid, Bricks)
        self.set_state(XB, YB, VBX, VBY, XP, VP, BRICKS, YPad,HGrid, ball, paddle, Bricks)
        # next I initialize a random action 
        Action = random.randint(0, 2)  
        if Action == 0:
            paddle.move_left()
        elif Action == 1:
            paddle.move_right()

        SA = [] # these are the state-action pairs for this episode

        state_action = self.get_state(ball, paddle, HGrid, YPad, Bricks).tolist() 
        state_action.append(Action)
        state_action = tuple(int(x) for x in state_action)
        SA.append(state_action)
        ball.update(paddle, Bricks, HGrid, VGrid, YPad)
        paddle.update(HGrid)

        timestep = 0
        while self.get_state(ball, paddle, HGrid, YPad, Bricks)[-1] != 0 and timestep<MAX:
            move, reset, previous_state = self.single_timestep(HGrid, VGrid, YPad, paddle, ball, Bricks, E)
            state_action = previous_state.tolist()
            state_action.append(move)
            state_action = tuple(int(x) for x in state_action)
            SA.append(state_action)
            timestep += 1

        reversed_SA = SA[::-1] # lastly I update the QA table
        Return = 0
        i=0
        for x in reversed_SA:
            Return += -1
            # I apply first visit MC
            dummy = reversed_SA[(i+1):]
            i = i+1
            if x not in dummy:
                Sum = self.AReturns[x]*self.COUNTER[x]
                Sum += Return
                self.COUNTER[x] += 1 # state has occured one more time
                self.AReturns[x] = Sum/self.COUNTER[x] # new average Return
                self.QA[x] = self.AReturns[x] # new average Return

        return Return
    # train for Episodes numeber of episodes, print average return for every average number of episodes
    def Train(self, strategy, episode_setting, Episodes, average, HGrid, VGrid, YPad, paddle, ball, Bricks, E, MAX):
        Episode = []
        Returns = []
        ReturnFifty = 0
        for i in range(0, Episodes):
            if strategy == STRATEGY_EXPLORING_STARTS_FIRST_VISIT and episode_setting == EPISODE_SETTING_CAPPED:
                ReturnFifty += self.ES_Episode(HGrid, VGrid, YPad, paddle, ball, Bricks, E, MAX)
            else:
                ReturnFifty += self.OnP_Episode(strategy, episode_setting, HGrid, VGrid, YPad, paddle, ball, Bricks, E, MAX)
            if i % average == 0 and not i == 0:
                print(i)
                print(ReturnFifty/average)
                Episode.append(i)
                Returns.append(ReturnFifty/average)
                ReturnFifty = 0
        return Episode, Returns
