"""
Unit tests for Tic Tac Toe game logic and AI.
Run with: python -m unittest test_game
"""

import unittest
from ttt_game import TicTacToe
from ai import MinimaxAI


class TestTicTacToeGame(unittest.TestCase):
    """Test core game logic."""
    
    def setUp(self):
        self.game = TicTacToe()
    
    def test_board_initialization(self):
        """Board should start empty."""
        self.assertEqual(self.game.board, [" "] * 9)
    
    def test_make_move_valid(self):
        """Valid move should be placed and switch player."""
        self.game.make_move(0)
        self.assertEqual(self.game.board[0], "X")
        self.assertEqual(self.game.current_player, "O")
    
    def test_make_move_invalid(self):
        """Invalid move should return False."""
        self.game.make_move(0)
        self.assertFalse(self.game.make_move(0))  # Already occupied
        self.assertFalse(self.game.make_move(9))   # Out of bounds
    
    def test_available_moves(self):
        """Available moves should track empty squares."""
        self.assertEqual(len(self.game.available_moves()), 9)
        self.game.make_move(0)
        self.assertEqual(len(self.game.available_moves()), 8)
    
    def test_win_detection_horizontal(self):
        """Horizontal win should be detected."""
        self.game.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.assertEqual(self.game.get_winner(), "X")
    
    def test_win_detection_vertical(self):
        """Vertical win should be detected."""
        self.game.board = ["X", " ", " ", "X", " ", " ", "X", " ", " "]
        self.assertEqual(self.game.get_winner(), "X")
    
    def test_win_detection_diagonal(self):
        """Diagonal win should be detected."""
        self.game.board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
        self.assertEqual(self.game.get_winner(), "X")
    
    def test_tie_detection(self):
        """Full board with no winner should be a tie."""
        self.game.board = ["X", "O", "X", "O", "X", "X", "O", "X", "O"]
        self.assertEqual(self.game.get_winner(), "Tie")
    
    def test_game_not_over(self):
        """Ongoing game should return None."""
        self.game.board = ["X", "O", " ", " ", " ", " ", " ", " ", " "]
        self.assertIsNone(self.game.get_winner())
    
    def test_reset_game(self):
        """Reset should clear board and reset player."""
        self.game.make_move(0)
        self.game.reset()
        self.assertEqual(self.game.board, [" "] * 9)
        self.assertEqual(self.game.current_player, "X")


class TestMinimaxAI(unittest.TestCase):
    """Test AI move selection."""
    
    def setUp(self):
        self.game = TicTacToe()
        self.ai = MinimaxAI(max_depth=9)
    
    def test_ai_returns_valid_move(self):
        """AI should return a valid, available move."""
        move, score = self.ai.get_best_move(self.game)
        self.assertIn(move, self.game.available_moves())
    
    def test_ai_finds_winning_move(self):
        """AI should find and play a winning move."""
        self.game.board = ["O", "O", " ", "X", "X", " ", " ", " ", " "]
        self.game.current_player = "O"
        move, score = self.ai.get_best_move(self.game)
        self.assertEqual(move, 2)  # Winning position
    
    def test_ai_blocks_player_win(self):
        """AI should block player's winning move."""
        self.game.board = ["X", "X", " ", "O", " ", " ", " ", " ", " "]
        self.game.current_player = "O"
        move, score = self.ai.get_best_move(self.game)
        self.assertEqual(move, 2)  # Blocking position
    
    def test_difficulty_levels(self):
        """AI should support different depth levels."""
        easy_ai = MinimaxAI(max_depth=2)
        medium_ai = MinimaxAI(max_depth=4)
        hard_ai = MinimaxAI(max_depth=9)
        
        self.assertEqual(easy_ai.max_depth, 2)
        self.assertEqual(medium_ai.max_depth, 4)
        self.assertEqual(hard_ai.max_depth, 9)


class TestGameIntegration(unittest.TestCase):
    """Test full game scenarios."""
    
    def test_ai_never_loses(self):
        """AI on hard difficulty should win or tie."""
        ai = MinimaxAI(max_depth=9)
        
        for _ in range(3):  # Run 3 games
            game = TicTacToe()
            move_count = 0
            
            while not game.game_over() and move_count < 50:
                # Human move (random available)
                available = game.available_moves()
                if available:
                    human_move = available[0]
                    game.make_move(human_move)
                
                if game.game_over():
                    break
                
                # AI move
                ai_move, _ = ai.get_best_move(game)
                game.make_move(ai_move)
                move_count += 1
            
            winner = game.get_winner()
            self.assertIn(winner, ["O", "Tie"], 
                         f"AI lost game with winner: {winner}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
