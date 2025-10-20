# Checkers Bot - AI Mini Project

A Python implementation of a Checkers game with an AI bot that uses various search strategies to play against a human player.

## ✨ Features

- 🎮 **Multiple Interfaces**: Choose between command-line or beautiful graphical interfaces
- 🤖 **Three AI Strategies**: Minimax, Alpha-Beta Pruning, and Alpha-Beta with Ordering
- 📊 **Real-Time Analytics**: Track nodes expanded, generated, pruned, and time usage
- 🎯 **Configurable Difficulty**: Adjust time limits (1-3s) and search depth (5-9 plies)
- 👑 **Full Checkers Rules**: King promotion, forced captures, and multiple jumps
- 📈 **Performance Charts**: Visual analytics with matplotlib (Advanced GUI)
- 🎨 **Modern UI**: Beautiful dark theme with intuitive controls
- 📜 **Move History**: Track and review all moves during the game
- 🏆 **Game Statistics**: Comprehensive analytics for both players

## Project Structure

The code is organized into 4 main classes/packages as required, plus additional GUI implementations:

```
miniproject2/
├── OtherStuff.py                  # Utility functions and helper methods
├── GameBoard/                      # Game board representation and logic
│   ├── __init__.py
│   └── board.py                   # GameBoard class
├── SearchToolBox/                 # AI search algorithms
│   ├── __init__.py
│   └── search.py                  # SearchToolBox class
├── PlayingTheGame.py              # Game manager and main execution (CLI)
├── CheckersGUI.py                 # 🎮 Standard GUI (Tkinter only)
├── CheckersGUI_Advanced.py        # 🎮 Advanced GUI (with matplotlib charts)
├── requirements_gui.txt           # Optional dependencies for Advanced GUI
├── GUI_USER_GUIDE.md              # Comprehensive GUI user guide
├── QUICK_REFERENCE.md             # Quick reference card for GUI
├── BONUS_IMPLEMENTATION.md        # Documentation for 10% bonus implementation
└── README.md                      # This file
```

## Classes Description

### 1. OtherStuff
Contains miscellaneous helper functions:
- `StartingMoveLocation(r, c)`: Returns starting move location tuple
- `TargetingMoveLocation(r, c)`: Returns target move location tuple
- `OpponentOf(player)`: Returns opponent's symbol

### 2. GameBoard
Represents the checkers board and game state:
- 8x8 board with standard American checkers rules
- Move generation with forced-capture logic
- Multiple jumps support
- King promotion when reaching last row
- Heuristic evaluation function
- Board display utilities

**Piece Representation:**
- `w`: White piece (human)
- `W`: White king
- `b`: Black piece (AI agent)
- `B`: Black king
- `.`: Empty square

### 3. SearchToolBox
Implements AI search strategies:
- **Minimax**: Basic minimax algorithm
- **Alpha-Beta**: Minimax with alpha-beta pruning
- **Alpha-Beta with Ordering**: Alpha-beta with heuristic node ordering

**Features:**
- Time-limited search (T: 1-3 seconds)
- Depth-limited search (P: 5-9 plies)
- Analytics tracking:
  - Nodes expanded
  - Nodes generated
  - Pruning statistics
  - Ordering effectiveness

### 4. PlayingTheGame
High-level game manager:
- Interactive game loop
- Human input handling
- AI move selection
- Per-move analytics reporting
- Cumulative statistics tracking

## How to Run

### 🎮 Graphical User Interface (GUI) - **RECOMMENDED**

#### Option 1: Standard GUI (Tkinter only)
For a beautiful graphical interface with real-time analytics:
```bash
python CheckersGUI.py
```

**Features:**
- 🎨 Beautiful, modern graphical board with gradient effects
- 🖱️ Click-to-move interface (no typing coordinates!)
- 📊 Real-time analytics dashboard
- 📈 Visual statistics tracking
- 📜 Move history with color coding
- ⚙️ Easy configuration with sliders and radio buttons
- 👑 Visual king representation with crowns

#### Option 2: Advanced GUI with Charts (Requires matplotlib)
For the ultimate experience with interactive analytics charts:
```bash
python CheckersGUI_Advanced.py
```

**Additional Features:**
- 📊 **Interactive Analytics Charts** using matplotlib
  - Nodes expanded per move (line chart)
  - Time per move (line chart)
  - Alpha-beta prunes per move (line chart)
  - Cumulative statistics comparison
- 🎯 Tabbed interface (Game Board + Analytics Charts)
- 🎨 Enhanced dark theme
- 📈 Real-time chart updates after each move
- 💡 Quick stats cards with emoji indicators

**Installation for Advanced GUI:**
```bash
pip install matplotlib
# or
pip install -r requirements_gui.txt
```

### 💻 Command-Line Interface

1. **Basic execution:**
```bash
python PlayingTheGame.py
```

2. **Configuration:**
When you run the program, you'll be prompted to configure:
- **Strategy (S)**: Choose from:
  1. Minimax
  2. Alpha-Beta
  3. Alpha-Beta with Ordering (default)
- **Time Limit (T)**: 1-3 seconds per move (default: 2)
- **Max Plies (P)**: 5-9 plies depth (default: 6)

3. **Playing the game:**
- White (human) always starts first
- Input format: `start_row start_col target_row target_col`
- Example: `5 0 4 1` (moves piece from row 5, col 0 to row 4, col 1)
- Coordinates are 0-based (0-7)

## Game Rules

1. **Movement:**
   - Regular pieces move diagonally forward
   - Kings can move diagonally in any direction

2. **Captures:**
   - Captures are mandatory (forced-capture rule)
   - Multiple jumps are allowed in a single turn
   - Captured pieces are removed from the board

3. **Winning:**
   - Game ends when one player has no pieces left
   - That player loses

## Analytics

The bot tracks and reports:
- **Per-move analytics:**
  - Nodes expanded
  - Nodes generated
  - Alpha-beta prunes
  - Time used
  - Ordering effectiveness (if enabled)

- **Cumulative analytics:**
  - Total moves per player
  - Total nodes expanded
  - Total nodes generated
  - Total prunes

## Requirements

### Core Game (Command-Line)
- Python 3.7+
- Standard library only (no external dependencies)

### GUI Versions
- **Standard GUI** (`CheckersGUI.py`): Python 3.7+ with Tkinter (included by default)
- **Advanced GUI** (`CheckersGUI_Advanced.py`): Requires matplotlib
  ```bash
  pip install matplotlib
  ```

## Example Session

```
=== Checkers Agent ===
Configure Agent (press Enter to accept defaults).
Choose strategy S: 1) Minimax  2) AlphaBeta  3) AlphaBetaOrdering (default 3)
S> 3
Choose time limit T in seconds (1 to 3) (default 2):
T> 2
Choose max plies P (5 to 9) (default 6):
P> 6

Starting Checkers game. You are White (w). Input moves as: start_row start_col target_row target_col (0-based).
Agent search strategy: AlphaBetaOrdering, Time limit T=2.0s, MaxPly P=6
    0 1 2 3 4 5 6 7
   +----------------+
0 | . b . b . b . b |
1 | b . b . b . b . |
2 | . b . b . b . b |
3 | . . . . . . . . |
4 | . . . . . . . . |
5 | w . w . w . w . |
6 | . w . w . w . w |
7 | w . w . w . w . |
   +----------------+

Your move (start_row start_col target_row target_col): 5 0 4 1
...
```

## GUI Features & Screenshots

### Standard GUI (CheckersGUI.py)
The standard GUI provides a clean, modern interface with:
- **Interactive Board**: Click pieces to select, click destination to move
- **Color-Coded Squares**: 
  - Orange = selected piece
  - Gold = legal move destinations
  - Standard checkerboard pattern
- **Piece Visualization**: White circles with black outlines, black circles with white outlines
- **King Crowns**: Gold crowns appear on promoted pieces
- **Configuration Panel**: Easy-to-use radio buttons and spinboxes
- **Analytics Dashboard**: Real-time statistics for both players
- **Move History**: Scrollable log of all moves with color coding
- **Last Move Details**: Shows nodes expanded, generated, prunes, and time for agent's last move

### Advanced GUI (CheckersGUI_Advanced.py)
The advanced GUI includes everything from the standard GUI plus:
- **Tabbed Interface**: Separate tabs for game board and analytics charts
- **Real-Time Charts**: Four matplotlib charts showing:
  1. Nodes expanded per move (line chart)
  2. Time taken per move (line chart)
  3. Alpha-beta prunes per move (line chart)
  4. Cumulative statistics comparison
- **Enhanced Dark Theme**: Professional dark theme with accent colors
- **Quick Stats Cards**: Large, easy-to-read cards showing key metrics
- **Animated Charts**: Charts update in real-time after each agent move
- **Slider Controls**: Smooth sliders for time limit and ply depth configuration

### How to Use the GUI
1. Launch the GUI: `python CheckersGUI.py` or `python CheckersGUI_Advanced.py`
2. Configure your game settings:
   - Choose AI strategy (Minimax, Alpha-Beta, or Alpha-Beta with Ordering)
   - Set time limit (1-3 seconds)
   - Set max plies (5-9 depth)
3. Click "Start New Game"
4. Play by clicking:
   - First click: Select your piece (white)
   - Second click: Select destination square
   - Legal moves are highlighted in gold
5. Watch the analytics update in real-time!

## 🎯 Extra Credit - Graphical Interface (10% Bonus)

This project includes **TWO** complete graphical interfaces that go above and beyond the requirements:

### 1. Standard GUI - Tkinter Implementation
- ✅ Beautiful, modern UI using Python Tkinter
- ✅ Full graphical board representation with custom-drawn pieces
- ✅ Interactive click-to-move gameplay
- ✅ Real-time analytics visualization
- ✅ Professional color scheme and layout
- ✅ Move history tracking
- ✅ No external dependencies beyond standard Python

### 2. Advanced GUI - Enhanced with Matplotlib
- ✅ Everything from Standard GUI
- ✅ **Four interactive analytics charts** showing:
  - Performance metrics over time
  - Comparative analysis
  - Real-time updates
- ✅ Tabbed interface for better organization
- ✅ Professional dark theme
- ✅ Enhanced user experience with sliders and visual feedback

Both implementations provide:
- **Appealing graphical interface** for the game board
- **Analytics generation and visualization** with charts and statistics
- **Modern UX design** with intuitive controls
- **Real-time feedback** and visual indicators

The GUIs make the project more accessible, visually appealing, and educational by allowing users to see how different AI strategies perform through interactive charts and real-time statistics.

## Notes

- The bot uses heuristic evaluation based on:
  - Piece count (kings worth 1.8x regular pieces)
  - Mobility (number of available moves)
  - Center control bonus
- Alpha-beta with ordering typically performs best
- Higher ply depth makes the bot stronger but slower
- The GUI versions make it much easier to understand the game flow and AI performance
- Charts in the advanced GUI help visualize algorithm efficiency

"# Checkers-AI" 
