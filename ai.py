# ai.py

from math import inf
from typing import Tuple

from ttt_game import TicTacToe


class MinimaxAI:
    """
    Minimax AI with alpha-beta pruning and a simple point-based heuristic.
    """

    def __init__(self, ai_mark: str = "O", human_mark: str = "X", max_depth: int = 9) -> None:
        self.ai_mark = ai_mark
        self.human_mark = human_mark
        self.max_depth = max_depth
        self.nodes_evaluated = 0

    def get_best_move(self, game: TicTacToe) -> Tuple[int, int]:
        """
        Returns (best_move_index, best_score).
        The tutor explanation text is generated separately in tutor.py.
        """
        self.nodes_evaluated = 0  # Reset counter for this move
        best_score = -inf
        best_move = -1

        original_board = game.clone_board()
        for move in game.available_moves():
            # Try AI move
            game.board[move] = self.ai_mark
            score = self._minimax(game, depth=1, is_maximizing=False,
                                  alpha=-inf, beta=inf)
            game.board[move] = " "  # undo

            if score > best_score:
                best_score = score
                best_move = move

        # In case something weird happens (shouldn't) fall back to first available
        if best_move == -1:
            moves = game.available_moves()
            if moves:
                best_move = moves[0]
            else:
                best_move = 0

        return best_move, int(best_score)

    def _minimax(self,
                 game: TicTacToe,
                 depth: int,
                 is_maximizing: bool,
                 alpha: float,
                 beta: float) -> float:
        self.nodes_evaluated += 1
        winner = game.get_winner()
        # Terminal states
        if winner == self.ai_mark:
            # Prefer faster wins
            return 100 - depth
        elif winner == self.human_mark:
            # Prefer slower losses
            return depth - 100
        elif winner == "Tie":
            return 0

        # Depth limit reached: use heuristic evaluation
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
                    break  # beta cut-off
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
                    break  # alpha cut-off
            return best_val

    # ---------- Heuristic function ----------

    def _heuristic_score(self, board) -> float:
        """
        Simple point-based heuristic:
        - Center control
        - Corner control
        - Potential 2-in-a-row threats and opportunities
        """
        score = 0

        # Center control
        center = 4
        if board[center] == self.ai_mark:
            score += 3
        elif board[center] == self.human_mark:
            score -= 3

        # Corner control
        corners = [0, 2, 6, 8]
        for c in corners:
            if board[c] == self.ai_mark:
                score += 2
            elif board[c] == self.human_mark:
                score -= 2

        # Two-in-a-row possibilities
        for a, b, c in TicTacToe.WINNING_COMBOS:
            line = [board[a], board[b], board[c]]
            score += self._score_line(line)

        return score

    def _score_line(self, line) -> int:
        """
        Give points for lines that are favorable to the AI and subtract
        points for lines that are favorable to the human.
        """
        ai_count = line.count(self.ai_mark)
        human_count = line.count(self.human_mark)
        empty_count = line.count(" ")

        # If both players are in the line, it's neutral
        if ai_count > 0 and human_count > 0:
            return 0

        # Pure AI line
        if ai_count == 2 and empty_count == 1:
            return 5  # strong threat
        if ai_count == 1 and empty_count == 2:
            return 2  # mild opportunity

        # Pure human line
        if human_count == 2 and empty_count == 1:
            return -5  # need to block
        if human_count == 1 and empty_count == 2:
            return -2

        return 0
