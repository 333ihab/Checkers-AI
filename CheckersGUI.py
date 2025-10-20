"""
CheckersGUI - Graphical Interface for Checkers Bot

A beautiful Tkinter-based GUI for playing Checkers against an AI bot,
with real-time analytics visualization and game statistics.

Features:
- Interactive board with click-to-move functionality
- Visual representation of pieces (regular and kings)
- Real-time analytics dashboard
- Strategy configuration
- Move history tracking
- Beautiful modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from GameBoard.board import GameBoard
from SearchToolBox.search import SearchToolBox
from OtherStuff import OtherStuff


class CheckersGUI:
    """
    Main GUI class for the Checkers game.
    
    Provides interactive board, analytics display, and game management.
    """
    
    # Color scheme - modern and appealing
    COLORS = {
        'dark_square': '#8B4513',
        'light_square': '#DEB887',
        'highlight': '#FFD700',
        'selected': '#FFA500',
        'white_piece': '#FFFFFF',
        'black_piece': '#000000',
        'king_crown': '#FFD700',
        'bg_main': '#2C3E50',
        'bg_panel': '#34495E',
        'text_light': '#ECF0F1',
        'text_accent': '#3498DB',
        'success': '#2ECC71',
        'warning': '#E74C3C'
    }
    
    SQUARE_SIZE = 70
    PIECE_RADIUS = 28
    CROWN_SIZE = 12
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Checkers Bot - AI Mini Project")
        self.root.configure(bg=self.COLORS['bg_main'])
        
        # Game state
        self.board = None
        self.search_agent = None
        self.selected_square = None
        self.legal_moves = []
        self.game_active = False
        
        # Analytics tracking
        self.cumulative_analytics = {
            'w': {'NodesExpanded': 0, 'NodesGenerated': 0, 'AlphaBetaPrunes': 0, 'Moves': 0},
            'b': {'NodesExpanded': 0, 'NodesGenerated': 0, 'AlphaBetaPrunes': 0, 'Moves': 0}
        }
        self.move_history = []
        
        # Build the UI
        self._build_ui()
        
    def _build_ui(self):
        """Build the complete user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg_main'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side: Configuration and Analytics
        left_panel = tk.Frame(main_frame, bg=self.COLORS['bg_panel'], relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
        
        # Build configuration panel
        self._build_config_panel(left_panel)
        
        # Build analytics panel
        self._build_analytics_panel(left_panel)
        
        # Center: Game board
        board_frame = tk.Frame(main_frame, bg=self.COLORS['bg_main'])
        board_frame.pack(side=tk.LEFT, padx=10)
        
        # Title
        title_label = tk.Label(board_frame, text="Checkers Bot", 
                               font=('Arial', 24, 'bold'),
                               fg=self.COLORS['text_light'],
                               bg=self.COLORS['bg_main'])
        title_label.pack(pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(board_frame, text="Configure and start game", 
                                     font=('Arial', 14),
                                     fg=self.COLORS['text_accent'],
                                     bg=self.COLORS['bg_main'])
        self.status_label.pack(pady=(0, 10))
        
        # Canvas for the board
        canvas_size = self.SQUARE_SIZE * 8
        self.canvas = tk.Canvas(board_frame, width=canvas_size, height=canvas_size,
                               bg=self.COLORS['bg_main'], highlightthickness=2,
                               highlightbackground=self.COLORS['text_light'])
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self._on_square_click)
        
        # Coordinate labels
        coord_frame = tk.Frame(board_frame, bg=self.COLORS['bg_main'])
        coord_frame.pack(pady=(5, 0))
        tk.Label(coord_frame, text="Columns: 0-7 (left to right) | Rows: 0-7 (top to bottom)",
                font=('Arial', 9), fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_main']).pack()
        
        # Right side: Move history and additional info
        right_panel = tk.Frame(main_frame, bg=self.COLORS['bg_panel'], relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))
        
        self._build_history_panel(right_panel)
        
    def _build_config_panel(self, parent):
        """Build the configuration panel."""
        config_frame = tk.LabelFrame(parent, text="⚙ Configuration", 
                                     font=('Arial', 12, 'bold'),
                                     fg=self.COLORS['text_light'],
                                     bg=self.COLORS['bg_panel'],
                                     relief=tk.GROOVE, bd=2)
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Strategy selection
        tk.Label(config_frame, text="Search Strategy:", 
                font=('Arial', 10, 'bold'),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_panel']).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        self.strategy_var = tk.StringVar(value="AlphaBetaOrdering")
        strategies = [
            ("Minimax", "Minimax"),
            ("Alpha-Beta", "AlphaBeta"),
            ("Alpha-Beta + Ordering", "AlphaBetaOrdering")
        ]
        
        for i, (text, value) in enumerate(strategies):
            tk.Radiobutton(config_frame, text=text, variable=self.strategy_var,
                          value=value, font=('Arial', 9),
                          fg=self.COLORS['text_light'],
                          bg=self.COLORS['bg_panel'],
                          selectcolor=self.COLORS['bg_main']).grid(row=i+1, column=0, 
                                                                    sticky='w', padx=20, pady=2)
        
        # Time limit
        tk.Label(config_frame, text="Time Limit (1-3s):", 
                font=('Arial', 10, 'bold'),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_panel']).grid(row=4, column=0, sticky='w', padx=10, pady=5)
        
        self.time_var = tk.DoubleVar(value=2.0)
        time_spinbox = tk.Spinbox(config_frame, from_=1.0, to=3.0, increment=0.5,
                                 textvariable=self.time_var, width=10,
                                 font=('Arial', 10))
        time_spinbox.grid(row=5, column=0, padx=20, pady=2, sticky='w')
        
        # Max plies
        tk.Label(config_frame, text="Max Plies (5-9):", 
                font=('Arial', 10, 'bold'),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_panel']).grid(row=6, column=0, sticky='w', padx=10, pady=5)
        
        self.ply_var = tk.IntVar(value=6)
        ply_spinbox = tk.Spinbox(config_frame, from_=5, to=9, increment=1,
                                textvariable=self.ply_var, width=10,
                                font=('Arial', 10))
        ply_spinbox.grid(row=7, column=0, padx=20, pady=2, sticky='w')
        
        # Start button
        self.start_button = tk.Button(config_frame, text="🎮 Start New Game",
                                      command=self._start_new_game,
                                      font=('Arial', 11, 'bold'),
                                      bg=self.COLORS['success'],
                                      fg='white',
                                      relief=tk.RAISED,
                                      bd=3,
                                      cursor='hand2')
        self.start_button.grid(row=8, column=0, padx=10, pady=15, sticky='ew')
        
    def _build_analytics_panel(self, parent):
        """Build the analytics display panel."""
        analytics_frame = tk.LabelFrame(parent, text="📊 Analytics Dashboard", 
                                       font=('Arial', 12, 'bold'),
                                       fg=self.COLORS['text_light'],
                                       bg=self.COLORS['bg_panel'],
                                       relief=tk.GROOVE, bd=2)
        analytics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Per-move analytics
        move_frame = tk.LabelFrame(analytics_frame, text="Last Move (Agent)", 
                                   font=('Arial', 10, 'bold'),
                                   fg=self.COLORS['text_accent'],
                                   bg=self.COLORS['bg_panel'])
        move_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.last_move_labels = {}
        metrics = [
            ('Nodes Expanded', 'expanded'),
            ('Nodes Generated', 'generated'),
            ('Alpha-Beta Prunes', 'prunes'),
            ('Time Used', 'time')
        ]
        
        for i, (label, key) in enumerate(metrics):
            tk.Label(move_frame, text=f"{label}:", 
                    font=('Arial', 9),
                    fg=self.COLORS['text_light'],
                    bg=self.COLORS['bg_panel']).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            value_label = tk.Label(move_frame, text="0", 
                                  font=('Arial', 9, 'bold'),
                                  fg=self.COLORS['king_crown'],
                                  bg=self.COLORS['bg_panel'])
            value_label.grid(row=i, column=1, sticky='e', padx=5, pady=2)
            self.last_move_labels[key] = value_label
        
        # Cumulative analytics
        cum_frame = tk.LabelFrame(analytics_frame, text="Cumulative Statistics", 
                                 font=('Arial', 10, 'bold'),
                                 fg=self.COLORS['text_accent'],
                                 bg=self.COLORS['bg_panel'])
        cum_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # White (Human) stats
        white_frame = tk.Frame(cum_frame, bg=self.COLORS['bg_panel'])
        white_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(white_frame, text="⚪ White (You)", 
                font=('Arial', 10, 'bold'),
                fg='white',
                bg=self.COLORS['bg_panel']).pack()
        
        self.white_stats_labels = {}
        for metric in ['Moves', 'Nodes Expanded', 'Nodes Generated', 'Prunes']:
            frame = tk.Frame(white_frame, bg=self.COLORS['bg_panel'])
            frame.pack(fill=tk.X, padx=10)
            tk.Label(frame, text=f"{metric}:", 
                    font=('Arial', 9),
                    fg=self.COLORS['text_light'],
                    bg=self.COLORS['bg_panel']).pack(side=tk.LEFT)
            label = tk.Label(frame, text="0", 
                           font=('Arial', 9, 'bold'),
                           fg=self.COLORS['king_crown'],
                           bg=self.COLORS['bg_panel'])
            label.pack(side=tk.RIGHT)
            self.white_stats_labels[metric] = label
        
        # Separator
        tk.Frame(cum_frame, height=2, bg=self.COLORS['text_light']).pack(fill=tk.X, pady=5)
        
        # Black (Agent) stats
        black_frame = tk.Frame(cum_frame, bg=self.COLORS['bg_panel'])
        black_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(black_frame, text="⚫ Black (Agent)", 
                font=('Arial', 10, 'bold'),
                fg='black',
                bg=self.COLORS['text_light']).pack()
        
        self.black_stats_labels = {}
        for metric in ['Moves', 'Nodes Expanded', 'Nodes Generated', 'Prunes']:
            frame = tk.Frame(black_frame, bg=self.COLORS['bg_panel'])
            frame.pack(fill=tk.X, padx=10)
            tk.Label(frame, text=f"{metric}:", 
                    font=('Arial', 9),
                    fg=self.COLORS['text_light'],
                    bg=self.COLORS['bg_panel']).pack(side=tk.LEFT)
            label = tk.Label(frame, text="0", 
                           font=('Arial', 9, 'bold'),
                           fg=self.COLORS['king_crown'],
                           bg=self.COLORS['bg_panel'])
            label.pack(side=tk.RIGHT)
            self.black_stats_labels[metric] = label
        
    def _build_history_panel(self, parent):
        """Build the move history panel."""
        history_frame = tk.LabelFrame(parent, text="📜 Move History", 
                                     font=('Arial', 12, 'bold'),
                                     fg=self.COLORS['text_light'],
                                     bg=self.COLORS['bg_panel'],
                                     relief=tk.GROOVE, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable text widget
        scroll_frame = tk.Frame(history_frame, bg=self.COLORS['bg_panel'])
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(scroll_frame, width=30, height=35,
                                   font=('Consolas', 9),
                                   bg=self.COLORS['bg_main'],
                                   fg=self.COLORS['text_light'],
                                   yscrollcommand=scrollbar.set,
                                   wrap=tk.WORD,
                                   state=tk.DISABLED)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Configure tags for colored text
        self.history_text.tag_config('white', foreground='white', font=('Consolas', 9, 'bold'))
        self.history_text.tag_config('black', foreground='yellow', font=('Consolas', 9, 'bold'))
        self.history_text.tag_config('analytics', foreground='#3498DB', font=('Consolas', 8))
        
    def _start_new_game(self):
        """Start a new game with current configuration."""
        strategy = self.strategy_var.get()
        time_limit = self.time_var.get()
        max_ply = self.ply_var.get()
        
        # Initialize game
        self.board = GameBoard()
        self.search_agent = SearchToolBox(Strategy=strategy, TimeLimit=time_limit, MaxPly=max_ply)
        self.selected_square = None
        self.legal_moves = []
        self.game_active = True
        
        # Reset analytics
        self.cumulative_analytics = {
            'w': {'NodesExpanded': 0, 'NodesGenerated': 0, 'AlphaBetaPrunes': 0, 'Moves': 0},
            'b': {'NodesExpanded': 0, 'NodesGenerated': 0, 'AlphaBetaPrunes': 0, 'Moves': 0}
        }
        self.move_history = []
        
        # Clear history display
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        # Update status
        self.status_label.config(text="Your turn (White)", fg=self.COLORS['success'])
        
        # Add game start to history
        self._add_history_message(f"=== Game Started ===\nStrategy: {strategy}\n"
                                f"Time Limit: {time_limit}s\nMax Plies: {max_ply}\n", 'analytics')
        
        # Draw board
        self._draw_board()
        
        # Update analytics
        self._update_analytics_display()
        
        messagebox.showinfo("Game Started", 
                           f"New game started!\n\n"
                           f"You are White (⚪)\n"
                           f"Agent is Black (⚫)\n\n"
                           f"Click a piece to select it,\n"
                           f"then click destination square.")
        
    def _draw_board(self):
        """Draw the current board state on the canvas."""
        self.canvas.delete('all')
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                # Determine square color
                if (row + col) % 2 == 0:
                    color = self.COLORS['light_square']
                else:
                    color = self.COLORS['dark_square']
                
                # Highlight selected square
                if self.selected_square == (row, col):
                    color = self.COLORS['selected']
                
                # Highlight legal move destinations
                for move in self.legal_moves:
                    if move['start'] == self.selected_square:
                        for target in move['sequence']:
                            if target == (row, col):
                                color = self.COLORS['highlight']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
                
                # Draw coordinate labels
                if col == 0:
                    self.canvas.create_text(x1 + 10, y1 + 10, text=str(row),
                                          font=('Arial', 8), fill='gray')
                if row == 7:
                    self.canvas.create_text(x2 - 10, y2 - 10, text=str(col),
                                          font=('Arial', 8), fill='gray')
        
        # Draw pieces
        if self.board:
            for row in range(8):
                for col in range(8):
                    piece = self.board.Board[row][col]
                    if piece:
                        self._draw_piece(row, col, piece)
        
    def _draw_piece(self, row, col, piece):
        """Draw a single piece on the board."""
        center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        center_y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        
        # Determine piece color
        if piece.lower() == 'w':
            color = self.COLORS['white_piece']
            outline = 'black'
        else:
            color = self.COLORS['black_piece']
            outline = 'white'
        
        # Draw piece circle
        self.canvas.create_oval(center_x - self.PIECE_RADIUS,
                               center_y - self.PIECE_RADIUS,
                               center_x + self.PIECE_RADIUS,
                               center_y + self.PIECE_RADIUS,
                               fill=color, outline=outline, width=2)
        
        # Draw crown for kings
        if piece.isupper():
            crown_size = self.CROWN_SIZE
            # Simple crown representation
            points = [
                center_x - crown_size, center_y + crown_size // 2,
                center_x - crown_size // 2, center_y - crown_size // 2,
                center_x, center_y + crown_size // 2,
                center_x + crown_size // 2, center_y - crown_size // 2,
                center_x + crown_size, center_y + crown_size // 2,
                center_x + crown_size, center_y + crown_size,
                center_x - crown_size, center_y + crown_size
            ]
            self.canvas.create_polygon(points, fill=self.COLORS['king_crown'], 
                                      outline='darkgoldenrod', width=1)
    
    def _on_square_click(self, event):
        """Handle mouse click on board square."""
        if not self.game_active or self.board.PlayerToMove != 'w':
            return
        
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        # If no square selected, try to select this square
        if self.selected_square is None:
            piece = self.board.Board[row][col]
            if piece and piece.lower() == 'w':
                self.selected_square = (row, col)
                self.legal_moves = self.board.GenerateLegalMoves('w')
                self._draw_board()
        else:
            # Try to make a move
            start_row, start_col = self.selected_square
            target_row, target_col = row, col
            
            # Attempt the move
            new_board = self.board.MakeMoveIfLegal((start_row, start_col), (target_row, target_col))
            
            if new_board is not None:
                # Valid move
                self.board = new_board
                self.cumulative_analytics['w']['Moves'] += 1
                
                # Add to history
                self._add_history_message(f"Move #{self.cumulative_analytics['w']['Moves']}: ", 'white')
                self._add_history_message(f"({start_row},{start_col}) → ({target_row},{target_col})\n", None)
                
                # Clear selection
                self.selected_square = None
                self.legal_moves = []
                
                # Check for game over
                winner = self.board.GoalTest()
                if winner:
                    self._game_over(winner)
                    return
                
                # Update display
                self._draw_board()
                self._update_analytics_display()
                self.status_label.config(text="Agent is thinking...", fg=self.COLORS['warning'])
                self.root.update()
                
                # Agent's turn
                self.root.after(500, self._agent_move)
            else:
                # Invalid move, try selecting a different piece
                piece = self.board.Board[row][col]
                if piece and piece.lower() == 'w':
                    self.selected_square = (row, col)
                    self.legal_moves = self.board.GenerateLegalMoves('w')
                else:
                    self.selected_square = None
                    self.legal_moves = []
                self._draw_board()
    
    def _agent_move(self):
        """Execute the agent's move."""
        if not self.game_active:
            return
        
        # Get agent's move
        chosen_move, analytics = self.search_agent.ChooseMove(self.board)
        
        if chosen_move is None:
            self._game_over('w')
            return
        
        # Apply move
        self.board = self.board.ApplyMove(chosen_move)
        
        # Update analytics
        self.cumulative_analytics['b']['NodesExpanded'] += analytics['NodesExpanded']
        self.cumulative_analytics['b']['NodesGenerated'] += analytics['NodesGenerated']
        self.cumulative_analytics['b']['AlphaBetaPrunes'] += analytics['AlphaBetaPrunes']
        self.cumulative_analytics['b']['Moves'] += 1
        
        # Update last move analytics
        self.last_move_labels['expanded'].config(text=str(analytics['NodesExpanded']))
        self.last_move_labels['generated'].config(text=str(analytics['NodesGenerated']))
        self.last_move_labels['prunes'].config(text=str(analytics['AlphaBetaPrunes']))
        self.last_move_labels['time'].config(text=f"{analytics['TimeUsed']:.3f}s")
        
        # Add to history
        self._add_history_message(f"Move #{self.cumulative_analytics['b']['Moves']}: ", 'black')
        start = chosen_move['start']
        seq = chosen_move['sequence'][-1]  # Final destination
        self._add_history_message(f"({start[0]},{start[1]}) → ({seq[0]},{seq[1]})\n", None)
        self._add_history_message(f"  Nodes: {analytics['NodesExpanded']} | "
                                f"Time: {analytics['TimeUsed']:.2f}s\n", 'analytics')
        
        # Check for game over
        winner = self.board.GoalTest()
        if winner:
            self._game_over(winner)
            return
        
        # Update display
        self._draw_board()
        self._update_analytics_display()
        self.status_label.config(text="Your turn (White)", fg=self.COLORS['success'])
    
    def _update_analytics_display(self):
        """Update the analytics labels."""
        # White stats
        w_data = self.cumulative_analytics['w']
        self.white_stats_labels['Moves'].config(text=str(w_data['Moves']))
        self.white_stats_labels['Nodes Expanded'].config(text=str(w_data['NodesExpanded']))
        self.white_stats_labels['Nodes Generated'].config(text=str(w_data['NodesGenerated']))
        self.white_stats_labels['Prunes'].config(text=str(w_data['AlphaBetaPrunes']))
        
        # Black stats
        b_data = self.cumulative_analytics['b']
        self.black_stats_labels['Moves'].config(text=str(b_data['Moves']))
        self.black_stats_labels['Nodes Expanded'].config(text=str(b_data['NodesExpanded']))
        self.black_stats_labels['Nodes Generated'].config(text=str(b_data['NodesGenerated']))
        self.black_stats_labels['Prunes'].config(text=str(b_data['AlphaBetaPrunes']))
    
    def _add_history_message(self, message, tag=None):
        """Add a message to the history panel."""
        self.history_text.config(state=tk.NORMAL)
        if tag:
            self.history_text.insert(tk.END, message, tag)
        else:
            self.history_text.insert(tk.END, message)
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def _game_over(self, winner):
        """Handle game over."""
        self.game_active = False
        
        winner_text = "You (White)" if winner == 'w' else "Agent (Black)"
        self.status_label.config(text=f"Game Over! Winner: {winner_text}", 
                                fg=self.COLORS['king_crown'])
        
        # Add to history
        self._add_history_message(f"\n{'='*30}\n", None)
        self._add_history_message(f"GAME OVER!\n", 'analytics')
        self._add_history_message(f"Winner: {winner_text}\n", 
                                'white' if winner == 'w' else 'black')
        self._add_history_message(f"{'='*30}\n", None)
        
        # Show final statistics
        stats_msg = (
            f"\nFinal Statistics:\n"
            f"White - Moves: {self.cumulative_analytics['w']['Moves']}, "
            f"Nodes: {self.cumulative_analytics['w']['NodesExpanded']}\n"
            f"Black - Moves: {self.cumulative_analytics['b']['Moves']}, "
            f"Nodes: {self.cumulative_analytics['b']['NodesExpanded']}, "
            f"Prunes: {self.cumulative_analytics['b']['AlphaBetaPrunes']}"
        )
        
        messagebox.showinfo("Game Over", 
                           f"{winner_text} wins!\n\n{stats_msg}")


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    
    # Set window size and center it
    window_width = 1400
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Create the application
    app = CheckersGUI(root)
    
    # Run the main loop
    root.mainloop()


if __name__ == "__main__":
    main()

