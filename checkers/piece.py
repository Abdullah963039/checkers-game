import pygame
from .constants import GRAY, SQUARE_SIZE, CROWN


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calc_position()

    def calc_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, window):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, GRAY, (self.x, self.y), radius)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius + self.OUTLINE)
        if self.king:
            window.blit(
                CROWN,
                (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2),
            )

    def __repr__(self):
        return str(self.color)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_position()
