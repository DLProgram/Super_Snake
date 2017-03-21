import pygame

from classes import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

S_SIZE = 15
MARGIN = 2

WIDTH = S_SIZE * 27
HEIGHT = S_SIZE * 27 + 250


def generate_images():
    ck = (127, 33, 33)
    T0X = pygame.Surface((S_SIZE, S_SIZE))
    T0O = pygame.Surface((S_SIZE, S_SIZE))
    T1X = pygame.Surface((S_SIZE * 3, S_SIZE * 3))
    T1O = pygame.Surface((S_SIZE * 3, S_SIZE * 3))
    T2X = pygame.Surface((S_SIZE * 9, S_SIZE * 9))
    T2O = pygame.Surface((S_SIZE * 9, S_SIZE * 9))
    images = {"X": [T0X, T1X, T2X], "O": [T0O, T1O, T2O]}
    for i in range(3):
        x_surface = images["X"][i]
        o_surface = images["O"][i]
        size = x_surface.get_width()
        center = int(size / 2)
        width = int(size / 3)

        x_surface.fill(ck)
        x_surface.set_colorkey(ck)
        o_surface.fill(ck)
        o_surface.set_colorkey(ck)

        pygame.draw.line(x_surface, BLACK, (0, 0), (size, size), width)
        pygame.draw.line(x_surface, BLACK, (0, size), (size, 0), width)

        pygame.draw.circle(o_surface, BLACK, (center, center), center)
        pygame.draw.circle(o_surface, ck, (center, center), center - width)

    return images


def draw_board(surface, board, images, x_offset=0, y_offset=0):
    for cord in range(28):
        if cord % 9 == 0:
            pygame.draw.rect(surface, (0, 0, 0), (0 + x_offset, cord * S_SIZE + y_offset, WIDTH, 1))
            pygame.draw.rect(surface, (0, 0, 0), (cord * S_SIZE + x_offset, 0 + y_offset, 1, WIDTH))
        elif cord % 3 == 0:
            pygame.draw.rect(surface, (80, 80, 80), (0 + x_offset, cord * S_SIZE + y_offset, WIDTH, 1))
            pygame.draw.rect(surface, (80, 80, 80), (cord * S_SIZE + x_offset, 0 + y_offset, 1, WIDTH))
        else:
            pygame.draw.rect(surface, (150, 150, 150), (0 + x_offset, cord * S_SIZE + y_offset, WIDTH, 1))
            pygame.draw.rect(surface, (150, 150, 150), (cord * S_SIZE + x_offset, 0 + y_offset, 1, WIDTH))

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

            if t2.get_winner():
                if t2.get_winner() == 1:
                    surface.blit(images["O"][2], (x // 9 * S_SIZE * 9 + x_offset, y // 9 * S_SIZE * 9 + y_offset))
                else:
                    surface.blit(images["X"][2], (x // 9 * S_SIZE * 9 + x_offset, y // 9 * S_SIZE * 9 + y_offset))
            elif t1.get_winner():
                if t1.get_winner() == 1:
                    surface.blit(images["O"][1], (x // 3 * S_SIZE * 3 + x_offset, y // 3 * S_SIZE * 3 + y_offset))
                elif t1.get_winner() == -1:
                    surface.blit(images["X"][1], (x // 3 * S_SIZE * 3 + x_offset, y // 3 * S_SIZE * 3 + y_offset))
            else:
                if t0.get_status() == 1:
                    surface.blit(images["O"][0], (x * S_SIZE + x_offset, y * S_SIZE + y_offset))
                elif t0.get_status() == -1:
                    surface.blit(images["X"][0], (x * S_SIZE + x_offset, y * S_SIZE + y_offset))


def main():
    board = T3()
    board.get_t2_at(0, 0).get_t1_at(0, 0).get_t0_at(0, 0).set_status(1)
    board.get_t2_at(0, 0).get_t1_at(0, 0).get_t0_at(1, 1).set_status(1)
    board.get_t2_at(0, 0).get_t1_at(0, 0).get_t0_at(2, 2).set_status(1)
    board.get_t2_at(0, 0).get_t1_at(1, 0).get_t0_at(2, 0).set_status(-1)
    board.get_t2_at(0, 0).get_t1_at(1, 0).get_t0_at(1, 1).set_status(-1)
    board.get_t2_at(0, 0).get_t1_at(1, 0).get_t0_at(0, 2).set_status(-1)
    board.get_t2_at(0, 0).get_t1_at(1, 1).set_winner(1)
    board.get_t2_at(0, 0).get_t1_at(2, 2).set_winner(1)

    board.get_t2_at(1, 1).set_winner(1)
    board.get_t2_at(2, 2).set_winner(1)

    pygame.init()
    surface = pygame.display.set_mode((WIDTH + 10, HEIGHT), 0, 32)
    pygame.display.set_caption('T^3')
    clock = pygame.time.Clock()
    images = generate_images()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        surface.fill(WHITE)

        draw_board(surface, board, images, 5, 245)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
