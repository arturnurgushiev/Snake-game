from random import randrange

from src.constants import *


class Food:
    def __init__(self):
        self.position = [0, 0]

    def check(self, wall):
        for one_wall in wall:
            for pos in one_wall:
                if self.position[0] == pos[0] and self.position[1] == pos[1]:
                    return False
        return True

    def generate_position(self, wall):
        self.position = [randrange(0, (WINDOW_WIDTH // 10)) * 10, randrange(1, (WINDOW_HEIGHT // 10)) * 10]
        while not self.check(wall):
            self.position = [randrange(0, (WINDOW_WIDTH // 10)) * 10, randrange(1, (WINDOW_HEIGHT // 10)) * 10]
