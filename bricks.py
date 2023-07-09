from brick import Brick

# Collection class for all bricks in the game instance

class Bricks:
    def __init__(self, coordinates, ypad):
        self.brick_array = []
        for c in coordinates:
            self.brick_array.append(Brick(c[0], c[1], ypad))

    def all_bricks_disappeared(self):
        # Returns true if all bricks have been hit in the game and are not visible anymore
        for brick in self.brick_array:
            if brick.isvisible():
                return False
        return True

    def reset(self):
        # Sets all bricks to visible again for restarting the game
        for brick in self.brick_array:
            brick.showturtle()

    def check_for_collisions(self, ball):
        # Checks if a brick was hit by the ball and if so, hides it / removes it from the game
        brick_hit = self.get_hit_brick(ball)
        if brick_hit:
            brick_hit.hideturtle()

    def get_hit_brick(self, ball):
        # Returns the brick that was hit by the ball, or None if no brick was hit. This function works with prioritization among hits.
        # Highest prio hits are returned directly, lower prio hits can be overwritten as the code lines out below
        brick_hit = None
        orig_vy = ball.vy
        orig_vx = ball.vx
        # Loop that iterates through all bricks that are in direct y-proximity of the ball
        for brick in self.brick_array:
            if not brick.isvisible():
                continue
            # Skips all bricks whose x-projection wouldn't be hit by the ball in the next iteration
            if abs(ball.ycor() + (50 * orig_vy) - brick.ycor()) >= 35 or abs(ball.ycor() - brick.ycor()) < 35:
                continue
            # Checking for highest prio case: frontal hit by the ball via y-direction
            if abs(ball.xcor() - brick.xcor()) < 85:
                ball.vy = -orig_vy
                ball.vx = orig_vx
                return brick
            # Checking for low prio hit: edge hit by the ball via x- and y-direction
            if abs(orig_vx) >= 1 and abs(ball.xcor() + (50 if orig_vx > 0 else -50) - brick.xcor()) < 85:
                ball.vy = -orig_vy
                ball.vx = -orig_vx
                brick_hit = brick
            # Checking for lowest prio hit: sort-of edge hit by the ball via x- and y-direction with x-speed=2. This ensures ball cannot skip a closer hit for a more distant hit
            if abs(orig_vx) == 2 and abs(ball.xcor() + (50 * orig_vx) - brick.xcor()) < 85:
                if not brick_hit:
                    ball.vx = -orig_vx
                    ball.vy = orig_vy
                    brick_hit = brick

        # If ball does not move in x-direction, then we are done here
        if orig_vx == 0:
            return brick_hit

        # Loop that iterates through all bricks that are in direct x-proximity of the ball
        for brick in self.brick_array:
            if not brick.isvisible():
                continue
            # Skips all bricks whose y-projection wouldn't be hit by the ball in the next iteration
            if abs(ball.xcor() + (50 if orig_vx>0 else -50) - brick.xcor()) >= 85 or abs(ball.xcor() - brick.xcor()) < 85:
                continue
            # Checking for highest prio case: frontal hit by the ball via x-direction
            if abs(ball.ycor() - brick.ycor()) < 35 and abs(ball.xcor() + (50 if orig_vx>0 else -50) - brick.xcor()) < 85:
                ball.vx = -orig_vx
                ball.vy = orig_vy
                return brick

        return brick_hit


    # def is_corner(self, xcoord, ycoord, ballvx, ballvy):
    #     for i in range(len(self.brick_array)):
    #         brick = self.brick_array[i]
    #         if not (abs(brick.xcor() - xcoord) < 85 and abs(ycoord - brick.ycor())<35):
    #             continue
    #         if ballvx > 0:
    #             if abs(xcoord - brick.xcor() - 50) < 35 and ballvy > 0:
    #                 for j in range(len(self.brick_array)):
    #                     otherbrick = self.brick_array[j]
    #                     if otherbrick.ycor()
    #             elif abs(xcoord - brick.xcor() - 50) < 35 and ballvy < 0:
    #                 for j in range(len(self.brick_array)):
    #                     otherbrick = self.brick_array[j]
    #     return False

#import numpy as np

#HGrid = 13
#VGrid = 9
#YPAD = -275
#Coordinates = [[-3, 7], [0, 7], [3, 7]]
#N = 3

#A = np.zeros((HGrid, VGrid, 5, 2, HGrid-5, 5, 2**N, 3), dtype=np.int32)
#print(A.shape)

#B = np.array([1, 1, 1, 1, 0, 1, 1, 1])

#print(A[1, 1, 1, 1, 1, 1, 1, 1])
#print(A[1, 1, 1, 1, 0, 1, 1, 1])

# Create an open mesh grid of indices using np.ix_()
#indexer = (1, 1, 1, 1, 0, 1, 1)

# Use tuple unpacking to index the array A
#print(A[indexer,1])











