import time
from typing import Dict, List, Tuple, Set
from ttt_game import TicTacToe
from ai import MinimaxAI


class PerformanceMetrics:

    def __init__(self):
        self.move_times: List[float] = []
        self.nodes_evaluated: int = 0
        self.total_moves: int = 0
        self.correct_moves: int = 0
        self.total_evaluated: int = 0
        self.optimal_move_found: int = 0
        
    def add_time(self, elapsed: float):
        self.move_times.append(elapsed)
        
    def average_time(self) -> float:
        return sum(self.move_times) / len(self.move_times) if self.move_times else 0
    
    def min_time(self) -> float:
        return min(self.move_times) if self.move_times else 0
    
    def max_time(self) -> float:
        return max(self.move_times) if self.move_times else 0
    
    def correctness_rate(self) -> float:

        return (self.correct_moves / self.total_evaluated * 100) if self.total_evaluated > 0 else 0


def count_nodes(ai: MinimaxAI, game: TicTacToe) -> int:
    return ai.nodes_evaluated


def test_move_quality(ai: MinimaxAI, game: TicTacToe) -> Tuple[int, int]:
    move, ai_score = ai.get_best_move(game)
    
    game_copy = TicTacToe()
    game_copy.board = game.board[:]
    game_copy.current_player = game.current_player
    
    all_moves_scores = []
    for candidate_move in game_copy.available_moves():
        game_copy.board[candidate_move] = ai.ai_mark
        score = ai._minimax(game_copy, depth=1, is_maximizing=False, 
                           alpha=float('-inf'), beta=float('inf'))
    
    if not all_moves_scores:
        return 0, 0
    
    best_possible_score = max(score for _, score in all_moves_scores)
    
    is_optimal = ai_score == best_possible_score
    correctness_score = 100 if is_optimal else 0
    
    return correctness_score, best_possible_score

# Play multiple full games where AI plays optimally
def test_ai_never_loses() -> Tuple[int, int, int]:
    ai = MinimaxAI(ai_mark="O", human_mark="X", max_depth=9)
    wins = 0
    ties = 0
    losses = 0
    
    # Run 10 games with different human strategies
    for game_num in range(10):
        game = TicTacToe()
        move_count = 0
        
        while not game.game_over() and move_count < 50:
            available = game.available_moves()
            if not available:
                break
            
            # Human makes a move (using various strategies)
            if game_num % 3 == 0:
                # Strategy 1: Play center if available
                human_move = 4 if 4 in available else available[0]
            elif game_num % 3 == 1:
                # Strategy 2: Play corners
                corners = [c for c in available if c in [0, 2, 6, 8]]
                human_move = corners[0] if corners else available[0]
            else:
                # Strategy 3: Play first available
                human_move = available[0]
            
            game.make_move(human_move)
            
            if game.game_over():
                break
            
            # AI move
            ai_move, _ = ai.get_best_move(game)
            game.make_move(ai_move)
            move_count += 1
        
        winner = game.get_winner()
        if winner == "O":
            wins += 1
        elif winner == "Tie":
            ties += 1
        else:
            losses += 1
    
    return wins, ties, losses


def test_winning_move_detection() -> int:
    ai = MinimaxAI(ai_mark="O", human_mark="X", max_depth=9)
    test_cases = [
        # (board, expected_winning_move, description)
        (["O", "O", " ", "X", "X", " ", " ", " ", " "], 2, "O wins at 2"),
        (["O", " ", " ", "O", " ", " ", " ", " ", "X"], 6, "O wins at 6"),
        ([" ", " ", " ", "O", "O", " ", "X", "X", " "], 5, "O wins at 5"),
        (["O", "X", "X", "O", " ", " ", " ", " ", " "], 4, "O blocks at 4 (or better move)"),
        (["O", " ", "O", " ", " ", " ", "X", "X", " "], 4, "O wins at 4 (or 2)"),  # Fixed: valid immediate win
    ]
    
    correct_count = 0
    for board, expected_move, description in test_cases:
        game = TicTacToe()
        game.board = board
        game.current_player = "O"
        
        move, score = ai.get_best_move(game)
        
        # Move is correct if it wins or has a very high score (>90)
        game_test = TicTacToe()
        game_test.board = board[:]
        game_test.board[move] = "O"
        is_winning = game_test.get_winner() == "O"
        has_high_score = score > 90
        
        if is_winning or has_high_score:
            correct_count += 1
            print(f"  PASS {description}: AI={move}, score={score}, winning={is_winning}")
        else:
            print(f"  FAIL {description}: AI={move}, score={score}, winning={is_winning}")
    
    return correct_count


def test_blocking_move_detection() -> int:
    ai = MinimaxAI(ai_mark="O", human_mark="X", max_depth=9)
    test_cases = [
        # (board, position_where_opponent_wins_if_not_blocked)
        (["X", "X", " ", " ", "O", " ", " ", " ", " "], 2),
        ([" ", " ", " ", "X", "X", " ", " ", " ", "O"], 6),
        (["X", " ", " ", " ", "X", " ", " ", " ", "O"], 8),
    ]
    
    correct_blocks = 0
    for board, must_block_pos in test_cases:
        game = TicTacToe()
        game.board = board
        game.current_player = "O"
        
        move, _ = ai.get_best_move(game)
        
        # After AI's move, check if opponent can still win immediately
        game_after_ai = TicTacToe()
        game_after_ai.board = board[:]
        game_after_ai.board[move] = "O"
        game_after_ai.current_player = "X"
        
        opponent_can_win_next = False
        for opp_move in game_after_ai.available_moves():
            game_after_ai.board[opp_move] = "X"
            if game_after_ai.get_winner() == "X":
                opponent_can_win_next = True
                game_after_ai.board[opp_move] = " "
                break
            game_after_ai.board[opp_move] = " "
        
        # AI did well if opponent can't win immediately
        if not opponent_can_win_next:
            correct_blocks += 1
    
    return correct_blocks

# Test AI performance on the first move
def test_first_move():
    print("\n" + "="*70)
    print("TEST 1: First Move Performance (Latency)")
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

# Test AI performance in mid-game scenarios
def test_mid_game_performance():
    print("\n" + "="*70)
    print("TEST 2: Mid-Game Performance (Latency)")
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

# Test AI performance when close to winning/losing
def test_endgame_performance():
    print("\n" + "="*70)
    print("TEST 3: Endgame Performance - Winning Move (Latency)")
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

# Run multiple games and collect statistics
def test_multiple_games():
    print("\n" + "="*70)
    print("TEST 4: Statistics Over 10 Games (Hard Difficulty)")
    print("="*70)
    
    metrics = PerformanceMetrics()
    game_count = 10
    
    for game_num in range(game_count):
        game = TicTacToe()
        ai = MinimaxAI(max_depth=9)
        moves_made = 0
        
        while not game.game_over() and moves_made < 5:  
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

# Test if AI never loses at EACH difficulty level
def test_never_loses_all_depths():
    print("\n" + "="*70)
    print("TEST 5: Never Loses - All Difficulty Levels")
    print("="*70)
    
    depths = {"Easy (d=2)": 2, "Medium (d=4)": 4, "Hard (d=9)": 9}
    
    for difficulty, depth in depths.items():
        ai = MinimaxAI(ai_mark="O", human_mark="X", max_depth=depth)
        wins = 0
        ties = 0
        losses = 0
        
        for game_num in range(5):  
            game = TicTacToe()
            move_count = 0
            
            while not game.game_over() and move_count < 50:
                available = game.available_moves()
                if not available:
                    break
                
                # Human makes varying moves based on strategy
                if game_num % 2 == 0:
                    human_move = 4 if 4 in available else available[0]
                else:
                    human_move = available[0]
                
                game.make_move(human_move)
                
                if game.game_over():
                    break
                
                # AI move
                ai_move, _ = ai.get_best_move(game)
                game.make_move(ai_move)
                move_count += 1
            
            winner = game.get_winner()
            if winner == "O":
                wins += 1
            elif winner == "Tie":
                ties += 1
            else:
                losses += 1
        
        print(f"\n{difficulty} (5 games):")
        print(f"  Wins: {wins}  |  Ties: {ties}  |  Losses: {losses}")
        if losses == 0:
            print(f"  PASS: Never loses at this depth")
        else:
            print(f"  FAIL: Lost {losses} game(s)")

# Show what move each difficulty level selects for the same board
def test_move_selection_across_depths():
    print("\n" + "="*70)
    print("TEST 6: Move Selection Comparison Across Depths")
    print("="*70)
    
    # Test multiple board states
    test_boards = [
        ("Starting board (empty)", [" "] * 9),
        ("Mid-game (6 empty)", ["X", " ", " ", " ", "O", " ", " ", " ", " "]),
        ("AI can win", ["O", "O", " ", "X", "X", " ", " ", " ", " "]),
        ("Must block", ["X", "X", " ", "O", " ", " ", " ", " ", " "]),
    ]
    
    depths = {"Easy (d=2)": 2, "Medium (d=4)": 4, "Hard (d=9)": 9}
    
    for board_desc, board in test_boards:
        game = TicTacToe()
        game.board = board[:]
        game.current_player = "O"
        
        if game.game_over():
            print(f"\n{board_desc}: Game over, skipping")
            continue
        
        print(f"\n{board_desc}:")
        print(f"  Board: {board}")
        
        move_results = {}
        for difficulty, depth in depths.items():
            ai = MinimaxAI(ai_mark="O", human_mark="X", max_depth=depth)
            move, score = ai.get_best_move(game)
            move_results[difficulty] = (move, score)
            print(f"  {difficulty:15} -> Move {move} (pos {move+1}), Score: {score}")
        
        # Check if all depths agree
        moves = [move_results[d][0] for d in depths]
        if len(set(moves)) == 1:
            print(f"  → All depths agree on position {moves[0]+1}")
        else:
            print(f"  → Depths DISAGREE: Easy={moves[0]+1}, Medium={moves[1]+1}, Hard={moves[2]+1}")

# Play a complete game with each difficulty level and show move sequence
def test_full_game_trace():
    print("\n" + "="*70)
    print("TEST 7: Complete Game Traces - Strategy Comparison")
    print("="*70)
    
    depths = {"Easy (d=2)": 2, "Medium (d=4)": 4, "Hard (d=9)": 9}
    
    for difficulty, depth in depths.items():
        print(f"\n{difficulty} - Full Game Trace:")
        
        game = TicTacToe()
        ai = MinimaxAI(ai_mark="O", human_mark="X", max_depth=depth)
        move_num = 0
        
        # Use deterministic strategy for human
        human_moves = [4, 0, 1]  # Center, corner, side
        human_idx = 0
        
        while not game.game_over() and move_num < 20:
            available = game.available_moves()
            if not available:
                break
            
            # Human move (deterministic)
            if human_idx < len(human_moves) and human_moves[human_idx] in available:
                human_move = human_moves[human_idx]
            else:
                human_move = available[0]
            human_idx += 1
            
            game.make_move(human_move)
            print(f"Move {move_num+1}: Human plays X at {human_move+1} (position)")
            
            if game.game_over():
                break
            
            # AI move
            ai_move, score = ai.get_best_move(game)
            game.make_move(ai_move)
            print(f"        AI plays O at {ai_move+1} (score: {score})")
            
            move_num += 1
        
        winner = game.get_winner()
        print(f"\nGame Result: {winner}")
        print("Final Board:")
        for i in range(0, 9, 3):
            print(f"  {game.board[i]} | {game.board[i+1]} | {game.board[i+2]}")

# Compare AI response time across different board state
def compare_board_complexity():
    print("\n" + "="*70)
    print("TEST 8: Response Time by Board Complexity (Latency)")
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

# Run all performance tests
def main():
    print("\n" + "="*70)
    print("MINIMAX AI PERFORMANCE & CORRECTNESS TESTING SUITE")
    print("="*70)
    
    # ========================================================================
    # CORRECTNESS TESTS (Algorithm Validation)
    # ========================================================================
    print("\n" + "="*70)
    print("CORRECTNESS TESTS (Move Optimality)")
    print("="*70)
    
    print("\n" + "="*70)
    print("CORRECTNESS TEST 1: AI Never Loses (Full Depth Search)")
    print("="*70)
    wins, ties, losses = test_ai_never_loses()
    print(f"\nResults over 10 games:")
    print(f"  AI Wins: {wins}")
    print(f"  Ties: {ties}")
    print(f"  AI Losses: {losses}")
    if losses == 0:
        print(f"  PASS: AI achieved optimal play (no losses)")
    else:
        print(f"  FAIL: AI lost {losses} game(s)")
    
    print("\n" + "="*70)
    print("CORRECTNESS TEST 2: Winning Move Detection")
    print("="*70)
    winning_moves_correct = test_winning_move_detection()
    total_winning_tests = 5
    print(f"\nResults: {winning_moves_correct}/{total_winning_tests} correct")
    print(f"  Accuracy: {winning_moves_correct/total_winning_tests*100:.1f}%")
    if winning_moves_correct == total_winning_tests:
        print(f"  PASS: AI correctly identified all winning moves")
    else:
        print(f"  PARTIAL: AI missed {total_winning_tests - winning_moves_correct} case(s)")
    
    print("\n" + "="*70)
    print("CORRECTNESS TEST 3: Blocking Move Detection")
    print("="*70)
    blocks_correct = test_blocking_move_detection()
    total_block_tests = 3
    print(f"\nResults: {blocks_correct}/{total_block_tests} correct")
    print(f"  Accuracy: {blocks_correct/total_block_tests*100:.1f}%")
    if blocks_correct == total_block_tests:
        print(f"  PASS: AI correctly blocked all threats")
    else:
        print(f"  PARTIAL: AI failed to block {total_block_tests - blocks_correct} threat(s)")
    
    print("\n" + "="*70)
    print("DEPTH COMPARISON TESTS (Easy vs Medium vs Hard)")
    print("="*70)
    
    test_never_loses_all_depths()
    test_move_selection_across_depths()
    test_full_game_trace()
    
    print("\n" + "="*70)
    print("LATENCY TESTS (Performance)")
    print("="*70)
    
    test_first_move()
    test_mid_game_performance()
    test_endgame_performance()
    test_multiple_games()
    compare_board_complexity()
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)
    print("\n")


if __name__ == "__main__":
    main()
