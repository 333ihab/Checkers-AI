"""
GameBoard Module

This module represents the checkers board and game state.

Responsible for:
- Storing board as 8x8 grid with items: None, 'w', 'W', 'b', 'B'
- Generating legal moves (with forced-capture logic)
- Applying moves to produce successor states
- Testing goal (one side has no pieces)
- Display utilities
- Heuristic evaluation function

Board representation:
- 'w': White piece (human)
- 'W': White king
- 'b': Black piece (agent)
- 'B': Black king
- None: Empty square
"""

import copy
from typing import List, Tuple, Optional
from OtherStuff import OtherStuff


class GameBoard:
    """
    Represents the checkers board and game state.
    
    Attributes:
        BOARD_SIZE: Size of the board (8x8)
        Board: 2D list representing the game board
        PlayerToMove: Current player's turn ('w' or 'b')
    """

    BOARD_SIZE = 8
    def __init__(self, board: Optional[List[List[Optional[str]]]] = None,
                 player_to_move: str = 'w'):
        """
        Initialize a GameBoard. If board is None, create the standard starting position.
        
        Args:
            board: Optional 2D list representing board state
            player_to_move: 'w' (white/human) or 'b' (black/agent). Defaults to 'w'.
        """
        if board is None:
            self.Board = self._CreateStartingBoard()
        else:
            self.Board = board
        self.PlayerToMove = player_to_move  # 'w' or 'b'

    def _CreateStartingBoard(self) -> List[List[Optional[str]]]:
        """
        Create the standard checkers starting position: 3 rows of black on top, 3 rows of white on bottom.
        Playable squares are those with (r+c)%2==1.
          Returns:
            List[List[Optional[str]]]: Initial board configuration
        """
        B = [[None for _ in range(self.BOARD_SIZE)] for __ in range(self.BOARD_SIZE)]
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if (r + c) % 2 == 1:
                    if r < 3:
                        B[r][c] = 'b'  # black starts top
                    elif r > 4:
                        B[r][c] = 'w'  # white bottom
        return B

    def Clone(self) -> 'GameBoard':
        """
        Return a deep copy of the board state.
        
        Returns:
            GameBoard: Deep copy of current board state
        """
        return GameBoard(board=copy.deepcopy(self.Board), player_to_move=self.PlayerToMove)

    def DisplayBoard(self):
        """
        Nicely prints the board to stdout. Shows row/column indices 0..7.
        """
        print("    " + " ".join(str(c) for c in range(self.BOARD_SIZE)))
        print("   +" + "--" * self.BOARD_SIZE + "+")
        for r in range(self.BOARD_SIZE):
            rowstr = f"{r} | "
            for c in range(self.BOARD_SIZE):
                cell = self.Board[r][c]
                rowstr += (cell if cell is not None else '.') + " "
            rowstr += "|"
            print(rowstr)
        print("   +" + "--" * self.BOARD_SIZE + "+")

    def GetPiecesOfPlayer(self, player: str) -> List[Tuple[int, int]]:
        """
        Returns list of (r,c) positions occupied by player's pieces (both kings and men).
        
        Args:
            player: 'w' or 'b'
            
        Returns:
            List[Tuple[int, int]]: List of positions containing player's pieces
        """
        result = []
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                piece = self.Board[r][c]
                if piece is None:
                    continue
                if piece.lower() == player:
                    result.append((r, c))
        return result

    def GoalTest(self) -> Optional[str]:
        """
        Returns the winner 'w' or 'b' if one has no pieces left, otherwise None.
        
        Returns:
            Optional[str]: Winner ('w' or 'b') or None if game continues
        """
        w_pieces = any(self.Board[r][c] is not None and self.Board[r][c].lower() == 'w'
                       for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE))
        b_pieces = any(self.Board[r][c] is not None and self.Board[r][c].lower() == 'b'
                       for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE))
        if not w_pieces:
            return 'b'
        if not b_pieces:
            return 'w'
        return None

    # -------------------------
    # Move generation helpers
    # -------------------------
    def _InBounds(self, r: int, c: int) -> bool:
        """Check if position is within board boundaries."""
        return 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE

    def _IsOpponentPiece(self, piece: str, player: str) -> bool:
        """Check if piece belongs to opponent."""
        return piece is not None and piece.lower() != player

    def _PieceDirections(self, piece: str) -> List[Tuple[int, int]]:
        """
        Returns movement directions for piece:
        - Men: 'w' moves up (r-1), 'b' moves down (r+1)
        - Kings: can move both up/down
        Directions are diagonal offsets (dr, dc)
        
        Args:
            piece: Piece symbol ('w', 'W', 'b', 'B', or None)
            
        Returns:
            List[Tuple[int, int]]: List of valid direction tuples
        """
        if piece is None:
            return []
        if piece.isupper():  # King
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if piece == 'w':
                return [(-1, -1), (-1, 1)]
            else:  # 'b'
                return [(1, -1), (1, 1)]

    def GenerateLegalMoves(self, player: str) -> List[dict]:
        """
        Generate all legal moves for the given player.
        Return list of moves: each move is a dict with keys:
          - 'start': (r,c)
          - 'sequence': list of target squares visited (for jumps may be multiple)
          - 'captures': list of captured positions
        Captures are mandatory: if any capture move exists, only those are returned.
        For simple moves, 'captures' is empty and 'sequence' has exactly one target.
        
        Args:
            player: Player symbol ('w' or 'b')
            
        Returns:
            List[dict]: List of legal move dictionaries
        """
        all_moves = []
        capture_moves = []

        for (r, c) in self.GetPiecesOfPlayer(player):
            piece = self.Board[r][c]
            # first find captures (multi-jump allowed)
            visited = set()
            def dfs_jumps(cur_r, cur_c, captured_so_far, seq):
                """
                Recursively find multi-jumps from position (cur_r,cur_c).
                captured_so_far: list of captured positions
                seq: sequence of landing squares from the original start (list)
                """
                found_any = False
                dirs = self._PieceDirections(piece if len(captured_so_far)==0 else self.Board[orig_r][orig_c])
                # Note: During multi-jump the piece may become a king only after turn end (not in mid jump) in American checkers.
                for (dr, dc) in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    mid_r = cur_r + dr
                    mid_c = cur_c + dc
                    land_r = cur_r + 2*dr
                    land_c = cur_c + 2*dc
                    if not (self._InBounds(mid_r, mid_c) and self._InBounds(land_r, land_c)):
                        continue
                    mid_piece = self.Board[mid_r][mid_c]
                    land_piece = self.Board[land_r][land_c]
                    if mid_piece is None or land_piece is not None:
                        continue
                    if (mid_r, mid_c) in captured_so_far:
                        continue
                    if self._IsOpponentPiece(mid_piece, player):
                        # Make a temporary board change to allow further jumps without modifying self.
                        found_any = True
                        new_captured = captured_so_far + [(mid_r, mid_c)]
                        new_seq = seq + [(land_r, land_c)]
                        # save original pieces
                        orig_mid = self.Board[mid_r][mid_c]
                        orig_land = self.Board[land_r][land_c]
                        orig_cur = self.Board[cur_r][cur_c]
                        self.Board[land_r][land_c] = self.Board[cur_r][cur_c]
                        self.Board[cur_r][cur_c] = None
                        self.Board[mid_r][mid_c] = None
                        dfs_jumps(land_r, land_c, new_captured, new_seq)
                        # restore
                        self.Board[cur_r][cur_c] = orig_cur
                        self.Board[mid_r][mid_c] = orig_mid
                        self.Board[land_r][land_c] = orig_land
                if not found_any and captured_so_far:
                    # terminal capture sequence
                    capture_moves.append({'start': (orig_r, orig_c),
                                          'sequence': seq.copy(),
                                          'captures': captured_so_far.copy()})
            orig_r, orig_c = r, c
            dfs_jumps(r, c, [], [])
            # If no captures from this piece, consider simple moves
            if not any(move['start'] == (r, c) for move in capture_moves):
                for (dr, dc) in self._PieceDirections(piece):
                    nr = r + dr
                    nc = c + dc
                    if self._InBounds(nr, nc) and self.Board[nr][nc] is None:
                        all_moves.append({'start': (r, c), 'sequence': [(nr, nc)], 'captures': []})

        # If any capture moves anywhere, only return captures
        if capture_moves:
            return capture_moves
        return all_moves

    def ApplyMove(self, move: dict) -> 'GameBoard':
        """
        Apply a move dict to this board and return a new GameBoard as successor.
        move keys: 'start', 'sequence' (list of landing squares), 'captures' (list of captured positions)
        After move, switch player.
        Handle kinging (when a man reaches last rank).
        
        Args:
            move: Dictionary containing move information
            
        Returns:
            GameBoard: New board state after applying move
        """
        nb = self.Clone()
        sr, sc = move['start']
        piece = nb.Board[sr][sc]
        nb.Board[sr][sc] = None
        # For sequence, land on final square (intermediate landing squares used only for multiple jumps)
        last_r, last_c = (sr, sc)
        for (tr, tc) in move['sequence']:
            last_r, last_c = tr, tc
        # place piece
        nb.Board[last_r][last_c] = piece
        # remove captures
        for (cr, cc) in move['captures']:
            nb.Board[cr][cc] = None
        # kinging
        if piece == 'w' and last_r == 0:
            nb.Board[last_r][last_c] = 'W'
        if piece == 'b' and last_r == self.BOARD_SIZE - 1:
            nb.Board[last_r][last_c] = 'B'
        nb.PlayerToMove = OtherStuff.OpponentOf(self.PlayerToMove)
        return nb

    def MakeMoveIfLegal(self, StartingMoveLocation: Tuple[int,int], TargetingMoveLocation: Tuple[int,int]) -> Optional['GameBoard']:
        """
        Convenience: Given start and target single-step location from human, attempt to find matching legal move.
        For multi-jump, the human must provide the full landing square (the first or final?) -- to keep UI simple:
        We accept only single-step non-captures or single-jump captures. If a multi-jump is possible and human wants to do it,
        they can input the successive starts & targets per jump or we could try to auto-complete; to be user friendly we will:
        - If the requested target corresponds to the first landing of a multi-jump, we apply the full multi-jump automatically (do forced continuation).
        
        Args:
            StartingMoveLocation: Starting position tuple (row, col)
            TargetingMoveLocation: Target position tuple (row, col)
            
        Returns:
            Optional[GameBoard]: New board state if move is legal, None otherwise
        """
        legal = self.GenerateLegalMoves(self.PlayerToMove)
        s = StartingMoveLocation
        t = TargetingMoveLocation
        # find a legal move that matches start and whose first or final landing matches provided target
        for mv in legal:
            if mv['start'] != s:
                continue
            # Accept if target equals first sequence landing or final landing
            seq0 = mv['sequence'][0] if mv['sequence'] else None
            seqlast = mv['sequence'][-1] if mv['sequence'] else None
            if seq0 == t or seqlast == t:
                return self.ApplyMove(mv)
        return None

    # -------------------------
    # Heuristic / evaluation
    # -------------------------
    def EvaluateFor(self, player: str) -> float:
        """
        Heuristic evaluation function from 'player' perspective (higher => better for player).
        Components:
         - piece count: men = 1, kings = 1.8
         - mobility: number of legal moves * 0.1
         - center control bonus
         
        Args:
            player: Player to evaluate for ('w' or 'b')
            
        Returns:
            float: Evaluation score (higher is better for player)
        """
        my_score = 0.0
        opp_score = 0.0
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                p = self.Board[r][c]
                if p is None:
                    continue
                val = 1.0 if p.islower() else 1.8  # king slightly more valuable
                # center control
                center_bonus = 0.05 * (3 - (abs(3.5 - r) + abs(3.5 - c))/2.0)
                val += center_bonus
                if p.lower() == player:
                    my_score += val
                else:
                    opp_score += val
        # mobility
        my_moves = len(self.GenerateLegalMoves(player))
        opp_moves = len(self.GenerateLegalMoves(OtherStuff.OpponentOf(player)))
        mobility_score = 0.1 * (my_moves - opp_moves)
        return (my_score - opp_score) + mobility_score
