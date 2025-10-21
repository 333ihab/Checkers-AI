# Checkers Bot - AI Mini Project

A Python implementation of a Checkers game with an AI bot that uses various search strategies to play against a human player.

## Features

- **Multiple Interfaces**: Choose between command-line or beautiful graphical interfaces
- **Three AI Strategies**: Minimax, Alpha-Beta Pruning, and Alpha-Beta with Ordering
- **Real-Time Analytics**: Track nodes expanded, generated, pruned, and time usage
- **Configurable Difficulty**: Adjust time limits (1-3s) and search depth (5-9 plies)
- **Full Checkers Rules**: King promotion, forced captures, and multiple jumps
- **Performance Charts**: Visual analytics with matplotlib (Advanced GUI)
- **Modern UI**: Beautiful dark theme with intuitive controls
- **Move History**: Track and review all moves during the game
- **Game Statistics**: Comprehensive analytics for both players

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
├── CheckersGUI_Advanced.py        # Advanced GUI (with matplotlib charts)
├── requirements_gui.txt           # Dependencies for Advanced GUI
└── README.md                      # This file (documentation)
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

### Graphical User Interface (GUI) - RECOMMENDED (+10% Bonus)

**Advanced GUI with Analytics Charts:**
```bash
python CheckersGUI_Advanced.py
```

**Features:**
- Beautiful, modern graphical board with enhanced 3D pieces
- Click-to-move interface (no typing coordinates!)
- **Interactive Analytics Charts** using matplotlib:
  - Nodes expanded per move (line chart)
  - Time per move (line chart)
  - Alpha-beta prunes per move (line chart)
  - Cumulative statistics comparison
- Tabbed interface (Game Board + Analytics Charts)
- Real-time chart updates after each move
- Quick stats cards with indicators
- Move history with color coding
- Easy configuration with sliders and radio buttons
- Visual king representation with detailed crowns
- Professional dark theme

**Installation:**
```bash
pip install matplotlib
# or
pip install -r requirements_gui.txt
```

### Command-Line Interface

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

### GUI Version
- **Advanced GUI** (`CheckersGUI_Advanced.py`): Python 3.7+ with Tkinter (included) + matplotlib
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

### Advanced GUI (CheckersGUI_Advanced.py)
The advanced GUI provides a professional, feature-rich interface:

**Game Board Tab:**
- **Interactive Board**: Click pieces to select, click destination to move
- **Enhanced Graphics**: 
  - 3D pieces with shadow effects and inner highlights
  - Detailed gold crowns with jewel decorations for kings
  - Orange = selected piece
  - Gold = legal move destinations with green borders
  - Brown-themed professional checkerboard pattern
- **Configuration Panel**: 
  - Slider controls for smooth time limit and ply depth adjustment
  - Radio buttons for strategy selection
  - Live value labels that update as you adjust settings
- **Quick Stats Cards**: Large cards showing:
  - Total Moves
  - Nodes Explored
  - Prunes (Agent)
  - Avg Time/Move
- **Move History**: Scrollable log of all moves with color coding
- **Last Move Details**: Shows nodes expanded, generated, prunes, and time for agent's last move

**Analytics Charts Tab:**
- **Real-Time Charts**: Four matplotlib charts showing:
  1. Nodes expanded per move (line chart)
  2. Time taken per move (line chart)
  3. Alpha-beta prunes per move (line chart)
  4. Cumulative statistics comparison (multi-line chart)
- **Professional Dark Theme**: Charts with dark backgrounds and accent colors
- **Animated Updates**: Charts refresh in real-time after each agent move
- **Visual Analysis**: Easily compare performance across different strategies

### How to Use the GUI
1. Launch the GUI: `python CheckersGUI_Advanced.py`
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

## Extra Credit - Graphical Interface (10% Bonus)

This project includes a **complete advanced graphical interface** that goes above and beyond the requirements:

### Advanced GUI - Tkinter + Matplotlib Implementation
- **Beautiful, modern UI** with professional brown/gold theme
- **Enhanced 3D graphics** with:
  - Shadow effects on pieces
  - Inner highlight circles for depth
  - Detailed gold crowns with jewel decorations for kings
  - Smooth gradient effects
- **Interactive click-to-move gameplay** with visual feedback
- **Four interactive analytics charts** using matplotlib:
  - Nodes expanded per move (real-time tracking)
  - Time per move (performance monitoring)
  - Alpha-beta prunes per move (efficiency analysis)
  - Cumulative statistics comparison (trend visualization)
- **Tabbed interface** for better organization (Game Board + Charts)
- **Quick stats dashboard** with indicator cards
- **Slider controls** with live value updates
- **Move history tracking** with color-coded entries
- **Real-time chart updates** after each agent move

The GUI provides:
- **Appealing graphical interface** for the game board with professional design
- **Analytics generation and visualization** with interactive charts and statistics
- **Modern UX design** with intuitive controls and visual feedback
- **Educational value** by allowing users to see how different AI strategies perform through visual data

The advanced GUI makes the project more accessible, visually appealing, and educational by transforming complex AI analytics into easy-to-understand visual representations.

## Notes

- The bot uses heuristic evaluation based on:
  - Piece count (kings worth 1.8x regular pieces)
  - Mobility (number of available moves)
  - Center control bonus
- Alpha-beta with ordering typically performs best
- Higher ply depth makes the bot stronger but slower
- The advanced GUI makes it much easier to understand the game flow and AI performance
- Interactive charts help visualize algorithm efficiency and compare strategies

"# Checkers-AI" 
