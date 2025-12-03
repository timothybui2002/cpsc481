# tutor.py

from typing import List

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


def is_winning_board(board: List[str], mark: str) -> bool:
    for a, b, c in WINNING_COMBOS:
        if board[a] == board[b] == board[c] == mark:
            return True
    return False


def move_blocks_win(original_board: List[str],
                    move: int,
                    ai_mark: str,
                    human_mark: str) -> bool:
    """
    Check if the human had a winning move at `move` that we are blocking.
    """
    # If the human could win by playing in 'move', then AI is blocking
    tmp = original_board[:]
    tmp[move] = human_mark
    return is_winning_board(tmp, human_mark)


def explain_move(original_board: List[str],
                 move: int,
                 ai_mark: str,
                 human_mark: str) -> str:
    """
    Returns a human-readable explanation of why the AI chose this move.
    """
    board_after = original_board[:]
    board_after[move] = ai_mark

    # 1. Winning move
    if is_winning_board(board_after, ai_mark):
        return (
            f"I placed {ai_mark} at position {move + 1} to create three in a row "
            "and win the game."
        )

    # 2. Blocking move
    if move_blocks_win(original_board, move, ai_mark, human_mark):
        return (
            f"I chose position {move + 1} to block your next move, which "
            "could have given you three in a row."
        )

    # 3. Center control
    if move == 4:
        return (
            "I took the center (position 5) because controlling the center "
            "gives more ways to make three in a row."
        )

    # 4. Corner control
    if move in (0, 2, 6, 8):
        return (
            f"I chose the corner at position {move + 1}. Corners are strong "
            "because they are part of multiple winning lines."
        )

    # 5. Side squares
    return (
        f"I placed {ai_mark} at position {move + 1} to keep pressure on you "
        "and set up future chances to make three in a row."
    )
