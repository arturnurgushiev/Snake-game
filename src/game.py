from sys import exit

import time

from src.bonus import Bonus
from src.constants import *
from src.food import Food
from src.leaderboard import Leaderboard
from src.snake import Snake


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
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
        self.screen.blit(score_surface, score_rect)

    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 50)
        score = len(self.snake.body) * 10 - 10
        self.leaderboard.update_scores(score)
        game_over_surface = my_font.render(
            'Your Score is : ' + str(score), True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(3)
        self.leaderboard.display_scores(self.screen)
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
            self.screen.blit(choose_surface, choose_rect)
            self.screen.blit(help_surface, help_rect)
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
            self.clock.tick(self.snake.speed)
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
            self.screen.fill(black)
            for pos in self.snake.body:
                pygame.draw.rect(self.screen, green,
                                 pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(self.screen, white, pygame.Rect(
                self.food.position[0], self.food.position[1], 10, 10))
            for wall in self.wall:
                for pos in wall:
                    pygame.draw.rect(self.screen, gray,
                                     pygame.Rect(pos[0], pos[1], 10, 10))
            self.bonus.run(self.wall)
            if self.bonus.flag:
                pygame.draw.rect(self.screen, self.bonus.vector[self.bonus.type], pygame.Rect(
                    self.bonus.position[0], self.bonus.position[1], 10, 10))
            self.show_score(white, 'times new roman', 20)
            pygame.display.update()
            self.clock.tick(self.snake.speed)
            self.snake.speed += 0.0001
