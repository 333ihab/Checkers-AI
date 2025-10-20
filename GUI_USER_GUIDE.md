# Checkers Bot GUI - User Guide

This guide will help you get the most out of the graphical interfaces for the Checkers Bot AI project.

## Table of Contents
1. [Installation](#installation)
2. [Choosing the Right GUI](#choosing-the-right-gui)
3. [Getting Started](#getting-started)
4. [Playing the Game](#playing-the-game)
5. [Understanding Analytics](#understanding-analytics)
6. [Tips and Tricks](#tips-and-tricks)
7. [Troubleshooting](#troubleshooting)

## Installation

### Standard GUI (Recommended for most users)
No additional installation needed! Just run:
```bash
python CheckersGUI.py
```

The standard GUI uses Tkinter, which comes bundled with Python by default.

### Advanced GUI (For data enthusiasts)
Requires matplotlib for charts:
```bash
pip install matplotlib
# Then run:
python CheckersGUI_Advanced.py
```

Or use the requirements file:
```bash
pip install -r requirements_gui.txt
python CheckersGUI_Advanced.py
```

## Choosing the Right GUI

### Use **Standard GUI** (`CheckersGUI.py`) if you:
- ✅ Want a quick, no-setup experience
- ✅ Prefer a cleaner, simpler interface
- ✅ Don't need detailed performance charts
- ✅ Want to avoid installing dependencies

### Use **Advanced GUI** (`CheckersGUI_Advanced.py`) if you:
- ✅ Want to analyze AI performance with charts
- ✅ Are interested in visualizing search algorithms
- ✅ Need comparative analysis across moves
- ✅ Want the most feature-rich experience

## Getting Started

### 1. Launch the Application
```bash
# For Standard GUI:
python CheckersGUI.py

# For Advanced GUI:
python CheckersGUI_Advanced.py
```

### 2. Configure Your Game

Before starting a game, you'll see the configuration panel on the left:

#### **AI Strategy** (Choose one)
- 🔍 **Minimax**: Classic minimax algorithm without optimizations
  - Good for: Understanding basic game tree search
  - Performance: Slowest, explores all nodes
  
- ✂️ **Alpha-Beta**: Minimax with alpha-beta pruning
  - Good for: Faster search with pruning
  - Performance: Much faster than basic minimax
  
- 🎯 **Alpha-Beta + Ordering** (Recommended)
  - Good for: Best performance, most intelligent play
  - Performance: Fastest due to move ordering + pruning

#### **Time Limit** (1-3 seconds)
- Controls how long the AI can think per move
- Lower values = faster games but potentially weaker play
- Higher values = slower games but stronger AI decisions
- **Recommended**: 2.0 seconds (good balance)

#### **Search Depth** (5-9 plies)
- Controls how many moves ahead the AI looks
- Lower values = faster but less strategic
- Higher values = slower but more strategic
- **Recommended**: 6 plies (good balance)
- Note: Higher depths with longer time limits make the AI very strong!

### 3. Start Playing

Click the big **"🎮 START NEW GAME"** button to begin!

## Playing the Game

### Game Rules Quick Reference

#### Objective
Capture all of your opponent's pieces or block them from moving.

#### Pieces
- **White (⚪)**: You control these pieces
- **Black (⚫)**: The AI controls these pieces
- **Kings (👑)**: Pieces that reach the opposite end get crowned

#### Movement
1. **Regular pieces** move diagonally forward
2. **Kings** move diagonally in any direction (forward or backward)
3. **Captures are mandatory** - if you can jump, you must!
4. **Multiple jumps** are allowed in a single turn

### How to Make a Move

#### Step 1: Select Your Piece
- Click on any of your white pieces
- The selected piece's square will turn **orange**
- Legal move destinations will turn **gold/yellow**

#### Step 2: Choose Destination
- Click on any highlighted gold square
- Your piece will move there
- If it's a capture, the opponent's piece disappears

#### Visual Indicators
- 🟧 **Orange Square**: Currently selected piece
- 🟨 **Gold Square**: Legal move destination
- 🟫 **Brown Square**: Dark checkerboard square
- 🟪 **Tan Square**: Light checkerboard square

### Game Flow
1. You (White) always move first
2. After your move, the AI thinks (status shows "Agent is thinking...")
3. The AI makes its move
4. Your turn again
5. Repeat until someone wins!

### Winning
- You win if the AI has no pieces left
- AI wins if you have no pieces left
- A winner notification will appear with final statistics

## Understanding Analytics

### Standard GUI - Analytics Dashboard

#### Per-Move Analytics (Last Agent Move)
Shows details about the AI's most recent move:
- **Nodes Expanded**: Number of game states evaluated
- **Nodes Generated**: Total number of possible moves considered
- **Alpha-Beta Prunes**: Number of branches pruned (skipped) by the algorithm
- **Time Used**: How long the AI took to decide (in seconds)

💡 **What this means**: 
- More nodes expanded = deeper/thorough search
- More prunes = more efficient algorithm (Alpha-Beta variants)
- Less time = faster decision making

#### Cumulative Statistics
Tracks totals for the entire game:

**⚪ White (You)**
- Moves: Total number of moves you've made
- (No search analytics for human players)

**⚫ Black (Agent)**
- Moves: Total number of AI moves
- Nodes Expanded: Sum of all nodes explored
- Nodes Generated: Sum of all possible moves considered
- Prunes: Total number of branches pruned

#### Move History
A scrollable log showing:
- ⚪ **White moves**: Displayed in white text
- ⚫ **Black moves**: Displayed in yellow text
- 📊 **Analytics**: Displayed in blue text
- Each move shows: starting position → destination position

### Advanced GUI - Additional Features

#### Quick Stats Cards
Four large cards showing key metrics at a glance:
- 🎯 **Total Moves**: Combined moves from both players
- 🔍 **Nodes Explored**: Total nodes the AI has evaluated
- ✂️ **Prunes (Agent)**: Total pruning efficiency
- ⏱️ **Avg Time/Move**: Average time per AI move

#### Analytics Charts Tab
Click the "📊 Analytics Charts" tab to see:

1. **Nodes Expanded per Move** (Top-Left)
   - Line chart showing node exploration for each AI move
   - Higher peaks = AI had to think harder (complex position)
   - Useful for seeing which moves were computationally expensive

2. **Time per Move** (Top-Right)
   - Shows how long each AI move took
   - Helps identify when the AI approached the time limit
   - Useful for performance tuning

3. **Alpha-Beta Prunes per Move** (Bottom-Left)
   - Shows pruning efficiency for each move
   - Higher values = more efficient search
   - Only relevant for Alpha-Beta strategies

4. **Cumulative Statistics** (Bottom-Right)
   - Shows running totals over time
   - Two lines: total nodes (blue) and total prunes (gold)
   - Helps understand overall algorithm efficiency

💡 **Interpreting Charts**:
- Steep increases = difficult positions requiring more computation
- Flat sections = straightforward positions
- Compare prunes to nodes to see pruning efficiency

## Tips and Tricks

### Gameplay Tips
1. **Control the center** - Pieces in the center have more mobility
2. **Protect your back row** - Prevents easy king promotions
3. **Think ahead** - Consider what the AI might do next
4. **Kings are powerful** - Try to get pieces promoted to kings
5. **Force captures** - Set up situations where the AI must jump

### Strategy Testing
1. **Compare strategies** - Play multiple games with different AI strategies
2. **Adjust difficulty** - Increase plies for harder opponents
3. **Time analysis** - Check if the AI uses its full time allocation
4. **Watch the analytics** - Learn when the AI finds positions difficult

### Performance Optimization
1. **Lower settings for speed**: Use ply=5 and time=1.0 for quick games
2. **Higher settings for challenge**: Use ply=9 and time=3.0 for tough games
3. **Alpha-Beta + Ordering**: Almost always the best choice
4. **Monitor node counts**: High node counts might indicate you need to lower the ply depth

### Learning from Analytics
1. **Opening moves**: Note how many nodes the AI explores early
2. **Mid-game complexity**: Watch for spikes in node counts
3. **Endgame**: Usually fewer nodes (fewer pieces = simpler)
4. **Pruning effectiveness**: Alpha-Beta should show significant prunes

## Troubleshooting

### GUI Won't Launch

**Problem**: Double-clicking doesn't work
```bash
# Solution: Run from terminal/command prompt
python CheckersGUI.py
```

**Problem**: "tkinter not found"
```bash
# Solution: Install tkinter (varies by OS)
# Ubuntu/Debian:
sudo apt-get install python3-tk
# Fedora:
sudo dnf install python3-tkinter
# macOS: Usually included with Python
# Windows: Usually included with Python
```

**Problem**: "matplotlib not found" (Advanced GUI only)
```bash
# Solution: Install matplotlib
pip install matplotlib
```

### Game Issues

**Problem**: Can't select a piece
- **Solution**: Make sure it's your turn (White moves first)
- **Solution**: Click directly on a white piece (not empty square)

**Problem**: Can't move to a square
- **Solution**: Only gold-highlighted squares are legal moves
- **Solution**: You must capture if a capture is available (forced-capture rule)

**Problem**: Move was rejected
- **Solution**: Check the move history for the error
- **Solution**: Remember captures are mandatory

**Problem**: AI takes too long
- **Solution**: Reduce time limit or max plies
- **Solution**: Use Alpha-Beta + Ordering for fastest performance

### Display Issues

**Problem**: Board looks wrong or pieces overlap
- **Solution**: Resize the window and restart the game
- **Solution**: Check your display scaling settings

**Problem**: Colors are hard to see
- **Solution**: Try the other GUI version (different color schemes)
- **Solution**: Adjust monitor brightness/contrast

**Problem**: Charts don't update (Advanced GUI)
- **Solution**: Switch to the Analytics Charts tab to refresh
- **Solution**: Make sure matplotlib is installed correctly

## Keyboard Shortcuts

- **Alt+F4** (Windows) / **Cmd+Q** (Mac): Quit the application
- **Tab**: Navigate between UI elements
- No keyboard shortcuts for moves (GUI uses mouse/click only)

## Advanced Features

### Analyzing Game Complexity
Use the analytics to understand game complexity:
- **Simple positions**: Low node counts (< 1000)
- **Medium positions**: Moderate node counts (1000-10000)
- **Complex positions**: High node counts (> 10000)

### Comparing Strategies
1. Play a game with Minimax, note the node counts
2. Play another game with Alpha-Beta, compare the node counts
3. Play with Alpha-Beta + Ordering, see the improvement
4. Review the charts to visualize the differences

### Educational Use
- **For Students**: Watch how pruning reduces search space
- **For Teachers**: Demonstrate algorithm efficiency visually
- **For Researchers**: Collect data on heuristic performance

## Additional Resources

- **README.md**: Full project documentation
- **PlayingTheGame.py**: Command-line version for comparison
- **Source Code**: All GUI code is well-commented for learning

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Review the README.md file
3. Ensure all files are in the correct directory structure
4. Verify Python version (3.7+)
5. Check that all dependencies are installed

## Conclusion

The Checkers Bot GUI makes it easy and fun to play against an AI opponent while learning about search algorithms. Whether you use the Standard or Advanced GUI, you'll gain insights into how AI makes decisions!

**Enjoy playing! 🎮👑**

