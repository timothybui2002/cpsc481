import tkinter as tk
from tkinter import ttk

from ttt_game import TicTacToe
from ai import MinimaxAI
from tutor import explain_move


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - AI with Tutor Mode")

        # Game settings
        self.game = TicTacToe()
        self.human_mark = "X"
        self.ai_mark = "O"

        self.difficulty_levels = {"Easy": 2, "Medium": 4, "Hard": 9}
        self.current_difficulty = tk.StringVar(value="Hard")

        self.ai = MinimaxAI(
            ai_mark=self.ai_mark,
            human_mark=self.human_mark,
            max_depth=self.difficulty_levels[self.current_difficulty.get()]
        )

        self.tutor_enabled = tk.BooleanVar(value=True)

        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0

        self.buttons = []
        self.status_label = None
        self.explanation_label = None

        self.countdown_after_id = None  # fixes double reset issues

        self.build_ui()
        self.update_board()
        self.update_status("Your turn (X).")  # << this line is now correct

    # -------------------------------------------------------------------------
    def build_ui(self):
        control_frame = tk.Frame(self.root, pady=5)
        control_frame.pack()

        tk.Label(control_frame, text="Difficulty:").grid(row=0, column=0, padx=5)
        ttk.OptionMenu(
            control_frame, self.current_difficulty, self.current_difficulty.get(),
            *self.difficulty_levels.keys(), command=self.on_change_difficulty
        ).grid(row=0, column=1, padx=5)

        tk.Checkbutton(control_frame, text="Tutor mode", variable=self.tutor_enabled)\
            .grid(row=0, column=2, padx=5)

        tk.Button(control_frame, text="Restart Game", command=self.reset_game)\
            .grid(row=0, column=3, padx=5)

        tk.Button(control_frame, text="Reset Scores", command=self.reset_scores)\
            .grid(row=0, column=4, padx=5)

        board_frame = tk.Frame(self.root, pady=10)
        board_frame.pack()

        for i in range(9):
            btn = tk.Button(
                board_frame, text=" ", width=5, height=2, font=("Arial", 28),
                command=lambda idx=i: self.player_move(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack()

        self.explanation_label = tk.Label(
            self.root, text="", wraplength=330, justify="left",
            font=("Arial", 12), fg="white", bg="black", padx=6, pady=6
        )

        score_frame = tk.Frame(self.root, pady=5)
        score_frame.pack()

        self.player_score_label = tk.Label(score_frame, text="Player (X) wins: 0", font=("Arial", 11))
        self.player_score_label.grid(row=0, column=0, padx=10)

        self.ai_score_label = tk.Label(score_frame, text="AI (O) wins: 0", font=("Arial", 11))
        self.ai_score_label.grid(row=0, column=1, padx=10)

        self.tie_score_label = tk.Label(score_frame, text="Ties: 0", font=("Arial", 11))
        self.tie_score_label.grid(row=0, column=2, padx=10)

    # -------------------------------------------------------------------------
    def cancel_countdown(self):
        if self.countdown_after_id:
            self.root.after_cancel(self.countdown_after_id)
            self.countdown_after_id = None

    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=self.game.board[i], bg="SystemButtonFace")

    def update_status(self, text):
        self.status_label.config(text=text)

    def on_change_difficulty(self, _):
        self.ai.max_depth = self.difficulty_levels[self.current_difficulty.get()]
        self.update_status(f"Difficulty set to {self.current_difficulty.get()}. Your turn (X).")

    def highlight_winning_line(self):
        from ttt_game import TicTacToe as G
        for a, b, c in G.WINNING_COMBOS:
            if self.game.board[a] == self.game.board[b] == self.game.board[c] != " ":
                for idx in (a, b, c):
                    self.buttons[idx].config(bg="lightgreen")
                break

    # -------------------------------------------------------------------------
    def reset_game(self):
        self.cancel_countdown()
        self.game.reset()
        self.update_board()
        self.update_status("Your turn (X).")
        self.explanation_label.pack_forget()

    def reset_scores(self):
        self.cancel_countdown()
        self.player_wins = self.ai_wins = self.ties = 0
        self.refresh_scoreboard()
        self.update_status("Scores reset.")
        self.explanation_label.pack_forget()

    def refresh_scoreboard(self):
        self.player_score_label.config(text=f"Player (X) wins: {self.player_wins}")
        self.ai_score_label.config(text=f"AI (O) wins: {self.ai_wins}")
        self.tie_score_label.config(text=f"Ties: {self.ties}")

    # -------------------------------------------------------------------------
    def player_move(self, index):
        if self.game.game_over() or self.game.board[index] != " ":
            return

        self.game.make_move(index)
        self.update_board()
        self.update_status("AI is thinking...")

        if self.game.game_over():
            self.end_game()
            return

        self.root.after(250, self.ai_move)

    def ai_move(self):
        if self.game.game_over():
            return

        original = self.game.clone_board()
        move, score = self.ai.get_best_move(self.game)
        self.game.make_move(move)
        self.update_board()

        if self.tutor_enabled.get():
            msg = explain_move(original, move, self.ai_mark, self.human_mark) + f"\n\nMove Score: {score}"
            if not self.explanation_label.winfo_ismapped():
                self.explanation_label.pack(pady=8)
            self.explanation_label.config(text=msg)

        if self.game.game_over():
            self.end_game()
        else:
            self.update_status("Your turn (X).")

    # -------------------------------------------------------------------------
    def end_game(self):
        winner = self.game.get_winner()

        if winner == "Tie":
            self.ties += 1
            self.update_status("Tie game!")
        elif winner == self.human_mark:
            self.player_wins += 1
            self.highlight_winning_line()
            self.update_status("You win!")
        else:
            self.ai_wins += 1
            self.highlight_winning_line()
            self.update_status("AI wins!")

        self.refresh_scoreboard()
        self.cancel_countdown()
        self.start_countdown(5)

    def start_countdown(self, t):
        if t > 0:
            self.update_status(f"New game in {t}...")
            self.countdown_after_id = self.root.after(1000, lambda: self.start_countdown(t-1))
        else:
            self.countdown_after_id = None
            self.reset_game()


# -------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()