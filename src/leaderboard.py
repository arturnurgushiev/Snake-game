import os

from src.constants import *


class Leaderboard:
    def __init__(self):
        pass

    @staticmethod
    def load_scores():
        file = open(os.path.join("src", "leaderboard.txt"), "r")
        pb = list(map(int, file.readline().split()))
        file.close()
        return pb

    def update_scores(self, score):
        pb = self.load_scores()
        file = open(os.path.join("src", "leaderboard.txt"), "w")
        pb.append(score)
        pb.sort(reverse=True)
        pb.pop()
        line = ""
        for i in pb:
            line += f"{i} "
        file.write(line)
        file.close()

    def display_scores(self, screen):
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
