import tkinter as tk
from tkinter import messagebox, ttk

from ttt_game import TicTacToe
from ai import MinimaxAI
from tutor import explain_move


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - AI with Tutor Mode")

        # Game / AI settings
        self.game = TicTacToe()
        self.human_mark = "X"
        self.ai_mark = "O"

        # Difficulty levels mapped to max_depth for minimax
        self.difficulty_levels = {
            "Easy": 2,
            "Medium": 4,
            "Hard": 9
        }
        self.current_difficulty = tk.StringVar(value="Hard")

        # Initialize AI with default difficulty
        self.ai = MinimaxAI(
            ai_mark=self.ai_mark,
            human_mark=self.human_mark,
            max_depth=self.difficulty_levels[self.current_difficulty.get()]
        )

        # Tutor mode flag
        self.tutor_enabled = tk.BooleanVar(value=True)

        # Scoreboard
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0

        # UI elements
        self.buttons = []
        self.status_label = None
        self.player_score_label = None
        self.ai_score_label = None
        self.tie_score_label = None

        self.build_ui()
        self.update_board()
        self.update_status("Your turn (X).")

    # ---------- UI construction ----------

    def build_ui(self):
        # Top control panel
        control_frame = tk.Frame(self.root, pady=5)
        control_frame.pack()

        # Difficulty selector
        tk.Label(control_frame, text="Difficulty:").grid(
            row=0, column=0, padx=5)
        difficulty_menu = ttk.OptionMenu(
            control_frame,
            self.current_difficulty,
            self.current_difficulty.get(),
            *self.difficulty_levels.keys(),
            command=self.on_change_difficulty
        )
        difficulty_menu.grid(row=0, column=1, padx=5)

        # Tutor mode toggle
        tutor_check = tk.Checkbutton(
            control_frame,
            text="Tutor mode",
            variable=self.tutor_enabled,
            onvalue=True,
            offvalue=False
        )
        tutor_check.grid(row=0, column=2, padx=5)

        # Restart game button
        restart_button = tk.Button(
            control_frame,
            text="Restart Game",
            command=self.reset_game
        )
        restart_button.grid(row=0, column=3, padx=5)

        # Reset scores button
        reset_scores_button = tk.Button(
            control_frame,
            text="Reset Scores",
            command=self.reset_scores
        )
        reset_scores_button.grid(row=0, column=4, padx=5)

        # Board frame
        board_frame = tk.Frame(self.root, pady=10)
        board_frame.pack()

        for i in range(9):
            btn = tk.Button(
                board_frame,
                text=" ",
                width=5,
                height=2,
                font=("Arial", 28),
                command=lambda idx=i: self.player_move(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)

        # Status label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=2)

        # Scoreboard frame
        score_frame = tk.Frame(self.root, pady=5)
        score_frame.pack()

        self.player_score_label = tk.Label(
            score_frame, text="Player (X) wins: 0", font=("Arial", 11)
        )
        self.player_score_label.grid(row=0, column=0, padx=10)

        self.ai_score_label = tk.Label(
            score_frame, text="AI (O) wins: 0", font=("Arial", 11)
        )
        self.ai_score_label.grid(row=0, column=1, padx=10)

        self.tie_score_label = tk.Label(
            score_frame, text="Ties: 0", font=("Arial", 11)
        )
        self.tie_score_label.grid(row=0, column=2, padx=10)

    # ---------- Helpers ----------

    def update_board(self):
        for i in range(9):
            self.buttons[i].config(
                text=self.game.board[i],
                bg="SystemButtonFace"  # reset color (for winning highlight)
            )

    def update_status(self, text):
        if self.status_label is not None:
            self.status_label.config(text=text)

    def on_change_difficulty(self, _value):
        level = self.current_difficulty.get()
        depth = self.difficulty_levels[level]
        self.ai.max_depth = depth
        self.update_status(f"Difficulty set to {level}. Your turn (X).")

    def highlight_winning_line(self):
        winner = self.game.get_winner()
        if winner not in (self.human_mark, self.ai_mark):
            return

        from ttt_game import TicTacToe as GameClass  # reuse WINNING_COMBOS
        for a, b, c in GameClass.WINNING_COMBOS:
            line = [self.game.board[a], self.game.board[b], self.game.board[c]]
            if line[0] != " " and line[0] == line[1] == line[2]:
                for idx in (a, b, c):
                    self.buttons[idx].config(bg="lightgreen")
                break

    def reset_game(self):
        self.game.reset()
        self.update_board()
        self.update_status("New game started. Your turn (X).")
        self.root.bell()

    def reset_scores(self):
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.refresh_scoreboard()
        self.update_status("Scores reset.")

    def refresh_scoreboard(self):
        self.player_score_label.config(
            text=f"Player (X) wins: {self.player_wins}")
        self.ai_score_label.config(text=f"AI (O) wins: {self.ai_wins}")
        self.tie_score_label.config(text=f"Ties: {self.ties}")

    # ---------- Game flow ----------

    def player_move(self, index):
        # Ignore clicks on finished game or occupied squares
        if self.game.game_over() or self.game.board[index] != " ":
            return

        # Player move
        self.game.make_move(index)
        self.update_board()
        self.root.bell()
        self.update_status("AI is thinking...")

        if self.game.game_over():
            self.end_game()
            return

        # AI move after slight delay
        self.root.after(250, self.ai_move)

    def ai_move(self):
        original = self.game.clone_board()
        move, score = self.ai.get_best_move(self.game)
        self.game.make_move(move)
        self.update_board()
        self.root.bell()

        if self.tutor_enabled.get():
            explanation = explain_move(
                original, move, self.ai_mark, self.human_mark)
            full_message = explanation + \
                f"\n\nInternal score for this move: {score}"
            messagebox.showinfo("AI Explanation", full_message)

        if self.game.game_over():
            self.end_game()
        else:
            self.update_status("Your turn (X).")

    def end_game(self):
        winner = self.game.get_winner()

        if winner == "Tie":
            self.ties += 1
            self.update_status("Game over: tie.")
            self.root.bell()
            messagebox.showinfo("Game Over", "It is a tie.")
        elif winner == self.human_mark:
            self.player_wins += 1
            self.highlight_winning_line()
            self.update_status("Game over: you win.")
            self.root.bell()
            messagebox.showinfo("Game Over", "You win!")
        else:
            self.ai_wins += 1
            self.highlight_winning_line()
            self.update_status("Game over: AI wins.")
            self.root.bell()
            messagebox.showinfo("Game Over", "AI wins.")

        self.refresh_scoreboard()
        # Start a new game after the dialog
        self.reset_game()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

