from src.constants import *


class Snake:
    def __init__(self, body, direction):
        self.grow = 0
        self.body = body
        self.direction = direction
        self.speed = 15.0
        self.wall = []

    def move(self, food, bonus, wall):
        x, y = self.body[0]
        x += self.direction[0]
        y += self.direction[1]
        x %= WINDOW_WIDTH
        y %= WINDOW_HEIGHT
        for one_wall in wall:
            for pos in one_wall:
                if x == pos[0] and y == pos[1]:
                    return False
        if x == bonus.position[0] and y == bonus.position[1]:
            bonus.flag = False
            if bonus.type == 0:
                self.speed += 5.0
            elif bonus.type == 1:
                self.grow = 5
            elif bonus.type == 2:
                if len(self.body) > 5:
                    for _ in range(5):
                        self.body.pop()
                else:
                    self.body = [self.body[0]]
        if x == food.position[0] and y == food.position[1]:
            food.generate_position(wall)
        elif [x, y] in self.body:
            return False
        else:
            if self.grow == 0:
                self.body.pop()
            else:
                self.grow -= 1
        self.body.insert(0, [x, y])
        return True
