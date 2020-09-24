import numpy as np
import colors
import random

class FourInARow:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.board = np.zeros((rows, columns), dtype=int)
        self.human = 1
        self.ki = 2
        self.playerNames = ["None", "Human", "KI"]
        self.playerColors = [colors.WHITE, colors.RED, colors.YELLOW]
        self.currentPlayer = random.randint(1,2)
        self.lastPlayer = 2 if self.currentPlayer == 1 else 1
        self.game_piece_counter = 0
        self.turn_history = []

        self.animation_finished = True
        self.animation_offset_pos = 0

    def print_board(self):
        print(self.board)

    def check_game_over(self):
        if self.check_win_fast() or self.check_tie_fast():
            return True
        else:
            return False

    def check_tie(self):
        if not self.check_win_player(self.human) or not self.check_win_player(self.ki):
            if self.game_piece_counter == self.columns * self.rows:
                return True
        else:
            return False

    def check_tie_fast(self):
        if self.game_piece_counter == self.columns * self.rows:
            return True
        else:
            return False

    def check_win_player(self, player):
        for row in range(0, self.rows - 3, 1):
            for column in range(0, self.columns, 1):
                if self.board[row][column] == player and self.board[row + 1][column] == player and \
                        self.board[row + 2][column] == player and self.board[row + 3][column] == player:
                    return True

        for row in range(0, self.rows, 1):
            for column in range(0, self.columns - 3, 1):
                if self.board[row][column] == player and self.board[row][column + 1] == player and \
                        self.board[row][column + 2] == player and self.board[row][column + 3] == player:
                    return True

        for row in range(0, self.rows - 3, 1):
            for column in range(0, self.columns - 3, 1):
                if self.board[row][column] == player and self.board[row + 1][column + 1] == player and \
                        self.board[row + 2][column + 2] == player and self.board[row + 3][column + 3] == player:
                    return True

        for row in range(3, self.rows, 1):
            for column in range(0, self.columns - 3, 1):
                if self.board[row][column] == player and self.board[row - 1][column + 1] == player and \
                        self.board[row - 2][column + 2] == player and self.board[row - 3][column + 3] == player:
                    return True
        return False


    def switch_player(self):
        if self.currentPlayer == self.human:
            self.currentPlayer = self.ki
            self.lastPlayer = self.human
        else:
            self.currentPlayer = self.human
            self.lastPlayer = self.ki

    def check_column_free(self, column):
        return True if self.board[0][column - 1] == 0 else False

    def place_piece(self, column):
        if self.check_column_free(column):
            for i in range(self.rows - 1, -1, -1):
                if self.board[i][column - 1] == 0:
                    self.board[i][column - 1] = self.currentPlayer
                    self.turn_history.append((i, column - 1))
                    self.game_piece_counter += 1
                    self.switch_player()
                    self.animation_finished = False
                    self.animation_offset_pos = 0
                    return True
        return False

    def undo(self):
        if len(self.turn_history) == 0:
            return False
        last_turn = self.turn_history[-1]
        self.turn_history.pop(-1)
        self.board[last_turn[0]][last_turn[1]] = 0
        self.game_piece_counter -= 1
        self.switch_player()



    # This method must me called immediately after a piece was placed
    def check_win_fast(self):
        # Vertical Check
        if len(self.turn_history) == 0:
            return False

        last_turn = self.turn_history[-1]
        new_row = last_turn[0]
        new_column = last_turn[1]

        # Vertical Check
        if new_row < self.rows - 3:
            if self.board[new_row + 1][new_column] == self.lastPlayer and self.board[new_row + 2][new_column] == self.lastPlayer and \
                    self.board[new_row + 3][new_column] == self.lastPlayer:
                return True
        # Horizontal Check
        current_row = self.board[new_row]
        for pieces in range(0, self.columns - 3, 1):
            if current_row[pieces] == self.lastPlayer and current_row[pieces + 1] == self.lastPlayer and current_row[
                pieces + 2] == self.lastPlayer and current_row[pieces + 3] == self.lastPlayer:
                return True

        # Diagonal Check
        first_diagonal = []
        second_diagonal = []
        remain_diagonal_pieces_positive = self.columns - new_column if self.columns - new_column < new_row + 1 else new_row + 1
        remain_diagonal_pieces_negative = (new_column + 1 if new_column + 1 < self.rows - new_row else self.rows - new_row) * -1 + 1

        for i in range(remain_diagonal_pieces_negative, remain_diagonal_pieces_positive, 1):
            first_diagonal.append(self.board[new_row - i][new_column + i])

        remain_diagonal_pieces_positive = new_column + 1 if new_column + 1 < new_row + 1 else new_row + 1
        remain_diagonal_pieces_negative = (self.columns - new_column if self.columns - new_column < self.rows - new_row else self.rows - new_row) * -1 + 1
        for i in range(remain_diagonal_pieces_negative, remain_diagonal_pieces_positive, 1):
            second_diagonal.append(self.board[new_row - i][new_column - i])

        for i in range(0, len(first_diagonal) - 3, 1):
            if first_diagonal[i] == self.lastPlayer and first_diagonal[i + 1] == self.lastPlayer and first_diagonal[i + 2] == self.lastPlayer and \
                    first_diagonal[i + 3] == self.lastPlayer:
                return True

        for i in range(0, len(second_diagonal) - 3, 1):
            if second_diagonal[i] == self.lastPlayer and second_diagonal[i + 1] == self.lastPlayer and second_diagonal[
                i + 2] == self.lastPlayer and second_diagonal[i + 3] == self.lastPlayer:
                return True


    def search_for_three(self, pieces, player):
        four_minus_one_counter = 0
        free_piece = -1

        for piece in range(len(pieces)):
            if pieces[piece] == player:
                four_minus_one_counter += 1
            elif pieces[piece] == 0:
                free_piece = piece
            else:
                return -1

        if four_minus_one_counter == 3:
            return free_piece
        else:
            return -1



    def check_three_row(self, player):
        three_row_win_situations = []

        for row in range(0, self.rows, 1):
            for column in range(0, self.columns - 3, 1):
                tmp_four_line = (self.board[row][column], self.board[row][column + 1], \
                                 self.board[row][column + 2], self.board[row][column + 3])
                if (n:= self.search_for_three(tmp_four_line, player)) >= 0:
                    three_win_position = (row, column + n)
                    if three_win_position not in three_row_win_situations:
                        three_row_win_situations.append(three_win_position)


        for row in range(0, self.rows - 3, 1):
            for column in range(0, self.columns - 3, 1):
                tmp_four_line = (self.board[row][column], self.board[row + 1][column + 1], \
                        self.board[row + 2][column + 2] , self.board[row + 3][column + 3])
                if (n:= self.search_for_three(tmp_four_line, player)) >= 0:
                    three_win_position = (row + n, column + n)
                    if three_win_position not in three_row_win_situations:
                        three_row_win_situations.append(three_win_position)

        for row in range(3, self.rows, 1):
            for column in range(0, self.columns - 3, 1):
                tmp_four_line = (self.board[row][column], self.board[row - 1][column + 1], \
                        self.board[row - 2][column + 2], self.board[row - 3][column + 3])
                if (n:= self.search_for_three(tmp_four_line, player)) >= 0:
                    three_win_position = (row - n, column + n)
                    if three_win_position not in three_row_win_situations:
                        three_row_win_situations.append(three_win_position)

        return len(three_row_win_situations)


    def reset_game(self):
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.game_piece_counter = 0
        self.currentPlayer = random.randint(1, 2)
        self.lastPlayer = 2 if self.currentPlayer == 1 else 1
