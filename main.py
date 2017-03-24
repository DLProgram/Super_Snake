import pygame
import sys
from classes import *
from random import randint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

S_SIZE = 15
MARGIN = 2

INPUT_HEIGHT = 150
WIDTH = S_SIZE * 27
HEIGHT = S_SIZE * 27 + INPUT_HEIGHT

X_OFFSET = 5
Y_OFFSET = INPUT_HEIGHT - X_OFFSET


def generate_images():
    ck = (127, 33, 33)
    images = {"X": [pygame.Surface((S_SIZE, S_SIZE)),
                    pygame.Surface((S_SIZE * 3, S_SIZE * 3)),
                    pygame.Surface((S_SIZE * 9, S_SIZE * 9))],
              "O": [pygame.Surface((S_SIZE, S_SIZE)),
                    pygame.Surface((S_SIZE * 3, S_SIZE * 3)),
                    pygame.Surface((S_SIZE * 9, S_SIZE * 9))]}
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

        pygame.draw.line(x_surface, RED, (0, 0), (size, size), width)
        pygame.draw.line(x_surface, RED, (0, size), (size, 0), width)

        pygame.draw.circle(o_surface, BLUE, (center, center), center)
        pygame.draw.circle(o_surface, ck, (center, center), center - width)

    return images


def draw_board(surface, board, images):
    for cord in range(28):
        if cord % 9 == 0:
            pygame.draw.rect(surface, (0, 0, 0), (0 + X_OFFSET, cord * S_SIZE + Y_OFFSET, WIDTH, 1))
            pygame.draw.rect(surface, (0, 0, 0), (cord * S_SIZE + X_OFFSET, 0 + Y_OFFSET, 1, WIDTH))
        elif cord % 3 == 0:
            pygame.draw.rect(surface, (80, 80, 80), (0 + X_OFFSET, cord * S_SIZE + Y_OFFSET, WIDTH, 1))
            pygame.draw.rect(surface, (80, 80, 80), (cord * S_SIZE + X_OFFSET, 0 + Y_OFFSET, 1, WIDTH))
        else:
            pygame.draw.rect(surface, (150, 150, 150), (0 + X_OFFSET, cord * S_SIZE + Y_OFFSET, WIDTH, 1))
            pygame.draw.rect(surface, (150, 150, 150), (cord * S_SIZE + X_OFFSET, 0 + Y_OFFSET, 1, WIDTH))

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
                    surface.blit(images["O"][2], (x // 9 * S_SIZE * 9 + X_OFFSET, y // 9 * S_SIZE * 9 + Y_OFFSET))
                else:
                    surface.blit(images["X"][2], (x // 9 * S_SIZE * 9 + X_OFFSET, y // 9 * S_SIZE * 9 + Y_OFFSET))
            elif t1.get_winner():
                if t1.get_winner() == 1:
                    surface.blit(images["O"][1], (x // 3 * S_SIZE * 3 + X_OFFSET, y // 3 * S_SIZE * 3 + Y_OFFSET))
                elif t1.get_winner() == -1:
                    surface.blit(images["X"][1], (x // 3 * S_SIZE * 3 + X_OFFSET, y // 3 * S_SIZE * 3 + Y_OFFSET))
            else:
                if t0.get_status() == 1:
                    surface.blit(images["O"][0], (x * S_SIZE + X_OFFSET, y * S_SIZE + Y_OFFSET))
                elif t0.get_status() == -1:
                    surface.blit(images["X"][0], (x * S_SIZE + X_OFFSET, y * S_SIZE + Y_OFFSET))


def wait_for_click():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()


def draw_input(surface, t1, images, turn):
    cell_size = S_SIZE * 3
    input_surface = pygame.Surface((WIDTH, INPUT_HEIGHT - X_OFFSET))
    input_surface.fill(WHITE)
    rects = [[], [], []]
    for x in range(3):
        for y in range(3):
            t0 = t1.get_t0_at(x, y)
            rect = pygame.draw.rect(input_surface, BLACK,
                                    (X_OFFSET + cell_size * x, X_OFFSET + cell_size * y, cell_size, cell_size), 2)
            if t0.get_status() == 1:
                input_surface.blit(images["O"][1], rect)
            elif t0.get_status() == -1:
                input_surface.blit(images["X"][1], rect)

            rects[x].append(rect)

    if turn == 1:
        input_surface.blit(images["O"][2], (150, 5))
    else:
        input_surface.blit(images["X"][2], (150, 5))

    surface.blit(input_surface, (0, 0))
    return rects


def get_input_at_click(rects, pos):
    for x in range(3):
        for y in range(3):
            if rects[x][y].collidepoint(pos):
                return x, y
    return None


def check_t1(board, t2x, t2y, t1x, t1y):
    return not bool(board.get_t2_at(t2x, t2y).get_t1_at(t1x, t1y).get_winner())


def get_new_t1(board):
    while True:
        x = randint(0, 26)
        y = randint(0, 26)
        t1x = x // 3 % 3
        t1y = y // 3 % 3
        t2x = x // 9
        t2y = y // 9
        if check_t1(board, t2x, t2y, t1x, t1y):
            break
    return t2x, t2y, t1x, t1y


def get_next_t1(board, t2x, t2y, t1x, t1y, t0x, t0y):
    if check_t1(board, t0x, t0y, t0x, t0y):
        return t0x, t0x, t0x, t0y
    elif check_t1(board, t2x, t2y, t0x, t0y):
        return t2x, t2x, t0x, t0y
    else:
        return get_new_t1(board)



def main():
    board = T3()
    pygame.init()
    surface = pygame.display.set_mode((WIDTH + 10, HEIGHT), 0, 32)
    pygame.display.set_caption('T^3')
    images = generate_images()
    t2x, t2y, t1x, t1y = get_new_t1(board)
    turn = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        surface.fill(WHITE)

        draw_board(surface, board, images)

        rects = draw_input(surface, board.get_t2_at(t2x, t2y).get_t1_at(t1x, t1y), images, turn)
        pygame.display.update()
        t0x, t0y = get_input_at_click(rects, wait_for_click())
        t0 = board.get_t2_at(t2x, t2y).get_t1_at(t1x, t1y).get_t0_at(t0x, t0y)
        if not t0.get_status():
            t0.set_status(turn)
            t2x, t2y, t1x, t1y = get_next_t1(board, t2x, t2y, t1x, t1y, t0x, t0y)
            turn = -1 if turn == 1 else 1


if __name__ == '__main__':
    main()
