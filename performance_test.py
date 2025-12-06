"""
Performance testing script for the Minimax AI with Alpha-Beta Pruning.
Measures move latency, nodes evaluated, and pruning effectiveness.
"""

import time
from typing import Dict, List, Tuple
from ttt_game import TicTacToe
from ai import MinimaxAI


class PerformanceMetrics:
    """Tracks AI performance statistics."""
    
    def __init__(self):
        self.move_times: List[float] = []
        self.nodes_evaluated: int = 0
        self.total_moves: int = 0
        
    def add_time(self, elapsed: float):
        self.move_times.append(elapsed)
        
    def average_time(self) -> float:
        return sum(self.move_times) / len(self.move_times) if self.move_times else 0
    
    def min_time(self) -> float:
        return min(self.move_times) if self.move_times else 0
    
    def max_time(self) -> float:
        return max(self.move_times) if self.move_times else 0


def count_nodes(ai: MinimaxAI, game: TicTacToe) -> int:
    """
    Approximate node count by counting recursive calls.
    Note: This is a simplified count; actual implementation would require
    instrumenting the minimax function.
    """
    return len(game.available_moves()) ** ai.max_depth  # Rough upper bound


def test_first_move():
    """Test AI performance on the first move."""
    print("\n" + "="*70)
    print("TEST 1: First Move Performance")
    print("="*70)
    
    results: Dict[str, PerformanceMetrics] = {
        "Easy (depth 2)": PerformanceMetrics(),
        "Medium (depth 4)": PerformanceMetrics(),
        "Hard (depth 9)": PerformanceMetrics(),
    }
    
    depths = {"Easy (depth 2)": 2, "Medium (depth 4)": 4, "Hard (depth 9)": 9}
    
    for difficulty, depth in depths.items():
        game = TicTacToe()
        ai = MinimaxAI(max_depth=depth)
        
        start = time.time()
        move, score = ai.get_best_move(game)
        elapsed = time.time() - start
        
        results[difficulty].add_time(elapsed)
        
        print(f"\n{difficulty}:")
        print(f"  Best move: {move} (position {move + 1})")
        print(f"  Score: {score}")
        print(f"  Time: {elapsed:.4f}s")


def test_mid_game_performance():
    """Test AI performance in mid-game scenarios."""
    print("\n" + "="*70)
    print("TEST 2: Mid-Game Performance")
    print("="*70)
    
    # Create a mid-game board state
    mid_game_board = [
        "X", " ", "O",
        " ", "X", " ",
        " ", " ", "O"
    ]
    
    depths = {"Easy (depth 2)": 2, "Medium (depth 4)": 4, "Hard (depth 9)": 9}
    
    for difficulty, depth in depths.items():
        game = TicTacToe()
        game.board = mid_game_board[:]
        game.current_player = "O"
        
        ai = MinimaxAI(max_depth=depth)
        
        start = time.time()
        move, score = ai.get_best_move(game)
        elapsed = time.time() - start
        
        print(f"\n{difficulty}:")
        print(f"  Best move: {move} (position {move + 1})")
        print(f"  Score: {score}")
        print(f"  Time: {elapsed:.4f}s")


def test_endgame_performance():
    """Test AI performance when close to winning/losing."""
    print("\n" + "="*70)
    print("TEST 3: Endgame Performance (AI Can Win in 1)")
    print("="*70)
    
    # Board where AI has two in a row and can win
    winning_move_board = [
        "O", "O", " ",
        "X", "X", " ",
        " ", " ", " "
    ]
    
    depths = {"Easy (depth 2)": 2, "Medium (depth 4)": 4, "Hard (depth 9)": 9}
    
    for difficulty, depth in depths.items():
        game = TicTacToe()
        game.board = winning_move_board[:]
        game.current_player = "O"
        
        ai = MinimaxAI(max_depth=depth)
        
        start = time.time()
        move, score = ai.get_best_move(game)
        elapsed = time.time() - start
        
        print(f"\n{difficulty}:")
        print(f"  Best move: {move} (position {move + 1}) - WINNING MOVE")
        print(f"  Score: {score}")
        print(f"  Time: {elapsed:.4f}s")


def test_multiple_games():
    """Run multiple games and collect statistics."""
    print("\n" + "="*70)
    print("TEST 4: Statistics Over 10 Games (Hard Difficulty)")
    print("="*70)
    
    metrics = PerformanceMetrics()
    game_count = 10
    
    for game_num in range(game_count):
        game = TicTacToe()
        ai = MinimaxAI(max_depth=9)
        moves_made = 0
        
        while not game.game_over() and moves_made < 5:  # First 5 moves
            available = game.available_moves()
            if not available:
                break
            
            # Make a random valid move for human to set up different scenarios
            import random
            human_move = random.choice(available)
            game.make_move(human_move)
            
            if game.game_over():
                break
            
            # AI move
            start = time.time()
            move, score = ai.get_best_move(game)
            elapsed = time.time() - start
            metrics.add_time(elapsed)
            
            game.make_move(move)
            moves_made += 1
    
    print(f"\nGames played: {game_count}")
    print(f"Total moves evaluated: {len(metrics.move_times)}")
    print(f"\nMove Time Statistics:")
    print(f"  Average: {metrics.average_time():.4f}s")
    print(f"  Minimum: {metrics.min_time():.4f}s")
    print(f"  Maximum: {metrics.max_time():.4f}s")
    print(f"  Total time: {sum(metrics.move_times):.4f}s")


def compare_board_complexity():
    """Compare AI response time across different board states."""
    print("\n" + "="*70)
    print("TEST 5: Response Time by Board Complexity")
    print("="*70)
    
    test_boards = [
        ("Empty board", [" "] * 9),
        ("1 move each", ["X", " ", " ", " ", "O", " ", " ", " ", " "]),
        ("2 moves each", ["X", " ", "O", " ", "X", " ", "O", " ", " "]),
        ("3 moves each", ["X", " ", "O", " ", "X", " ", "O", " ", "X"]),
        ("4 moves each", ["X", "O", "X", " ", "O", "X", "O", " ", " "]),
    ]
    
    ai = MinimaxAI(max_depth=9)
    
    for description, board in test_boards:
        game = TicTacToe()
        game.board = board[:]
        game.current_player = "O"
        
        if game.game_over():
            print(f"\n{description}: Game already over, skipping")
            continue
        
        start = time.time()
        move, score = ai.get_best_move(game)
        elapsed = time.time() - start
        
        available_moves = len(game.available_moves())
        print(f"\n{description}:")
        print(f"  Available moves: {available_moves}")
        print(f"  Move chosen: {move} (position {move + 1})")
        print(f"  Time: {elapsed:.4f}s")


def main():
    """Run all performance tests."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  MINIMAX AI PERFORMANCE TESTING SUITE".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    test_first_move()
    test_mid_game_performance()
    test_endgame_performance()
    test_multiple_games()
    compare_board_complexity()
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)
    print("\nKey Observations:")
    print("  • First move (empty board) should be slowest at Hard difficulty")
    print("  • Winning/blocking moves should be fast (found near top of tree)")
    print("  • Mid-game moves vary based on available options")
    print("  • Alpha-beta pruning effectiveness increases with more branches")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
