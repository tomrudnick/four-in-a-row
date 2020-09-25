import copy
import math
from concurrent import futures
class KI:
    #position_map  = [-1, -1, 1, 2, 2, 1, -1, -1]
    position_map = [-1, -1, 1, 2, 1, -1 , -1]
    def __init__(self, depth, game, maximize_player):
        self.depth = depth
        self.game = game
        self.maximize_player = maximize_player
        self.minimize_player = self.game.human if maximize_player == self.game.ki else self.game.ki


    def evaluate_board(self, board, depth):
        #print(board.board)
        total_eval_score = 0

        winCheck = board.check_win_fast()
        if winCheck:
            if board.lastPlayer == self.maximize_player:
                total_eval_score += 100
                total_eval_score += 10 * depth
            else:
                total_eval_score -= 100
                total_eval_score -= 10 * depth
        else:
            if board.check_tie_fast():
                total_eval_score = 0

        total_eval_score += 15 * board.check_three_row(self.maximize_player)
        total_eval_score -= 15 * board.check_three_row(self.minimize_player)

        for row in range(board.rows - 1, -1, -1):
            for column in range(0, board.columns, 1):
                if board.board[row][column] == self.maximize_player:
                    total_eval_score += self.position_map[column]
                elif board.board[row][column] == self.minimize_player:
                    total_eval_score += self.position_map[column] * -1
        return total_eval_score

    def minimax(self, current_board, depth, alpha, beta, is_maximizing):
        if depth == 0 or current_board.check_game_over():
            return self.evaluate_board(current_board, depth)

        if is_maximizing:
            max_eval = -9999
            for pos in range(1, self.game.columns + 1, 1):
                game_copy = copy.deepcopy(current_board)
                #print("Maximizing")
                if game_copy.place_piece(pos):
                    eval = self.minimax(game_copy, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = 9999
            for pos in range(1, self.game.columns + 1, 1):
                game_copy = copy.deepcopy(current_board)
                if game_copy.place_piece(pos):
                    eval = self.minimax(game_copy, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                    #print(game_copy.board)
            return min_eval

    def calculate_move(self):
        max_eval = -999
        move = -1
        #depth = int(0.3 * ((1 - self.game.columns / 10) ** 2) * math.exp(0.11*self.game.game_piece_counter - (self.game.columns - 6)) + self.depth,0)
        depth = round(int(0.2 * math.exp(0.11 * self.game.game_piece_counter)), 0)
        print("Current depth: " + str(depth))
        for column in range(1, self.game.columns + 1, 1):
            game_copy = copy.deepcopy(self.game)
            if game_copy.place_piece(column):
                eval = self.minimax(game_copy, depth, -9999, 9999, False)
                print("Evaluating column: " + str(column) + " eval Value: " + str(eval))
                if eval > max_eval:
                    max_eval = eval
                    move = column
        if move != -1:
            self.game.place_piece(move)

    def process_move(self, column, depth):
        game_copy = copy.deepcopy(self.game)
        game_copy.place_piece(column)
        return self.minimax(game_copy, depth, -9999, 9999, False)

    def calculate_move_multiple_processes(self):
        max_eval = -9999
        move = -1
        depth = int(round(0.2 * math.exp(0.11 * self.game.game_piece_counter) + self.depth, 0))
        columns_eval = []
        for column in range(1, self.game.columns + 1, 1):
            if self.game.check_column_free(column):
                columns_eval.append(column)
        with futures.ProcessPoolExecutor(max_workers=len(columns_eval)) as e:
            eval_processes = {e.submit(self.process_move, n, depth): n for n in columns_eval}
            res = futures.wait(eval_processes)
            for f in res.done:
                print("Evaluation of column: " + str(eval_processes[f]) + " eval Value: " + str(f.result()))
                if f.result() > max_eval:
                    max_eval = f.result()
                    move = eval_processes[f]
        if move != -1:
            self.game.place_piece(move)


