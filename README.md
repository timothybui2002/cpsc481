# Minimax Tic Tac Toe with Alpha-Beta Pruning

An unbeatable AI Tic Tac Toe opponent using the minimax algorithm with alpha-beta pruning. Features an interactive GUI, tutor mode, and multiple difficulty levels.

**Group Members:** Moksh Patel, Sean Hawi, Timothy Bui, Christian Hernandez

## Quick Start

**Prerequisites:** Python 3.7+ (tkinter included by default)

```bash
python3 main.py
```

**How to Play:**
- Select difficulty level (Easy/Medium/Hard)
- Toggle Tutor Mode to see AI explanations
- Click empty squares to place your X
- AI plays as O and is unbeatable on Hard difficulty

## Features

- **Minimax with Alpha-Beta Pruning**: Optimal move selection with performance optimization
- **3 Difficulty Levels**: Easy (depth 2), Medium (depth 4), Hard (depth 9)
- **Tutor Mode**: AI explains its strategic reasoning for each move
- **Interactive GUI**: Tkinter-based interface with scoreboard tracking
- **Heuristic Evaluation**: Prioritizes center/corner control and threat blocking

## Performance Testing

Run the comprehensive performance test suite:

```bash
python3 performance_test.py
```

**Test Coverage:**
- **Correctness**: AI never loses across all difficulty levels (10/10 games)
- **Depth Comparison**: Early termination behavior at depths 2, 4, and 9
- **Move Consistency**: Agreement on critical positions (wins/blocks)
- **Latency Analysis**: Response time across board states

**Key Results:**
- AI achieves perfect play even at shallow depth (d=2: 5/5 wins)
- First move: 30ms | Mid-game: <1ms | Endgame: <1ms
- Alpha-beta pruning effectiveness: ~300x speedup (empty board vs. 3 moves remaining)
- All moves under 30ms threshold for real-time play

## Testing

Run the unit test suite:

```bash
python -m unittest test_game -v
```

**Coverage:** 15 essential tests
- Game logic: board, moves, win detection, reset
- AI: valid moves, winning moves, blocking, difficulty levels
- Integration: AI doesn't lose on hard difficulty

## Files

- `main.py` - GUI and game loop
- `ttt_game.py` - Game logic
- `ai.py` - Minimax with alpha-beta pruning
- `tutor.py` - Move explanations
- `performance_test.py` - Benchmark suite
- `test_game.py` - Unit tests (15 essential tests)

## Technical Notes

- AI searches to configurable depth (9 = full game tree, guarantees optimal play)
- Alpha-beta pruning reduces time complexity from O(b^d) to O(b^(d/2)) (Knuth & Moore, 1975)
- Evaluation function: depth-adjusted terminal values (±100) + positional heuristic (center +3, corners +2, threats ±5)
- Graceful degradation: Even depth 2 achieves perfect play due to heuristic quality
- Game always starts with human (X)

## Academic References

This implementation follows principles from classic game AI research:
- **Knuth & Moore (1975)**: Alpha-beta pruning efficiency analysis
- **Schaeffer et al. (1992)**: Game-playing AI evaluation methodology
- **Russell & Norvig (2020)**: Minimax with evaluation functions (AIMA textbook)

