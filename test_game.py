import unittest
from ttt_game import TicTacToe
from ai import MinimaxAI


class TestTicTacToeGame(unittest.TestCase):
    
    def setUp(self):
        self.game = TicTacToe()
    
    # Board should be empty
    def test_board_initialization(self):
        self.assertEqual(self.game.board, [" "] * 9)
    
    # Valid move should be placed
    def test_make_move_valid(self):
        self.game.make_move(0)
        self.assertEqual(self.game.board[0], "X")
        self.assertEqual(self.game.current_player, "O")
    
    # Invalid should return false
    def test_make_move_invalid(self):
        self.game.make_move(0)
        self.assertFalse(self.game.make_move(0))  
        self.assertFalse(self.game.make_move(9))   
    
    # Avail moves should track empty squares
    def test_available_moves(self):
        self.assertEqual(len(self.game.available_moves()), 9)
        self.game.make_move(0)
        self.assertEqual(len(self.game.available_moves()), 8)
    
    # Hozizontal win should be detected
    def test_win_detection_horizontal(self):
        self.game.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.assertEqual(self.game.get_winner(), "X")
    
    # Verticle win should be detected
    def test_win_detection_vertical(self):
        self.game.board = ["X", " ", " ", "X", " ", " ", "X", " ", " "]
        self.assertEqual(self.game.get_winner(), "X")
    
    # Diagonal win should be detected
    def test_win_detection_diagonal(self):
        self.game.board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
        self.assertEqual(self.game.get_winner(), "X")
    
    # Full board with no winner is tie
    def test_tie_detection(self):
        self.game.board = ["X", "O", "X", "O", "X", "X", "O", "X", "O"]
        self.assertEqual(self.game.get_winner(), "Tie")
    
    # Ongoing game should return None
    def test_game_not_over(self):
        self.game.board = ["X", "O", " ", " ", " ", " ", " ", " ", " "]
        self.assertIsNone(self.game.get_winner())
    
    # Reset should clear board
    def test_reset_game(self):
        self.game.make_move(0)
        self.game.reset()
        self.assertEqual(self.game.board, [" "] * 9)
        self.assertEqual(self.game.current_player, "X")

# Test AI move selection
class TestMinimaxAI(unittest.TestCase):
    
    def setUp(self):
        self.game = TicTacToe()
        self.ai = MinimaxAI(max_depth=9)
    
    # AI should return a valid, available move
    def test_ai_returns_valid_move(self):
        move, score = self.ai.get_best_move(self.game)
        self.assertIn(move, self.game.available_moves())
    
    # AI should play a winning move
    def test_ai_finds_winning_move(self):
        self.game.board = ["O", "O", " ", "X", "X", " ", " ", " ", " "]
        self.game.current_player = "O"
        move, score = self.ai.get_best_move(self.game)
        self.assertEqual(move, 2)  # Winning pos
        
   # AI should block player's winning move
    def test_ai_blocks_player_win(self):
        self.game.board = ["X", "X", " ", "O", " ", " ", " ", " ", " "]
        self.game.current_player = "O"
        move, score = self.ai.get_best_move(self.game)
        self.assertEqual(move, 2)  # Blocking pos
    
    # AI should support different depth levels
    def test_difficulty_levels(self):
        easy_ai = MinimaxAI(max_depth=2)
        medium_ai = MinimaxAI(max_depth=4)
        hard_ai = MinimaxAI(max_depth=9)
        
        self.assertEqual(easy_ai.max_depth, 2)
        self.assertEqual(medium_ai.max_depth, 4)
        self.assertEqual(hard_ai.max_depth, 9)


class TestGameIntegration(unittest.TestCase):
    
    # AI on hard difficulty should win or tie
    def test_ai_never_loses(self):
        ai = MinimaxAI(max_depth=9)
        
        for _ in range(3):  
            game = TicTacToe()
            move_count = 0
            
            while not game.game_over() and move_count < 50:
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
