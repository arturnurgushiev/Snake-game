from random import randint
from random import randrange

from src.constants import *


class Bonus:
    def __init__(self):
        self.vector = [red, blue, purple]
        self.type = 0
        self.position = [0, 0]
        self.flag = False
        self.time = 0

    def check(self, wall):
        for one_wall in wall:
            for pos in one_wall:
                if self.position[0] == pos[0] and self.position[1] == pos[1]:
                    return False
        return True

    def generate_position(self):
        self.position = [randrange(0, (WINDOW_WIDTH // 10)) * 10, randrange(0, (WINDOW_HEIGHT // 10)) * 10]

    def run(self, wall):
        if self.flag:
            if self.time == 0:
                self.flag = False
                return
            self.time -= 1
            return
        self.flag = randint(0, 1000) < 10
        if self.flag:
            self.type = randint(0, 2)
            self.time = 150
            self.generate_position()
            while not self.check(wall):
                self.generate_position()
