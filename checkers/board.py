import pygame

from .piece import Piece
from .constants import BLACK, COLS, ROWS, RED, SQUARE_SIZE, WHITE


class Board:
    def __init__(self):
        self.borad = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.__create_board()

    def draw_squares(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(
                    window,
                    RED,
                    (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )

    def __create_board(self):
        for row in range(ROWS):
            self.borad.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.borad[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.borad[row].append(Piece(row, col, RED))
                    else:
                        self.borad[row].append(0)
                else:
                    self.borad[row].append(0)

    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.borad[row][col]
                if piece != 0:
                    piece.draw(window)

    def get_piece(self, row, col):
        return self.borad[row][col]

    def evaluate(self):
        return (
            self.white_left
            - self.red_left
            + (self.white_kings * 0.5 - self.red_kings * 0.5)
        )

    def get_all_pieces(self, color):
        pieces = []
        for row in self.borad:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.borad[piece.row][piece.col], self.borad[row][col] = (
            self.borad[row][col],
            self.borad[piece.row][piece.col],
        )
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(
                self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left)
            )
            moves.update(
                self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right)
            )

        if piece.color == WHITE or piece.king:
            moves.update(
                self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left)
            )
            moves.update(
                self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right)
            )

        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.borad[piece.row][piece.col] = 0
        if piece != 0:
            if piece.color == RED:
                self.red_left -= 1
            else:
                self.white_left -= 1

    def winner(self):
        if self.red_left <= 0 or self.get_valid_player_moves(RED) == 0:
            return WHITE
        elif self.white_left <= 0 or self.get_valid_player_moves(WHITE) == 0:
            return RED
        else:
            return None

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.borad[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(
                        self._traverse_left(
                            r + step, row, step, color, left - 1, skipped=last
                        )
                    )
                    moves.update(
                        self._traverse_right(
                            r + step, row, step, color, left + 1, skipped=last
                        )
                    )
                break

            elif current.color == color:
                break

            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.borad[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(
                        self._traverse_left(
                            r + step, row, step, color, right - 1, skipped=last
                        )
                    )
                    moves.update(
                        self._traverse_right(
                            r + step, row, step, color, right + 1, skipped=last
                        )
                    )
                break

            elif current.color == color:
                break

            else:
                last = [current]

            right += 1

        return moves

    def get_valid_player_moves(self, color):
        total_valid_moves = 0

        for piece in self.get_all_pieces(color):
            if piece == 0:
                return 0
            valid_moves = self.get_valid_moves(piece)
            total_valid_moves += len(valid_moves)

        return total_valid_moves
