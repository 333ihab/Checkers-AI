"""
SearchToolBox Module

Implements the search strategies for the Checkers AI agent:
 - Minimax
 - Alpha-Beta pruning
 - Alpha-Beta with node ordering (heuristic ordering)

Also enforces time limit T and depth limit P.

Tracks analytics:
 - NodesExpanded: number of nodes visited/expanded
 - NodesGenerated: number of moves generated
 - AlphaBetaPrunes: count of cutoff occurrences
 - OrderingUsed: boolean indicating if ordering was used
 - OrderingEffectPrunesEstimate: estimated gain from ordering
"""

import time
import math
from typing import Tuple, Optional
from GameBoard.board import GameBoard


class SearchToolBox:
    """
    Implements the search strategies for the Checkers AI agent.
    
    Attributes:
        Strategy: Search strategy name ("Minimax", "AlphaBeta", "AlphaBetaOrdering")
        TimeLimit: Maximum time allowed per move in seconds
        MaxPly: Maximum depth to search in plies
        NodesExpanded: Counter for nodes expanded
        NodesGenerated: Counter for nodes generated
        AlphaBetaPrunes: Counter for alpha-beta cutoffs
        OrderingUsed: Boolean flag for node ordering
        TimeStart: Starting time of search
        TimeUp: Flag indicating if time limit exceeded
    """

    def __init__(self, Strategy: str = "AlphaBetaOrdering", TimeLimit: float = 2.0, MaxPly: int = 6):
        """
        Initialize the search toolbox with specified parameters.
        
        Args:
            Strategy: one of "Minimax", "AlphaBeta", "AlphaBetaOrdering"
            TimeLimit: seconds allowed per move (1 to 3 recommended)
            MaxPly: depth in plies (5 to 9 recommended)
        """
        self.Strategy = Strategy
        self.TimeLimit = TimeLimit
        self.MaxPly = MaxPly
        # analytics counters (reset per move)
        self.NodesExpanded = 0
        self.NodesGenerated = 0
        self.AlphaBetaPrunes = 0
        self.OrderingUsed = (Strategy == "AlphaBetaOrdering")
        self.TimeStart = None
        self.TimeUp = False

    def _TimeRemaining(self) -> bool:
        """
        Check if there is time remaining within the time limit.
        
        Returns:
            bool: True if time remaining, False otherwise
        """
        return (time.time() - self.TimeStart) < self.TimeLimit

    def ChooseMove(self, board: GameBoard) -> Tuple[dict, dict]:
        """
        Given a GameBoard where board.PlayerToMove is the agent's color ('b'), select best move.
        
        Args:
            board: Current game board state
            
        Returns:
            Tuple[dict, dict]: (chosen_move, analytics_dict)
                chosen_move: Dictionary containing move information
                analytics_dict: Reports nodes expanded/generated, prunes, time used, etc.
        """
        self.NodesExpanded = 0
        self.NodesGenerated = 0
        self.AlphaBetaPrunes = 0
        self.TimeStart = time.time()
        self.TimeUp = False

        player = board.PlayerToMove
        legal = board.GenerateLegalMoves(player)
        if not legal:
            return (None, self._CollectAnalytics(0.0))

        bestMove = None
        bestVal = -math.inf if player == 'b' else math.inf

        # For fairness, we will perform a depth-limited search to MaxPly using the selected strategy.
        # If time runs out we return best found so far.
        # Node ordering: compute utility of children then sort descending (for maximizing player)

        # Precompute move ordering if ordering is enabled
        child_list = legal.copy()
        if self.OrderingUsed:
            # Order by shallow evaluation after applying move (heuristic)
            scored_children = []
            for mv in child_list:
                succ = board.ApplyMove(mv)
                v = succ.EvaluateFor(player)
                scored_children.append((v, mv))
            # Sort descending since agent ('b') is maximizing black; but generalize: maximize for current player
            scored_children.sort(key=lambda x: x[0], reverse=True)
            child_list = [mv for (_, mv) in scored_children]

        # Search entry depending on Strategy
        if self.Strategy == "Minimax":
            for mv in child_list:
                self.NodesGenerated += 1
                succ = board.ApplyMove(mv)
                val = self._MinValue(succ, 1, player)
                if val is None:
                    break  # time up
                if val > bestVal:
                    bestVal = val
                    bestMove = mv
        elif self.Strategy == "AlphaBeta":
            alpha = -math.inf
            beta = math.inf
            for mv in child_list:
                self.NodesGenerated += 1
                succ = board.ApplyMove(mv)
                val = self._AlphaBetaMin(succ, 1, alpha, beta, player, use_ordering=False)
                if val is None:
                    break
                if val > bestVal:
                    bestVal = val
                    bestMove = mv
                alpha = max(alpha, bestVal)
        elif self.Strategy == "AlphaBetaOrdering":
            alpha = -math.inf
            beta = math.inf
            for mv in child_list:
                self.NodesGenerated += 1
                succ = board.ApplyMove(mv)
                val = self._AlphaBetaMin(succ, 1, alpha, beta, player, use_ordering=True)
                if val is None:
                    break
                if val > bestVal:
                    bestVal = val
                    bestMove = mv
                alpha = max(alpha, bestVal)
        else:
            raise ValueError("Unknown strategy: " + self.Strategy)

        time_used = time.time() - self.TimeStart
        analytics = self._CollectAnalytics(time_used)
        # Optionally compute ordering effect estimate at shallow depth to report "ordering gain"
        if self.OrderingUsed:
            ordering_gain_est = self._EstimateOrderingGain(board, player)
            analytics['OrderingGainEstimate'] = ordering_gain_est
        else:
            analytics['OrderingGainEstimate'] = 0

        return (bestMove, analytics)

    def _CollectAnalytics(self, time_used: float) -> dict:
        """
        Collect current analytics into dict for reporting.
        
        Args:
            time_used: Time taken for the move in seconds
            
        Returns:
            dict: Analytics dictionary
        """
        return {
            'NodesExpanded': self.NodesExpanded,
            'NodesGenerated': self.NodesGenerated,
            'AlphaBetaPrunes': self.AlphaBetaPrunes,
            'OrderingUsed': self.OrderingUsed,
            'TimeUsed': time_used,
            'MaxPly': self.MaxPly,
            'TimeLimit': self.TimeLimit
        }

    # -------------------------
    # Minimax helpers
    # -------------------------
    def _MinValue(self, board: GameBoard, depth: int, root_player: str) -> Optional[float]:
        """
        Min step of minimax. Returns None if time up.
        
        Args:
            board: Current board state
            depth: Current search depth
            root_player: Original player at root of search tree
            
        Returns:
            Optional[float]: Minimum value or None if time limit exceeded
        """
        if not self._TimeRemaining():
            self.TimeUp = True
            return None
        self.NodesExpanded += 1
        winner = board.GoalTest()
        if winner is not None:
            # Terminal utility: large positive if root_player wins
            return float('inf') if winner == root_player else float('-inf')
        if depth >= self.MaxPly:
            return board.EvaluateFor(root_player)
        v = math.inf
        moves = board.GenerateLegalMoves(board.PlayerToMove)
        self.NodesGenerated += len(moves)
        for mv in moves:
            succ = board.ApplyMove(mv)
            val = self._MaxValue(succ, depth + 1, root_player)
            if val is None:
                return None
            v = min(v, val)
        return v

    def _MaxValue(self, board: GameBoard, depth: int, root_player: str) -> Optional[float]:
        """
        Max step of minimax. Returns None if time up.
        
        Args:
            board: Current board state
            depth: Current search depth
            root_player: Original player at root of search tree
            
        Returns:
            Optional[float]: Maximum value or None if time limit exceeded
        """
        if not self._TimeRemaining():
            self.TimeUp = True
            return None
        self.NodesExpanded += 1
        winner = board.GoalTest()
        if winner is not None:
            return float('inf') if winner == root_player else float('-inf')
        if depth >= self.MaxPly:
            return board.EvaluateFor(root_player)
        v = -math.inf
        moves = board.GenerateLegalMoves(board.PlayerToMove)
        self.NodesGenerated += len(moves)
        for mv in moves:
            succ = board.ApplyMove(mv)
            val = self._MinValue(succ, depth + 1, root_player)
            if val is None:
                return None
            v = max(v, val)
        return v

    # -------------------------
    # Alpha-Beta helpers
    # -------------------------
    def _AlphaBetaMax(self, board: GameBoard, depth: int, alpha: float, beta: float,
                      root_player: str, use_ordering: bool) -> Optional[float]:
        """
        Alpha-beta maximizing node.
        
        Args:
            board: Current board state
            depth: Current search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            root_player: Original player at root of search tree
            use_ordering: Whether to use node ordering
            
        Returns:
            Optional[float]: Maximum value or None if time limit exceeded
        """
        if not self._TimeRemaining():
            self.TimeUp = True
            return None
        self.NodesExpanded += 1
        winner = board.GoalTest()
        if winner is not None:
            return float('inf') if winner == root_player else float('-inf')
        if depth >= self.MaxPly:
            return board.EvaluateFor(root_player)
        v = -math.inf
        moves = board.GenerateLegalMoves(board.PlayerToMove)
        self.NodesGenerated += len(moves)
        # optional ordering
        if use_ordering:
            scored = []
            for mv in moves:
                succ = board.ApplyMove(mv)
                scored.append((succ.EvaluateFor(root_player), mv))
            scored.sort(key=lambda x: x[0], reverse=True)
            moves = [mv for (_, mv) in scored]
        for mv in moves:
            succ = board.ApplyMove(mv)
            val = self._AlphaBetaMin(succ, depth + 1, alpha, beta, root_player, use_ordering)
            if val is None:
                return None
            v = max(v, val)
            if v >= beta:
                self.AlphaBetaPrunes += 1
                return v
            alpha = max(alpha, v)
        return v

    def _AlphaBetaMin(self, board: GameBoard, depth: int, alpha: float, beta: float,
                      root_player: str, use_ordering: bool) -> Optional[float]:
        """
        Alpha-beta minimizing node.
        
        Args:
            board: Current board state
            depth: Current search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            root_player: Original player at root of search tree
            use_ordering: Whether to use node ordering
            
        Returns:
            Optional[float]: Minimum value or None if time limit exceeded
        """
        if not self._TimeRemaining():
            self.TimeUp = True
            return None
        self.NodesExpanded += 1
        winner = board.GoalTest()
        if winner is not None:
            return float('inf') if winner == root_player else float('-inf')
        if depth >= self.MaxPly:
            return board.EvaluateFor(root_player)
        v = math.inf
        moves = board.GenerateLegalMoves(board.PlayerToMove)
        self.NodesGenerated += len(moves)
        if use_ordering:
            scored = []
            for mv in moves:
                succ = board.ApplyMove(mv)
                scored.append((succ.EvaluateFor(root_player), mv))
            # For minimizing node, order ascending to get cutoffs faster
            scored.sort(key=lambda x: x[0])
            moves = [mv for (_, mv) in scored]
        for mv in moves:
            succ = board.ApplyMove(mv)
            val = self._AlphaBetaMax(succ, depth + 1, alpha, beta, root_player, use_ordering)
            if val is None:
                return None
            v = min(v, val)
            if v <= alpha:
                self.AlphaBetaPrunes += 1
                return v
            beta = min(beta, v)
        return v

    # -------------------------
    # Ordering gain estimation
    # -------------------------
    def _EstimateOrderingGain(self, board: GameBoard, player: str) -> float:
        """
        Rough estimate of ordering gain (percentage of prunes reduced).
        We perform two shallow alpha-beta runs at depth min(2,MaxPly) with and without ordering,
        counting prunes. This is only an estimate and kept lightweight to avoid big time cost.
        
        Args:
            board: Current board state
            player: Player to evaluate for
            
        Returns:
            float: Percentage gain = (prunes_without - prunes_with)/max(1,prunes_without)
        """
        saved_TimeLimit = self.TimeLimit
        saved_MaxPly = self.MaxPly
        saved_strategy = self.Strategy

        # Run without ordering
        self.TimeLimit = min(0.5, saved_TimeLimit)  # small budget
        self.MaxPly = min(2, saved_MaxPly)
        self.AlphaBetaPrunes = 0
        self.TimeStart = time.time()
        self._AlphaBetaTopCountPrunes(board, use_ordering=False, player=player)

        prunes_without = self.AlphaBetaPrunes
        # Run with ordering
        self.AlphaBetaPrunes = 0
        self.TimeStart = time.time()
        self._AlphaBetaTopCountPrunes(board, use_ordering=True, player=player)
        prunes_with = self.AlphaBetaPrunes

        # Restore
        self.TimeLimit = saved_TimeLimit
        self.MaxPly = saved_MaxPly
        self.Strategy = saved_strategy

        if prunes_without == 0:
            return 0.0
        gain = (prunes_without - prunes_with) / max(1, prunes_without)
        return gain * 100.0

    def _AlphaBetaTopCountPrunes(self, board: GameBoard, use_ordering: bool, player: str):
        """
        Helper used for ordering estimation: does a small alpha-beta run to count prunes.
        
        Args:
            board: Current board state
            use_ordering: Whether to use node ordering
            player: Player to evaluate for
        """
        moves = board.GenerateLegalMoves(player)
        alpha = -math.inf
        beta = math.inf
        for mv in moves:
            succ = board.ApplyMove(mv)
            val = self._AlphaBetaMin(succ, 1, alpha, beta, player, use_ordering)
            if val is None:
                break
            alpha = max(alpha, val)
