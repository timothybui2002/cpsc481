# ai.py

from math import inf
from typing import Tuple

from ttt_game import TicTacToe


class MinimaxAI:
    """
    Minimax AI with alpha-beta pruning and a point-based heuristic.
    """

    def __init__(self, ai_mark: str = "O", human_mark: str = "X", max_depth: int = 9) -> None:
        self.ai_mark = ai_mark
        self.human_mark = human_mark
        self.max_depth = max_depth
        self.nodes_evaluated = 0

    def get_best_move(self, game: TicTacToe) -> Tuple[int, int]:
        self.nodes_evaluated = 0
        best_score = -inf
        best_move = -1

        for move in game.available_moves():
            game.board[move] = self.ai_mark
            score = self._minimax(game, depth=1, is_maximizing=False,
                                  alpha=-inf, beta=inf)
            game.board[move] = " "

            if score > best_score:
                best_score = score
                best_move = move

        if best_move == -1:
            moves = game.available_moves()
            if moves:
                best_move = moves[0]

        return best_move, int(best_score)

    def _minimax(self,
                 game: TicTacToe,
                 depth: int,
                 is_maximizing: bool,
                 alpha: float,
                 beta: float) -> float:
        self.nodes_evaluated += 1
        winner = game.get_winner()
        if winner == self.ai_mark:
            return 100 - depth  # prefer faster wins
        elif winner == self.human_mark:
            return depth - 100  # prefer slower losses
        elif winner == "Tie":
            return 0

        if depth >= self.max_depth:
            return self._heuristic_score(game.board)

        if is_maximizing:
            best_val = -inf
            for move in game.available_moves():
                game.board[move] = self.ai_mark
                val = self._minimax(game, depth + 1, False, alpha, beta)
                game.board[move] = " "
                best_val = max(best_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return best_val
        else:
            best_val = inf
            for move in game.available_moves():
                game.board[move] = self.human_mark
                val = self._minimax(game, depth + 1, True, alpha, beta)
                game.board[move] = " "
                best_val = min(best_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return best_val

    def _heuristic_score(self, board) -> float:
        score = 0
        if board[4] == self.ai_mark:
            score += 3
        elif board[4] == self.human_mark:
            score -= 3

        for c in [0, 2, 6, 8]:
            if board[c] == self.ai_mark:
                score += 2
            elif board[c] == self.human_mark:
                score -= 2

        for a, b, c in TicTacToe.WINNING_COMBOS:
            score += self._score_line([board[a], board[b], board[c]])

        return score

    def _score_line(self, line) -> int:
        ai_count = line.count(self.ai_mark)
        human_count = line.count(self.human_mark)
        empty_count = line.count(" ")

        if ai_count > 0 and human_count > 0:
            return 0
        if ai_count == 2 and empty_count == 1:
            return 5
        if ai_count == 1 and empty_count == 2:
            return 2
        if human_count == 2 and empty_count == 1:
            return -5
        if human_count == 1 and empty_count == 2:
            return -2
        return 0
