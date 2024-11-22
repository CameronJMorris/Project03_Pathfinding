import time

import pygame
import random
from enum import Enum
from collections import namedtuple
from A_Star import get_directions, a_star_search
import numpy as np
import pprint

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20000


class SnakeGame:

    def __init__(self, w=240, h=320):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self.board = self.set_board()
        self._place_food()

    def set_board(self):
        board = [[1 for _ in range(int(self.h/BLOCK_SIZE))] for _ in range(int(self.w/BLOCK_SIZE))]
        board[int(self.w/2/BLOCK_SIZE)][int(self.h/2/BLOCK_SIZE)] = 0
        board[int((self.w/2/BLOCK_SIZE)-1)][int(self.h/2/BLOCK_SIZE)] = 0
        board[int((self.w/2/BLOCK_SIZE)-2)][int(self.h/2/BLOCK_SIZE)] = 0
        return board

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def get_board(self):
        board = self.board
        x = 0
        y = 0
        x1 = 0
        y1 = 0
        for p in self.snake:
            x = int(p.x/BLOCK_SIZE)
            y = int(p.y/BLOCK_SIZE)
            board[x][y] = 0
            if x1 == 0 and y1 == 0:
                x1 = p.x/BLOCK_SIZE
                y1 = p.y/BLOCK_SIZE
        return board

    def get_simple_direction(self, tup):
        if tup[0] == 1 and tup[1] == 0:
            return Direction.RIGHT
        if tup[0] == 0 and tup[1] == 1:
            return Direction.DOWN
        if tup[0] == -1 and tup[1] == 0:
            return Direction.LEFT
        if tup[0] == 0 and tup[1] == -1:
            return Direction.UP
        else:
            print("Umm...")
            return None

    def to_blocks(self, thing):
        th = ()
        for t in thing:
            th = th+(int(t/BLOCK_SIZE),)
        return th

    def play_step(self, i=0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        board = self.get_board()
        directions = get_directions(a_star_search(board, self.to_blocks(self.head), self.to_blocks(self.food)))
        if len(directions) >= 1:
            if self.get_simple_direction(directions[0]) is not None:
                self.direction = self.get_simple_direction(directions[0])
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.board[self.to_blocks(self.snake[-1])[0]][self.to_blocks(self.snake[-1])[1]]=1
            self.snake.pop()
        self.board[self.to_blocks(self.head)[0]][self.to_blocks(self.head)[1]]=0
        self._update_ui()
        self.clock.tick(SPEED)
        time.sleep(i)
        return game_over, self.score

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

def run_game(i):
    game = SnakeGame(400, 400)
    score = 0
    board = np.array(game.get_board())
    running = True
    while running:
        game_over, score = game.play_step(i)
        if game_over == True:
            break
    while True:
        break
    return score

if __name__ == '__main__':
    j = 0
    max = 0
    tim = 0
    tim = int(input("Enter how long you would like for each action to tak in milliseconds: "))/1000.0
    for i in range(1000):
        num = run_game(tim)
        print(i, num)
        j += num
        if num > max:
            max = num
    print(j/1000)
    print(max)