from brick import Brick

class Bricks:
    def __init__(self, coordinates, ypad):
        self.brick_array = []
        for c in coordinates:
            self.brick_array.append(Brick(c[0], c[1], ypad))

    def all_bricks_disappeared(self):
        for brick in self.brick_array:
            if brick.isvisible():
                return False
        return True

    def reset(self):
        for brick in self.brick_array:
            brick.showturtle()

    def check_for_collisions(self, ball):
        brick_hit = self.get_hit_brick(ball)
        if brick_hit:
            brick_hit.hideturtle()

    def get_hit_brick(self, ball):
        brick_hit = None
        orig_vy = ball.vy
        orig_vx = ball.vx
        for brick in self.brick_array:
            if not brick.isvisible():
                continue
            if abs(ball.ycor() + (50 * orig_vy) - brick.ycor()) >= 35 or abs(ball.ycor() - brick.ycor()) < 35:
                continue
            if abs(ball.xcor() - brick.xcor()) < 85:
                ball.vy = -orig_vy
                ball.vx = orig_vx
                return brick
            if abs(orig_vx) >= 1 and abs(ball.xcor() + (50 if orig_vx > 0 else -50) - brick.xcor()) < 85:
                ball.vy = -orig_vy
                ball.vx = -orig_vx
                brick_hit = brick
            if abs(orig_vx) == 2 and abs(ball.xcor() + (50 * orig_vx) - brick.xcor()) < 85:
                if not brick_hit:
                    ball.vx = -orig_vx
                    ball.vy = orig_vy
                    brick_hit = brick

        if orig_vx == 0:
            return brick_hit

        for brick in self.brick_array:
            if not brick.isvisible():
                continue
            if abs(ball.xcor() + (50 if orig_vx>0 else -50) - brick.xcor()) >= 85 or abs(ball.xcor() - brick.xcor()) < 85:
                continue
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
