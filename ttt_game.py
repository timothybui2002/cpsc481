from typing import List, Optional

class TicTacToe:

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
        if 0 <= index < 9 and self.board[index] == " ":
            self.board[index] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def is_full(self) -> bool:
        return all(v != " " for v in self.board)

    def get_winner(self) -> Optional[str]:
        for a, b, c in self.WINNING_COMBOS:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return "Tie" if self.is_full() else None

    def game_over(self) -> bool:
        return self.get_winner() is not None

    def clone_board(self) -> List[str]:
        return self.board[:]
