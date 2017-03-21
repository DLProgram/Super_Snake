import pygame
from classes import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

S_SIZE = 15
MARGIN = 2

WIDTH = S_SIZE * 27 + MARGIN
HEIGHT = S_SIZE * 27 + MARGIN + 100


def draw_board(surface, board, x_offset=0, y_offset=0):
    for x in range(27):
        for y in range(27):
            t0x = x % 3
            t0y = y % 3
            t1x = x // 3 % 3
            t1y = y // 3 % 3
            t2x = x // 9
            t2y = y // 9

            t2 = board.get_t2_at(t2x, t2y)
            t1 = t2.get_t1_at(t1x, t1y)
            t0 = t1.get_t0_at(t0x, t0y)

            color = RED if t0.get_status() == -1 else (GREEN if t0.get_status() == 1 else WHITE)
            background = RED if t1.get_winner() == -1 else (GREEN if t1.get_winner() == 1 else BLUE)

            # if status == -1:
            #     color = RED
            # elif status == 1:
            #     color = GREEN
            # else:
            #     color = BLUE
            pygame.draw.rect(surface, background,
                             (x * S_SIZE + x_offset, y * S_SIZE + y_offset, S_SIZE, S_SIZE))
            pygame.draw.rect(surface, color,
                             (x * S_SIZE + MARGIN + x_offset, y * S_SIZE + MARGIN + y_offset, S_SIZE - MARGIN * 2,
                              S_SIZE - MARGIN * 2))


def main():
    board = T3()
    board.get_t2_at(0, 0).get_t1_at(0, 0).get_t0_at(0, 0).set_status(1)
    board.get_t2_at(0, 0).get_t1_at(0, 0).get_t0_at(1, 1).set_status(1)
    board.get_t2_at(0, 0).get_t1_at(0, 0).get_t0_at(2, 2).set_status(1)
    board.get_t2_at(0, 0).get_t1_at(1, 0).get_t0_at(2, 0).set_status(-1)
    board.get_t2_at(0, 0).get_t1_at(1, 0).get_t0_at(1, 1).set_status(-1)
    board.get_t2_at(0, 0).get_t1_at(1, 0).get_t0_at(0, 2).set_status(-1)

    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('T^3')
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        surface.fill(WHITE)

        draw_board(surface, board, 0, 0)

        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
