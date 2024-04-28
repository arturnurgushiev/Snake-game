from random import randint
from random import randrange
import pygame
import time
from sys import exit

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
purple = pygame.Color(160, 32, 255)
gray = pygame.Color(140, 140, 140)

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


class Leaderboard:
    def __init__(self):
        pass

    def load_scores(self):
        file = open("leaderboard.txt", "r")
        pb = list(map(int, file.readline().split()))
        file.close()
        return pb

    def update_scores(self, score):
        pb = self.load_scores()
        file = open("leaderboard.txt", "w")
        pb.append(score)
        pb.sort(reverse=True)
        pb.pop()
        line = ""
        for i in pb:
            line += str(i) + ' '
        file.write(line)
        file.close()

    def display_scores(self):
        screen.fill(black)
        pb = self.load_scores()
        my_font = pygame.font.SysFont('times new roman', 50)
        pb_surface = my_font.render('Your Records:', True, red)
        pb_first = my_font.render(str(pb[0]), True, red)
        pb_second = my_font.render(str(pb[1]), True, red)
        pb_third = my_font.render(str(pb[2]), True, red)
        pb_fourth = my_font.render(str(pb[3]), True, red)
        pb_fifth = my_font.render(str(pb[4]), True, red)
        pb_rect = pb_surface.get_rect()
        pb_first_rect = pb_first.get_rect()
        pb_second_rect = pb_second.get_rect()
        pb_third_rect = pb_third.get_rect()
        pb_fourth_rect = pb_fourth.get_rect()
        pb_fifth_rect = pb_fifth.get_rect()
        pb_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 8)
        pb_first_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 8 + 80)
        pb_second_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 8 + 160)
        pb_third_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 8 + 240)
        pb_fourth_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 8 + 320)
        pb_fifth_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 8 + 400)
        screen.blit(pb_surface, pb_rect)
        screen.blit(pb_first, pb_first_rect)
        screen.blit(pb_second, pb_second_rect)
        screen.blit(pb_third, pb_third_rect)
        screen.blit(pb_fourth, pb_fourth_rect)
        screen.blit(pb_fifth, pb_fifth_rect)
        pygame.display.flip()


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
            # self.generate_position()


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


class Game:
    def __init__(self):
        self.wall = []
        self.leaderboard = Leaderboard()
        self.snake = Snake([[140, 140]], (0, 10))
        self.food = Food()
        self.food.generate_position(self.wall)
        self.bonus = Bonus()
        self.vector = {pygame.K_UP: (0, -10), pygame.K_DOWN: (0, 10), pygame.K_LEFT: (-10, 0), pygame.K_RIGHT: (10, 0)}

    def show_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(len(self.snake.body) * 10 - 10), True, color)
        score_rect = score_surface.get_rect()
        screen.blit(score_surface, score_rect)

    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 50)
        score = len(self.snake.body) * 10 - 10
        self.leaderboard.update_scores(score)
        game_over_surface = my_font.render(
            'Your Score is : ' + str(score), True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
        screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(3)
        self.leaderboard.display_scores()
        time.sleep(2)
        pygame.quit()
        quit()

    def run(self):
        pygame.init()
        begin_flag = False
        while True:
            my_font = pygame.font.SysFont('times new roman', 50)
            choose_surface = my_font.render(
                'Choose level', True, red)
            choose_rect = choose_surface.get_rect()
            choose_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
            help_surface = my_font.render(
                'Press button from 1 to 5', True, red)
            help_rect = choose_surface.get_rect()
            help_rect.midtop = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 4 + 300)
            screen.blit(choose_surface, choose_rect)
            screen.blit(help_surface, help_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        begin_flag = True
                        break
                    elif event.key == pygame.K_2:
                        begin_flag = True

                        for i in range(3, 6):
                            new_wall = []
                            for j in range(100, 710, 10):
                                new_wall.append([j, i * 100])
                            self.wall.append(new_wall)
                        break

                    elif event.key == pygame.K_3:
                        begin_flag = True

                        first_wall = []
                        for j in range(0, 810, 10):
                            first_wall.append([j, 0])
                            self.wall.append(first_wall)
                        second_wall = []
                        for j in range(0, 810, 10):
                            second_wall.append([j, 790])
                            self.wall.append(second_wall)
                        third_wall = []
                        for j in range(0, 810, 10):
                            third_wall.append([0, j])
                            self.wall.append(third_wall)
                        fourth_wall = []
                        for j in range(0, 810, 10):
                            fourth_wall.append([790, j])
                            self.wall.append(fourth_wall)
                        break
                    elif event.key == pygame.K_4:
                        for i in range(10, WINDOW_WIDTH, 100):
                            for j in range(10, WINDOW_HEIGHT, 100):
                                self.wall.append([[i, j]])
                        begin_flag = True
                        break
                    elif event.key == pygame.K_5:
                        first_wall = []
                        for i in range(100, WINDOW_WIDTH - 100, 10):
                            first_wall.append([i, WINDOW_HEIGHT / 2])
                        second_wall = []
                        for i in range(100, WINDOW_HEIGHT - 100, 10):
                            second_wall.append([WINDOW_WIDTH / 2, i])
                        self.wall.append(first_wall)
                        self.wall.append(second_wall)
                        begin_flag = True
                        break
            clock.tick(self.snake.speed)
            if begin_flag:
                break

        self.food.generate_position(self.wall)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    self.snake.direction = self.vector[event.key]
            flag = self.snake.move(self.food, self.bonus, self.wall)
            if not flag:
                self.game_over()
            screen.fill(black)
            for pos in game.snake.body:
                pygame.draw.rect(screen, green,
                                 pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(screen, white, pygame.Rect(
                self.food.position[0], self.food.position[1], 10, 10))
            for wall in self.wall:
                for pos in wall:
                    pygame.draw.rect(screen, gray,
                                     pygame.Rect(pos[0], pos[1], 10, 10))
            self.bonus.run(self.wall)
            if self.bonus.flag:
                pygame.draw.rect(screen, self.bonus.vector[self.bonus.type], pygame.Rect(
                    self.bonus.position[0], self.bonus.position[1], 10, 10))
            self.show_score(white, 'times new roman', 20)
            pygame.display.update()
            clock.tick(self.snake.speed)
            self.snake.speed += 0.0001


game = Game()
game.run()
