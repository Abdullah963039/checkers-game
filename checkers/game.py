import pygame

from minimax.algorithm import minimax


from .constants import AI_ENGINE_DEPTH, BLUE, HIEGHT, RED, SQUARE_SIZE, WHITE, WIDTH
from .board import Board

FPS = 60

pygame.init()


class Game:
    def __init__(self):
        self.__initialize_game()
        self.screen = pygame.display.set_mode((WIDTH, HIEGHT))
        pygame.display.set_caption("Checkers Game")
        self.__run_game = True

    def start_game(self):
        clock = pygame.time.Clock()
        clock.tick(FPS)

        if self.__winner():
            self.__end_game()

        while self.__run_game:
            clock.tick(FPS)

            if self.__turn == WHITE:
                value, new_board = minimax(
                    self.__board, AI_ENGINE_DEPTH, WHITE, self
                )
                self.__ai_move(new_board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__end_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.__get_row_col_from_mouse(pos)

                    self.__select(row, col)

            self.__update()

        pygame.quit()

    def __update(self):
        self.__board.draw(self.screen)
        self.__draw_valid_moves(self.__valid_moves)
        pygame.display.update()

    def __initialize_game(self):
        self.__selected = None
        self.__board = Board()
        self.__turn = RED
        self.__valid_moves = {}

    def __select(self, row, col):
        if self.__selected:
            result = self.__move(row, col)
            if not result:
                self.__selected = None
                self.__select(row, col)

        piece = self.__board.get_piece(row, col)
        if piece != 0 and piece.color == self.__turn:
            self.__selected = piece
            self.__valid_moves = self.__board.get_valid_moves(piece)
            return True

        return False

    def __move(self, row, col):
        piece = self.__board.get_piece(row, col)
        if self.__selected and piece == 0 and (row, col) in self.__valid_moves:
            self.__board.move(self.__selected, row, col)
            skipped = self.__valid_moves[(row, col)]

            if skipped:
                self.__board.remove(skipped)

            self.__change_turn()
        else:
            return False

        return True

    def __draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.screen,
                BLUE,
                (
                    col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    row * SQUARE_SIZE + SQUARE_SIZE // 2,
                ),
                15,
            )

    def __change_turn(self):
        self.__valid_moves = {}
        if self.__turn == RED:
            self.__turn = WHITE
        else:
            self.__turn = RED

    def __winner(self):
        return self.__board.winner()

    def __ai_move(self, board):
        self.__board = board
        self.__change_turn()

    def __get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE

        return row, col

    def __end_game(self):
        self.run_game = False
        pygame.quit()
