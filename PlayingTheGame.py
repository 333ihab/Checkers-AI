"""
PlayingTheGame Module

High-level game manager: interacts with the human player, receives StartingMoveLocation/TargetingMoveLocation,
invokes the SearchToolBox to pick the agent's move, and reports per-move and cumulative analytics.

Manages:
- Game loop and player turns
- Human input handling
- Bot move selection using SearchToolBox
- Analytics reporting (per-move and cumulative)
"""

import time
from GameBoard.board import GameBoard
from SearchToolBox.search import SearchToolBox
from OtherStuff import OtherStuff


class PlayingTheGame:
    """
    High-level game manager for Checkers.
    
    Attributes:
        BoardState: Current game board state
        SearchAgent: AI search agent for bot moves
        CumulativeAnalytics: Dictionary tracking cumulative statistics for both players
        AgentColor: Color assigned to the AI agent ('b' for black)
    """

    def __init__(self, Strategy: str = "AlphaBetaOrdering", TimeLimit: float = 2.0, MaxPly: int = 6):
        """
        Initialize a new game with given search parameters.
        
        Args:
            Strategy: Search strategy ("Minimax", "AlphaBeta", "AlphaBetaOrdering")
            TimeLimit: Time limit per move in seconds (1 to 3 recommended)
            MaxPly: Maximum search depth in plies (5 to 9 recommended)
        """
        self.BoardState = GameBoard()   # human (white) starts
        self.SearchAgent = SearchToolBox(Strategy=Strategy, TimeLimit=TimeLimit, MaxPly=MaxPly)
        # cumulative analytics tracked per player
        self.CumulativeAnalytics = {
            'w': {'NodesExpanded': 0, 'NodesGenerated': 0, 'AlphaBetaPrunes': 0, 'Moves': 0},
            'b': {'NodesExpanded': 0, 'NodesGenerated': 0, 'AlphaBetaPrunes': 0, 'Moves': 0}
        }
        self.AgentColor = 'b'  # black

    def RunInteractiveGame(self):
        """
        Main loop. Prompts human for moves until game ends. After each human move, agent picks a move.
        Inputs for human: starting and target coordinates using 0-based indices.
        """
        print("Starting Checkers game. You are White (w). Input moves as: start_row start_col target_row target_col (0-based).")
        print(f"Agent search strategy: {self.SearchAgent.Strategy}, Time limit T={self.SearchAgent.TimeLimit}s, MaxPly P={self.SearchAgent.MaxPly}")
        self.BoardState.DisplayBoard()

        while True:
            winner = self.BoardState.GoalTest()
            if winner is not None:
                print("\nGame over! Winner:", "You (white)" if winner == 'w' else "Agent (black)")
                self._ReportCumulativeStats()
                break

            if self.BoardState.PlayerToMove == 'w':
                # Human turn
                success = False
                while not success:
                    try:
                        raw = input("\nYour move (start_row start_col target_row target_col): ").strip()
                        parts = raw.split()
                        if len(parts) != 4:
                            print("Please enter 4 integers separated by space.")
                            continue
                        sr, sc, tr, tc = map(int, parts)
                        s = OtherStuff.StartingMoveLocation(sr, sc)
                        t = OtherStuff.TargetingMoveLocation(tr, tc)
                        newstate = self.BoardState.MakeMoveIfLegal(s, t)
                        if newstate is None:
                            print("Illegal move. Either move invalid or does not match forced-capture rules. Try again.")
                            continue
                        else:
                            self.BoardState = newstate
                            self.CumulativeAnalytics['w']['Moves'] += 1
                            # No search analytics for human (unless we want to track), but still show generated moves count
                            self.BoardState.DisplayBoard()
                            success = True
                    except Exception as e:
                        print("Error parsing input:", e)
                        continue
            else:
                # Agent turn
                print("\nAgent is thinking...")
                start_time = time.time()
                chosen_move, analytics = self.SearchAgent.ChooseMove(self.BoardState)
                time_used = analytics['TimeUsed']
                end_time = time.time()
                if chosen_move is None:
                    print("Agent has no legal moves. You win!")
                    self._ReportCumulativeStats()
                    break
                # Apply move
                self.BoardState = self.BoardState.ApplyMove(chosen_move)
                # Update cumulative analytics for agent
                self.CumulativeAnalytics['b']['NodesExpanded'] += analytics['NodesExpanded']
                self.CumulativeAnalytics['b']['NodesGenerated'] += analytics['NodesGenerated']
                self.CumulativeAnalytics['b']['AlphaBetaPrunes'] += analytics['AlphaBetaPrunes']
                self.CumulativeAnalytics['b']['Moves'] += 1

                # Report per-move analytics
                print(f"Agent move chosen: start {chosen_move['start']} -> sequence {chosen_move['sequence']}, captures {chosen_move['captures']}")
                print(f"Per-move analytics: NodesExpanded={analytics['NodesExpanded']}, NodesGenerated={analytics['NodesGenerated']}, "
                      f"AlphaBetaPrunes={analytics['AlphaBetaPrunes']}, TimeUsed={time_used:.3f}s, OrderingUsed={analytics['OrderingUsed']}")
                if 'OrderingGainEstimate' in analytics:
                    print(f"Estimated ordering gain: {analytics['OrderingGainEstimate']:.1f}% (shallow estimate)")
                self.BoardState.DisplayBoard()

    def _ReportCumulativeStats(self):
        """
        Print the cumulative analytics gathered across the game for both players (agent only tracked for search).
        """
        print("\nCumulative analytics:")
        for ply in ['w', 'b']:
            data = self.CumulativeAnalytics[ply]
            print(f"Player {ply} - Moves: {data['Moves']}, NodesExpanded: {data['NodesExpanded']}, NodesGenerated: {data['NodesGenerated']}, Prunes: {data['AlphaBetaPrunes']}")


# ---------------------------
# Main execution: Configuration and game start
# ---------------------------
def _PromptForConfig():
    """
    Prompt the user at start to select S, T, P within allowed ranges. Defaults provided.
    
    Returns:
        Tuple[str, float, int]: (Strategy, TimeLimit, MaxPly)
    """
    print("Configure Agent (press Enter to accept defaults).")
    strat_map = {'1': 'Minimax', '2': 'AlphaBeta', '3': 'AlphaBetaOrdering'}
    print("Choose strategy S: 1) Minimax  2) AlphaBeta  3) AlphaBetaOrdering (default 3)")
    s_choice = input("S> ").strip()
    Strategy = strat_map.get(s_choice, 'AlphaBetaOrdering')

    print("Choose time limit T in seconds (1 to 3) (default 2):")
    t_choice = input("T> ").strip()
    try:
        T = float(t_choice) if t_choice else 2.0
    except:
        T = 2.0
    if T < 1: T = 1.0
    if T > 3: T = 3.0

    print("Choose max plies P (5 to 9) (default 6):")
    p_choice = input("P> ").strip()
    try:
        P = int(p_choice) if p_choice else 6
    except:
        P = 6
    if P < 5: P = 5
    if P > 9: P = 9

    return Strategy, T, P


if __name__ == "__main__":
    print("=== Checkers Agent ===")
    Strategy, T, P = _PromptForConfig()
    game = PlayingTheGame(Strategy=Strategy, TimeLimit=T, MaxPly=P)
    game.RunInteractiveGame()
