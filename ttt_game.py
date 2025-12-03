# ttt_game.py

from typing import List, Optional

class TicTacToe:
    """
    Simple 3x3 Tic Tac Toe game logic.
    Board indices:
        0 | 1 | 2
        3 | 4 | 5
        6 | 7 | 8
    """

    WINNING_COMBOS = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    def __init__(self) -> None:
        self.board: List[str] = [" "] * 9
        self.current_player: str = "X"

    def reset(self) -> None:
        self.board = [" "] * 9
        self.current_player = "X"

    def available_moves(self) -> List[int]:
        return [i for i, v in enumerate(self.board) if v == " "]

    def make_move(self, index: int) -> bool:
        """Place current_player's mark at index if valid, then switch player."""
        if 0 <= index < 9 and self.board[index] == " ":
            self.board[index] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def is_full(self) -> bool:
        return all(v != " " for v in self.board)

    def get_winner(self) -> Optional[str]:
        """
        Returns:
            "X" or "O" if there is a winner,
            "Tie" if the board is full with no winner,
            None if the game is not over.
        """
        for a, b, c in self.WINNING_COMBOS:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]

        if self.is_full():
            return "Tie"

        return None

    def game_over(self) -> bool:
        return self.get_winner() is not None

    def clone_board(self) -> List[str]:
        return self.board[:]
