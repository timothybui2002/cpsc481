# Minimax Tic Tac Toe with Alpha-Beta Pruning

An unbeatable AI Tic Tac Toe opponent using the minimax algorithm with alpha-beta pruning. Features an interactive GUI, tutor mode, and multiple difficulty levels.

**Group Members:** Moksh Patel, Sean Hawi, Timothy Bui, Christian Hernandez

## Quick Start

**Prerequisites:** Python 3.7+ (tkinter included by default)

```bash
python main.py
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

Run the included performance test suite:

```bash
python3 performance_test.py
```

This tests AI speed across 5 scenarios: first move, mid-game, endgame, multi-game stats, and board complexity analysis.

**Sample Results (Hard Difficulty):**
- First move: 31ms | Mid-game: 0.1ms | Winning move: <0.1ms
- Average move: 2.6ms | Full board is ~318x faster than empty (fewer branches)

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
- Alpha-beta pruning reduces time complexity from O(b^d) to O(b^(d/2))
- Heuristic evaluation: center +3, corners +2, threats ±5
- Game always starts with human (X)

