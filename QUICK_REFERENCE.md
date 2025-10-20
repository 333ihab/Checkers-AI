# Checkers Bot GUI - Quick Reference Card

## 🚀 Quick Start

```bash
# Standard GUI (no dependencies)
python CheckersGUI.py

# Advanced GUI (requires matplotlib)
pip install matplotlib
python CheckersGUI_Advanced.py
```

## 🎮 How to Play

### 1. Configure Game
- **Strategy**: Minimax | Alpha-Beta | AB+Ordering ⭐
- **Time**: 1-3 seconds (default: 2s)
- **Depth**: 5-9 plies (default: 6)

### 2. Make Moves
1. **Click** your white piece
2. **Click** destination (gold squares)
3. Watch AI respond!

## 📊 Key Metrics

| Metric | Meaning |
|--------|---------|
| **Nodes Expanded** | Game states evaluated |
| **Nodes Generated** | Possible moves considered |
| **Alpha-Beta Prunes** | Branches skipped (efficiency) |
| **Time Used** | AI thinking time |

## 🎯 Visual Indicators

| Color | Meaning |
|-------|---------|
| 🟧 Orange | Selected piece |
| 🟨 Gold | Legal move |
| ⚪ White circle | Your pieces |
| ⚫ Black circle | AI pieces |
| 👑 Crown | King piece |

## 🏆 Game Rules

- ✅ **Moves**: Diagonal only
- ✅ **Kings**: Move forward/backward
- ✅ **Captures**: MANDATORY (forced-capture rule)
- ✅ **Multi-Jump**: Allowed in single turn
- ✅ **Win**: Capture all opponent pieces

## 💡 Strategy Tips

### Easy Game
- Time: 1.0s
- Depth: 5 plies
- Strategy: Minimax

### Medium Game
- Time: 2.0s ⭐
- Depth: 6 plies ⭐
- Strategy: Alpha-Beta

### Hard Game
- Time: 3.0s
- Depth: 9 plies
- Strategy: AB+Ordering ⭐

## 🔧 Troubleshooting

### Can't move?
- ✓ Is it your turn?
- ✓ Must capture if possible
- ✓ Click piece first, then destination

### AI too slow?
- ✓ Lower time limit
- ✓ Reduce depth
- ✓ Use AB+Ordering (fastest)

### GUI won't start?
```bash
# Check Tkinter
python -m tkinter

# Install matplotlib (Advanced only)
pip install matplotlib
```

## 📈 Understanding Charts (Advanced GUI)

**High Nodes** = Complex position, AI working hard
**High Prunes** = Efficient search, good algorithm
**Time Near Limit** = Challenging position

## 🎓 Learning Points

- Compare strategies using analytics
- Watch node counts decrease with pruning
- See how ordering improves efficiency
- Identify difficult game positions

## ⌨️ Keyboard Shortcuts

- **Alt+F4** / **Cmd+Q**: Quit
- **Tab**: Navigate UI

## 📚 Full Documentation

- `README.md` - Complete project documentation
- `GUI_USER_GUIDE.md` - Detailed GUI guide

---

**⭐ = Recommended Setting**

Enjoy! 🎮👑

