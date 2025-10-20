"""
CheckersGUI Advanced - Enhanced Graphical Interface with Analytics Charts

An advanced Tkinter-based GUI for playing Checkers against an AI bot,
featuring real-time analytics visualization with matplotlib charts.

Features:
- Interactive board with click-to-move functionality
- Visual representation of pieces with animations
- Real-time analytics dashboard with charts
- Strategy configuration
- Move history tracking
- Performance graphs
- Beautiful modern UI with dark theme
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from GameBoard.board import GameBoard
from SearchToolBox.search import SearchToolBox
from OtherStuff import OtherStuff

try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Charts will be disabled.")


class CheckersGUIAdvanced:
    """
    Advanced GUI class for the Checkers game with analytics charts.
    
    Provides interactive board, real-time charts, and comprehensive game management.
    """
    
    # Color scheme - modern brown theme
    COLORS = {
        'dark_square': '#8B4513',
        'light_square': '#DEB887',
        'highlight': '#FFD700',
        'selected': '#FFA500',
        'white_piece': '#FFFFFF',
        'black_piece': '#000000',
        'king_crown': '#FFD700',
        'bg_main': '#5D4037',
        'bg_panel': '#6D4C41',
        'bg_card': '#8D6E63',
        'text_light': '#FFFFFF',
        'text_accent': '#00D9FF',
        'success': '#00E676',
        'warning': '#FF3D00',
        'chart_bg': '#2A2A3E',
        'chart_grid': '#404060'
    }
    
    SQUARE_SIZE = 70
    PIECE_RADIUS = 28
    CROWN_SIZE = 12
    
    def __init__(self, root):
        """Initialize the advanced GUI application."""
        self.root = root
        self.root.title("Checkers Bot Advanced - AI Mini Project")
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
        self.analytics_history = {
            'moves': [],
            'nodes_expanded': [],
            'time_per_move': [],
            'prunes': []
        }
        
        # Build the UI
        self._build_ui()
        
    def _build_ui(self):
        """Build the complete user interface."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.COLORS['bg_main'])
        style.configure('TNotebook.Tab', background=self.COLORS['bg_panel'], 
                       foreground=self.COLORS['text_light'], padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', self.COLORS['bg_card'])])
        
        # Tab 1: Game Board
        game_tab = tk.Frame(self.notebook, bg=self.COLORS['bg_main'])
        self.notebook.add(game_tab, text="🎮 Game Board")
        self._build_game_tab(game_tab)
        
        # Tab 2: Analytics Charts
        if MATPLOTLIB_AVAILABLE:
            analytics_tab = tk.Frame(self.notebook, bg=self.COLORS['bg_main'])
            self.notebook.add(analytics_tab, text="📊 Analytics Charts")
            self._build_analytics_tab(analytics_tab)
        
    def _build_game_tab(self, parent):
        """Build the game board tab."""
        main_frame = tk.Frame(parent, bg=self.COLORS['bg_main'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side: Configuration and Stats
        left_panel = tk.Frame(main_frame, bg=self.COLORS['bg_panel'], relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        self._build_config_panel(left_panel)
        self._build_quick_stats_panel(left_panel)
        
        # Center: Game board
        board_frame = tk.Frame(main_frame, bg=self.COLORS['bg_main'])
        board_frame.pack(side=tk.LEFT, padx=10)
        
        # Title with gradient effect
        title_frame = tk.Frame(board_frame, bg=self.COLORS['bg_main'])
        title_frame.pack(pady=(0, 10))
        
        tk.Label(title_frame, text="♔", font=('Arial', 32),
                fg=self.COLORS['king_crown'], bg=self.COLORS['bg_main']).pack(side=tk.LEFT, padx=5)
        tk.Label(title_frame, text="CHECKERS BOT", 
                font=('Arial', 24, 'bold'),
                fg=self.COLORS['text_accent'],
                bg=self.COLORS['bg_main']).pack(side=tk.LEFT)
        tk.Label(title_frame, text="♚", font=('Arial', 32),
                fg=self.COLORS['king_crown'], bg=self.COLORS['bg_main']).pack(side=tk.LEFT, padx=5)
        
        # Status label
        status_frame = tk.Frame(board_frame, bg=self.COLORS['bg_card'], relief=tk.RAISED, bd=2)
        status_frame.pack(pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, text="⚙️ Configure and start game", 
                                     font=('Arial', 12, 'bold'),
                                     fg=self.COLORS['text_accent'],
                                     bg=self.COLORS['bg_card'],
                                     padx=20, pady=10)
        self.status_label.pack()
        
        # Canvas for the board with border
        canvas_frame = tk.Frame(board_frame, bg=self.COLORS['king_crown'], bd=3, relief=tk.RAISED)
        canvas_frame.pack()
        
        canvas_size = self.SQUARE_SIZE * 8
        self.canvas = tk.Canvas(canvas_frame, width=canvas_size, height=canvas_size,
                               bg=self.COLORS['bg_main'], highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self._on_square_click)
        self.canvas.bind('<Motion>', self._on_mouse_motion)
        
        # Coordinate labels
        coord_frame = tk.Frame(board_frame, bg=self.COLORS['bg_main'])
        coord_frame.pack(pady=(5, 0))
        tk.Label(coord_frame, text="🎯 Click a piece, then click destination",
                font=('Arial', 10, 'italic'), fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_main']).pack()
        
        # Right side: Move history and details
        right_panel = tk.Frame(main_frame, bg=self.COLORS['bg_panel'], relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))
        
        self._build_history_panel(right_panel)
        self._build_last_move_details(right_panel)
        
    def _build_config_panel(self, parent):
        """Build the configuration panel."""
        config_frame = tk.LabelFrame(parent, text="⚙️ Game Configuration", 
                                     font=('Arial', 11, 'bold'),
                                     fg=self.COLORS['text_accent'],
                                     bg=self.COLORS['bg_panel'],
                                     relief=tk.GROOVE, bd=2)
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Strategy selection with radio buttons
        tk.Label(config_frame, text="AI Strategy:", 
                font=('Arial', 10, 'bold'),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_panel']).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        
        self.strategy_var = tk.StringVar(value="AlphaBetaOrdering")
        strategies = [
            ("🔍 Minimax", "Minimax"),
            ("✂️ Alpha-Beta", "AlphaBeta"),
            ("🎯 AB + Ordering (Best)", "AlphaBetaOrdering")
        ]
        
        for i, (text, value) in enumerate(strategies):
            rb = tk.Radiobutton(config_frame, text=text, variable=self.strategy_var,
                          value=value, font=('Arial', 9),
                          fg=self.COLORS['text_light'],
                          bg=self.COLORS['bg_panel'],
                          selectcolor=self.COLORS['bg_card'],
                          activebackground=self.COLORS['bg_panel'],
                          activeforeground=self.COLORS['text_accent'])
            rb.grid(row=i+1, column=0, sticky='w', padx=25, pady=3)
        
        # Time limit slider
        tk.Label(config_frame, text="⏱️ Time Limit:", 
                font=('Arial', 10, 'bold'),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_panel']).grid(row=4, column=0, sticky='w', padx=10, pady=(10, 5))
        
        self.time_var = tk.DoubleVar(value=2.0)
        time_frame = tk.Frame(config_frame, bg=self.COLORS['bg_panel'])
        time_frame.grid(row=5, column=0, padx=20, pady=5, sticky='ew')
        
        time_scale = tk.Scale(time_frame, from_=1.0, to=3.0, resolution=0.5,
                            variable=self.time_var, orient=tk.HORIZONTAL,
                            bg=self.COLORS['bg_card'], fg=self.COLORS['text_light'],
                            highlightthickness=0, length=180, width=15,
                            troughcolor=self.COLORS['bg_main'])
        time_scale.pack(side=tk.LEFT)
        
        self.time_label = tk.Label(time_frame, text="2.0s", 
                                   font=('Arial', 9, 'bold'),
                                   fg=self.COLORS['king_crown'],
                                   bg=self.COLORS['bg_panel'], width=5)
        self.time_label.pack(side=tk.LEFT, padx=5)
        self.time_var.trace('w', lambda *args: self.time_label.config(text=f"{self.time_var.get():.1f}s"))
        
        # Max plies slider
        tk.Label(config_frame, text="🎲 Search Depth:", 
                font=('Arial', 10, 'bold'),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_panel']).grid(row=6, column=0, sticky='w', padx=10, pady=(10, 5))
        
        self.ply_var = tk.IntVar(value=6)
        ply_frame = tk.Frame(config_frame, bg=self.COLORS['bg_panel'])
        ply_frame.grid(row=7, column=0, padx=20, pady=5, sticky='ew')
        
        ply_scale = tk.Scale(ply_frame, from_=5, to=9, resolution=1,
                           variable=self.ply_var, orient=tk.HORIZONTAL,
                           bg=self.COLORS['bg_card'], fg=self.COLORS['text_light'],
                           highlightthickness=0, length=180, width=15,
                           troughcolor=self.COLORS['bg_main'])
        ply_scale.pack(side=tk.LEFT)
        
        self.ply_label = tk.Label(ply_frame, text="6", 
                                 font=('Arial', 9, 'bold'),
                                 fg=self.COLORS['king_crown'],
                                 bg=self.COLORS['bg_panel'], width=5)
        self.ply_label.pack(side=tk.LEFT, padx=5)
        self.ply_var.trace('w', lambda *args: self.ply_label.config(text=str(self.ply_var.get())))
        
        # Start button with gradient effect
        button_frame = tk.Frame(config_frame, bg=self.COLORS['success'], bd=2, relief=tk.RAISED)
        button_frame.grid(row=8, column=0, padx=10, pady=15, sticky='ew')
        
        self.start_button = tk.Button(button_frame, text="🎮 START NEW GAME",
                                      command=self._start_new_game,
                                      font=('Arial', 11, 'bold'),
                                      bg=self.COLORS['success'],
                                      fg='white',
                                      relief=tk.FLAT,
                                      cursor='hand2',
                                      activebackground=self.COLORS['text_accent'],
                                      activeforeground='white',
                                      bd=0)
        self.start_button.pack(fill=tk.BOTH, padx=2, pady=2)
        
    def _build_quick_stats_panel(self, parent):
        """Build quick statistics panel."""
        stats_frame = tk.LabelFrame(parent, text="📈 Quick Stats", 
                                   font=('Arial', 11, 'bold'),
                                   fg=self.COLORS['text_accent'],
                                   bg=self.COLORS['bg_panel'],
                                   relief=tk.GROOVE, bd=2)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create stat cards
        self.stat_cards = {}
        stats = [
            ('Total Moves', 'moves', '🎯'),
            ('Nodes Explored', 'nodes', '🔍'),
            ('Prunes (Agent)', 'prunes', '✂️'),
            ('Avg Time/Move', 'time', '⏱️')
        ]
        
        for label, key, emoji in stats:
            card = tk.Frame(stats_frame, bg=self.COLORS['bg_card'], relief=tk.RAISED, bd=2)
            card.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(card, text=emoji, font=('Arial', 16),
                    bg=self.COLORS['bg_card'], fg=self.COLORS['king_crown']).pack(pady=(5, 0))
            
            tk.Label(card, text=label, font=('Arial', 9),
                    fg=self.COLORS['text_light'], bg=self.COLORS['bg_card']).pack()
            
            value_label = tk.Label(card, text="0", font=('Arial', 16, 'bold'),
                                  fg=self.COLORS['text_accent'], bg=self.COLORS['bg_card'])
            value_label.pack(pady=(0, 5))
            
            self.stat_cards[key] = value_label
        
    def _build_history_panel(self, parent):
        """Build the move history panel."""
        history_frame = tk.LabelFrame(parent, text="📜 Move History", 
                                     font=('Arial', 11, 'bold'),
                                     fg=self.COLORS['text_accent'],
                                     bg=self.COLORS['bg_panel'],
                                     relief=tk.GROOVE, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Scrollable text widget
        scroll_frame = tk.Frame(history_frame, bg=self.COLORS['bg_panel'])
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(scroll_frame, bg=self.COLORS['bg_card'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(scroll_frame, width=28, height=20,
                                   font=('Consolas', 9),
                                   bg=self.COLORS['bg_card'],
                                   fg=self.COLORS['text_light'],
                                   yscrollcommand=scrollbar.set,
                                   wrap=tk.WORD,
                                   state=tk.DISABLED,
                                   insertbackground=self.COLORS['text_accent'])
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Configure tags
        self.history_text.tag_config('white', foreground='white', font=('Consolas', 9, 'bold'))
        self.history_text.tag_config('black', foreground='#FFD700', font=('Consolas', 9, 'bold'))
        self.history_text.tag_config('analytics', foreground='#00D9FF', font=('Consolas', 8))
        self.history_text.tag_config('header', foreground='#00E676', font=('Consolas', 10, 'bold'))
        
    def _build_last_move_details(self, parent):
        """Build last move details panel."""
        details_frame = tk.LabelFrame(parent, text="🎯 Last Agent Move", 
                                     font=('Arial', 11, 'bold'),
                                     fg=self.COLORS['text_accent'],
                                     bg=self.COLORS['bg_panel'],
                                     relief=tk.GROOVE, bd=2)
        details_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        self.last_move_labels = {}
        metrics = [
            ('Expanded', 'expanded', '🔍'),
            ('Generated', 'generated', '🌳'),
            ('Prunes', 'prunes', '✂️'),
            ('Time', 'time', '⏱️')
        ]
        
        for i, (label, key, emoji) in enumerate(metrics):
            row = tk.Frame(details_frame, bg=self.COLORS['bg_card'])
            row.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(row, text=f"{emoji} {label}:", 
                    font=('Arial', 9),
                    fg=self.COLORS['text_light'],
                    bg=self.COLORS['bg_card']).pack(side=tk.LEFT, padx=5)
            
            value_label = tk.Label(row, text="0", 
                                  font=('Arial', 9, 'bold'),
                                  fg=self.COLORS['king_crown'],
                                  bg=self.COLORS['bg_card'])
            value_label.pack(side=tk.RIGHT, padx=5)
            self.last_move_labels[key] = value_label
        
    def _build_analytics_tab(self, parent):
        """Build the analytics charts tab."""
        if not MATPLOTLIB_AVAILABLE:
            tk.Label(parent, text="Matplotlib not available", 
                    font=('Arial', 14),
                    fg=self.COLORS['warning'],
                    bg=self.COLORS['bg_main']).pack(pady=50)
            return
        
        # Create figure with subplots
        self.fig = Figure(figsize=(12, 8), facecolor=self.COLORS['bg_main'])
        
        # Create 2x2 grid of subplots
        self.ax_nodes = self.fig.add_subplot(221, facecolor=self.COLORS['chart_bg'])
        self.ax_time = self.fig.add_subplot(222, facecolor=self.COLORS['chart_bg'])
        self.ax_prunes = self.fig.add_subplot(223, facecolor=self.COLORS['chart_bg'])
        self.ax_cumulative = self.fig.add_subplot(224, facecolor=self.COLORS['chart_bg'])
        
        # Style all subplots
        for ax in [self.ax_nodes, self.ax_time, self.ax_prunes, self.ax_cumulative]:
            ax.grid(True, alpha=0.3, color=self.COLORS['chart_grid'])
            ax.tick_params(colors=self.COLORS['text_light'])
            for spine in ax.spines.values():
                spine.set_color(self.COLORS['chart_grid'])
        
        self.fig.tight_layout(pad=3.0)
        
        # Embed in tkinter
        self.chart_canvas = FigureCanvasTkAgg(self.fig, parent)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial plot
        self._update_charts()
        
    def _update_charts(self):
        """Update all analytics charts."""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        if not self.analytics_history['moves']:
            return
        
        moves = self.analytics_history['moves']
        
        # Chart 1: Nodes Expanded per Move
        self.ax_nodes.clear()
        self.ax_nodes.plot(moves, self.analytics_history['nodes_expanded'], 
                          'o-', color='#00D9FF', linewidth=2, markersize=6, label='Nodes Expanded')
        self.ax_nodes.set_title('Nodes Expanded per Move', color=self.COLORS['text_light'], fontsize=12, fontweight='bold')
        self.ax_nodes.set_xlabel('Move Number', color=self.COLORS['text_light'])
        self.ax_nodes.set_ylabel('Nodes', color=self.COLORS['text_light'])
        self.ax_nodes.grid(True, alpha=0.3, color=self.COLORS['chart_grid'])
        self.ax_nodes.set_facecolor(self.COLORS['chart_bg'])
        
        # Chart 2: Time per Move
        self.ax_time.clear()
        self.ax_time.plot(moves, self.analytics_history['time_per_move'], 
                         's-', color='#00E676', linewidth=2, markersize=6, label='Time (s)')
        self.ax_time.set_title('Time per Move', color=self.COLORS['text_light'], fontsize=12, fontweight='bold')
        self.ax_time.set_xlabel('Move Number', color=self.COLORS['text_light'])
        self.ax_time.set_ylabel('Seconds', color=self.COLORS['text_light'])
        self.ax_time.grid(True, alpha=0.3, color=self.COLORS['chart_grid'])
        self.ax_time.set_facecolor(self.COLORS['chart_bg'])
        
        # Chart 3: Prunes per Move
        self.ax_prunes.clear()
        self.ax_prunes.plot(moves, self.analytics_history['prunes'], 
                           '^-', color='#FFD700', linewidth=2, markersize=6, label='Prunes')
        self.ax_prunes.set_title('Alpha-Beta Prunes per Move', color=self.COLORS['text_light'], fontsize=12, fontweight='bold')
        self.ax_prunes.set_xlabel('Move Number', color=self.COLORS['text_light'])
        self.ax_prunes.set_ylabel('Prunes', color=self.COLORS['text_light'])
        self.ax_prunes.grid(True, alpha=0.3, color=self.COLORS['chart_grid'])
        self.ax_prunes.set_facecolor(self.COLORS['chart_bg'])
        
        # Chart 4: Cumulative Comparison
        self.ax_cumulative.clear()
        move_nums = list(range(1, len(moves) + 1))
        cumulative_nodes = [sum(self.analytics_history['nodes_expanded'][:i+1]) for i in range(len(moves))]
        cumulative_prunes = [sum(self.analytics_history['prunes'][:i+1]) for i in range(len(moves))]
        
        self.ax_cumulative.plot(move_nums, cumulative_nodes, 'o-', 
                               color='#00D9FF', linewidth=2, markersize=5, label='Cumulative Nodes')
        self.ax_cumulative.plot(move_nums, cumulative_prunes, 's-', 
                               color='#FFD700', linewidth=2, markersize=5, label='Cumulative Prunes')
        self.ax_cumulative.set_title('Cumulative Statistics', color=self.COLORS['text_light'], fontsize=12, fontweight='bold')
        self.ax_cumulative.set_xlabel('Move Number', color=self.COLORS['text_light'])
        self.ax_cumulative.set_ylabel('Count', color=self.COLORS['text_light'])
        self.ax_cumulative.legend(facecolor=self.COLORS['bg_card'], edgecolor=self.COLORS['chart_grid'],
                                 labelcolor=self.COLORS['text_light'])
        self.ax_cumulative.grid(True, alpha=0.3, color=self.COLORS['chart_grid'])
        self.ax_cumulative.set_facecolor(self.COLORS['chart_bg'])
        
        # Apply styling to all axes
        for ax in [self.ax_nodes, self.ax_time, self.ax_prunes, self.ax_cumulative]:
            ax.tick_params(colors=self.COLORS['text_light'])
            for spine in ax.spines.values():
                spine.set_color(self.COLORS['chart_grid'])
        
        self.chart_canvas.draw()
        
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
        self.analytics_history = {
            'moves': [],
            'nodes_expanded': [],
            'time_per_move': [],
            'prunes': []
        }
        
        # Clear history display
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        # Update status
        self.status_label.config(text="⚪ Your Turn - White", fg=self.COLORS['success'])
        
        # Add game start to history
        self._add_history_message("=" * 35 + "\n", 'header')
        self._add_history_message("🎮 GAME STARTED\n", 'header')
        self._add_history_message("=" * 35 + "\n", 'header')
        self._add_history_message(f"Strategy: {strategy}\n", 'analytics')
        self._add_history_message(f"Time: {time_limit}s | Depth: {max_ply}\n\n", 'analytics')
        
        # Draw board
        self._draw_board()
        
        # Update stats
        self._update_quick_stats()
        
        # Update charts
        if MATPLOTLIB_AVAILABLE:
            self._update_charts()
        
        messagebox.showinfo("🎮 Game Started", 
                           f"New game started!\n\n"
                           f"⚪ You are White\n"
                           f"⚫ Agent is Black\n\n"
                           f"🎯 Click a piece to select\n"
                           f"🎯 Then click destination\n\n"
                           f"Strategy: {strategy}\n"
                           f"Time: {time_limit}s | Depth: {max_ply}")
        
    def _draw_board(self):
        """Draw the current board state with enhanced graphics."""
        self.canvas.delete('all')
        
        # Draw squares with shadow effect
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
                is_legal_dest = False
                for move in self.legal_moves:
                    if move['start'] == self.selected_square:
                        for target in move['sequence']:
                            if target == (row, col):
                                color = self.COLORS['highlight']
                                is_legal_dest = True
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
                
                # Add subtle border to legal destinations
                if is_legal_dest:
                    self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, 
                                                outline=self.COLORS['success'], width=3)
        
        # Draw pieces with enhanced graphics
        if self.board:
            for row in range(8):
                for col in range(8):
                    piece = self.board.Board[row][col]
                    if piece:
                        self._draw_piece_enhanced(row, col, piece)
        
    def _draw_piece_enhanced(self, row, col, piece):
        """Draw a piece with enhanced graphics including shadows."""
        center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        center_y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        
        # Determine piece color
        if piece.lower() == 'w':
            color = self.COLORS['white_piece']
            outline_color = '#333333'
            shadow_color = '#CCCCCC'
        else:
            color = self.COLORS['black_piece']
            outline_color = '#FFFFFF'
            shadow_color = '#333333'
        
        # Draw shadow
        self.canvas.create_oval(center_x - self.PIECE_RADIUS + 2,
                               center_y - self.PIECE_RADIUS + 2,
                               center_x + self.PIECE_RADIUS + 2,
                               center_y + self.PIECE_RADIUS + 2,
                               fill=shadow_color, outline='')
        
        # Draw piece with gradient effect
        self.canvas.create_oval(center_x - self.PIECE_RADIUS,
                               center_y - self.PIECE_RADIUS,
                               center_x + self.PIECE_RADIUS,
                               center_y + self.PIECE_RADIUS,
                               fill=color, outline=outline_color, width=3)
        
        # Draw inner circle for 3D effect
        inner_radius = self.PIECE_RADIUS - 6
        highlight_color = '#EFEFEF' if piece.lower() == 'w' else '#444444'
        self.canvas.create_oval(center_x - inner_radius,
                               center_y - inner_radius,
                               center_x + inner_radius,
                               center_y + inner_radius,
                               fill='', outline=highlight_color, width=2)
        
        # Draw crown for kings
        if piece.isupper():
            self._draw_crown(center_x, center_y)
    
    def _draw_crown(self, x, y):
        """Draw a detailed crown for king pieces."""
        size = self.CROWN_SIZE
        # Crown shape
        points = [
            x - size, y + size//2,
            x - size//2, y - size//2,
            x, y,
            x + size//2, y - size//2,
            x + size, y + size//2,
            x + size*0.8, y + size,
            x, y + size//2,
            x - size*0.8, y + size
        ]
        
        # Draw crown with gradient
        self.canvas.create_polygon(points, fill=self.COLORS['king_crown'], 
                                  outline='#DAA520', width=2)
        
        # Add jewel points
        for jewel_x in [x - size//2, x, x + size//2]:
            self.canvas.create_oval(jewel_x - 2, y - size//2 - 2,
                                   jewel_x + 2, y - size//2 + 2,
                                   fill='#FF6B6B', outline='#C92A2A')
    
    def _on_mouse_motion(self, event):
        """Handle mouse motion for hover effects."""
        # Could add hover effects here if desired
        pass
    
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
                move_num = self.cumulative_analytics['w']['Moves']
                self._add_history_message(f"Move {move_num}: ", 'white')
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
                self._update_quick_stats()
                self.status_label.config(text="⚫ Agent Thinking...", fg=self.COLORS['warning'])
                self.root.update()
                
                # Agent's turn
                self.root.after(300, self._agent_move)
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
        
        # Record analytics history
        self.analytics_history['moves'].append(self.cumulative_analytics['b']['Moves'])
        self.analytics_history['nodes_expanded'].append(analytics['NodesExpanded'])
        self.analytics_history['time_per_move'].append(analytics['TimeUsed'])
        self.analytics_history['prunes'].append(analytics['AlphaBetaPrunes'])
        
        # Update last move analytics
        self.last_move_labels['expanded'].config(text=f"{analytics['NodesExpanded']:,}")
        self.last_move_labels['generated'].config(text=f"{analytics['NodesGenerated']:,}")
        self.last_move_labels['prunes'].config(text=f"{analytics['AlphaBetaPrunes']:,}")
        self.last_move_labels['time'].config(text=f"{analytics['TimeUsed']:.3f}s")
        
        # Add to history
        move_num = self.cumulative_analytics['b']['Moves']
        self._add_history_message(f"Move {move_num}: ", 'black')
        start = chosen_move['start']
        seq = chosen_move['sequence'][-1]
        self._add_history_message(f"({start[0]},{start[1]}) → ({seq[0]},{seq[1]})\n", None)
        self._add_history_message(f"  N:{analytics['NodesExpanded']:,} | "
                                f"P:{analytics['AlphaBetaPrunes']:,} | "
                                f"T:{analytics['TimeUsed']:.2f}s\n", 'analytics')
        
        # Check for game over
        winner = self.board.GoalTest()
        if winner:
            self._game_over(winner)
            return
        
        # Update display
        self._draw_board()
        self._update_quick_stats()
        if MATPLOTLIB_AVAILABLE:
            self._update_charts()
        self.status_label.config(text="⚪ Your Turn - White", fg=self.COLORS['success'])
    
    def _update_quick_stats(self):
        """Update quick statistics display."""
        total_moves = self.cumulative_analytics['w']['Moves'] + self.cumulative_analytics['b']['Moves']
        total_nodes = self.cumulative_analytics['b']['NodesExpanded']
        total_prunes = self.cumulative_analytics['b']['AlphaBetaPrunes']
        
        self.stat_cards['moves'].config(text=str(total_moves))
        self.stat_cards['nodes'].config(text=f"{total_nodes:,}")
        self.stat_cards['prunes'].config(text=f"{total_prunes:,}")
        
        if self.cumulative_analytics['b']['Moves'] > 0:
            avg_time = sum(self.analytics_history['time_per_move']) / len(self.analytics_history['time_per_move'])
            self.stat_cards['time'].config(text=f"{avg_time:.2f}s")
        else:
            self.stat_cards['time'].config(text="0.00s")
    
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
        
        winner_text = "⚪ You (White)" if winner == 'w' else "⚫ Agent (Black)"
        winner_emoji = "🎉" if winner == 'w' else "🤖"
        self.status_label.config(text=f"{winner_emoji} GAME OVER - {winner_text} Wins!", 
                                fg=self.COLORS['king_crown'])
        
        # Add to history
        self._add_history_message(f"\n{'='*35}\n", 'header')
        self._add_history_message(f"🏆 GAME OVER! 🏆\n", 'header')
        self._add_history_message(f"Winner: {winner_text}\n", 
                                'white' if winner == 'w' else 'black')
        self._add_history_message(f"{'='*35}\n\n", 'header')
        
        # Final statistics
        w_data = self.cumulative_analytics['w']
        b_data = self.cumulative_analytics['b']
        
        stats_msg = (
            f"📊 Final Statistics:\n\n"
            f"⚪ White (You):\n"
            f"  Moves: {w_data['Moves']}\n\n"
            f"⚫ Black (Agent):\n"
            f"  Moves: {b_data['Moves']}\n"
            f"  Nodes Expanded: {b_data['NodesExpanded']:,}\n"
            f"  Nodes Generated: {b_data['NodesGenerated']:,}\n"
            f"  Alpha-Beta Prunes: {b_data['AlphaBetaPrunes']:,}\n"
        )
        
        if self.analytics_history['time_per_move']:
            avg_time = sum(self.analytics_history['time_per_move']) / len(self.analytics_history['time_per_move'])
            stats_msg += f"  Avg Time/Move: {avg_time:.3f}s\n"
        
        self._add_history_message("Final Statistics:\n", 'header')
        self._add_history_message(f"White: {w_data['Moves']} moves\n", 'white')
        self._add_history_message(f"Black: {b_data['Moves']} moves\n", 'black')
        self._add_history_message(f"Nodes: {b_data['NodesExpanded']:,} | "
                                f"Prunes: {b_data['AlphaBetaPrunes']:,}\n", 'analytics')
        
        messagebox.showinfo("🏆 Game Over", stats_msg)


def main():
    """Main entry point for the advanced GUI application."""
    root = tk.Tk()
    
    # Set window size and center it
    window_width = 1600
    window_height = 900
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Set minimum size
    root.minsize(1200, 700)
    
    # Create the application
    app = CheckersGUIAdvanced(root)
    
    # Run the main loop
    root.mainloop()


if __name__ == "__main__":
    main()

