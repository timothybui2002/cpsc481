# main.py

from ttt_game import TicTacToe
from ai import MinimaxAI
from tutor import explain_move


def print_board(game: TicTacToe) -> None:
    b = game.board
    print()
    print(f" {b[0]} | {b[1]} | {b[2]} ")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]} ")
    print()


def get_human_move(game: TicTacToe) -> int:
    while True:
        try:
            raw = input("Choose your move (1-9): ").strip()
            idx = int(raw) - 1
            if idx in game.available_moves():
                return idx
            else:
                print("That spot is not available. Try again.")
        except ValueError:
            print("Please enter a number from 1 to 9.")


def main():
    print("=== Minimax Tic Tac Toe with Alpha-Beta Pruning ===")
    print("You can play against the AI and optionally see tutor explanations.")
    print()

    # Choose player mark
    human_mark = ""
    while human_mark not in ("X", "O"):
        human_mark = input("Do you want to be X or O? (X goes first): ").strip().upper()

    ai_mark = "O" if human_mark == "X" else "X"

    # Tutor mode
    tutor_mode = ""
    while tutor_mode not in ("Y", "N"):
        tutor_mode = input("Enable tutor explanations? (Y/N): ").strip().upper()
    tutor_enabled = tutor_mode == "Y"

    # Initialize game and AI
    game = TicTacToe()
    game.current_player = "X"  # X always starts
    ai = MinimaxAI(ai_mark=ai_mark, human_mark=human_mark, max_depth=9)

    print_board(game)

    while not game.game_over():
        if game.current_player == human_mark:
            print("Your turn.")
            move = get_human_move(game)
            game.make_move(move)
            print_board(game)
        else:
            print("AI is thinking...")
            original_board = game.clone_board()
            best_move, score = ai.get_best_move(game)
            # Apply move using game logic (also switches player)
            game.make_move(best_move)
            print_board(game)

            if tutor_enabled:
                explanation = explain_move(original_board, best_move, ai_mark, human_mark)
                print("Tutor explanation:")
                print(" ", explanation)
                print(f" (Internal score for this move: {score})")
                print()

    # Game over
    winner = game.get_winner()
    if winner == "Tie":
        print("Game over: It's a tie!")
    elif winner == human_mark:
        print("Game over: You win! (Nice job!)")
    else:
        print("Game over: The AI wins!")


if __name__ == "__main__":
    main()
