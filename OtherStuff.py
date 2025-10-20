"""
OtherStuff Module

This module contains miscellaneous helper functions and small data items
for the Checkers game implementation.

Contains:
- StartingMoveLocation: Returns starting move location chosen by the human
- TargetingMoveLocation: Returns target move location chosen by the human
- OpponentOf: Returns the opponent symbol
"""

from typing import Tuple


class OtherStuff:
    """
    Miscellaneous helper functions and small data items.
    Contains StartingMoveLocation and TargetingMoveLocation identifiers as required.
    """

    @staticmethod
    def StartingMoveLocation(r: int, c: int) -> Tuple[int, int]:
        """
        Returns a tuple representing the starting move location chosen by the human.
        Used by the driver to pass user input to the game engine.
        
        Args:
            r: Row index (0-based)
            c: Column index (0-based)
            
        Returns:
            Tuple[int, int]: Starting position (row, column)
        """
        return (r, c)

    @staticmethod
    def TargetingMoveLocation(r: int, c: int) -> Tuple[int, int]:
        """
        Returns a tuple representing the target move location chosen by the human.
        
        Args:
            r: Row index (0-based)
            c: Column index (0-based)
            
        Returns:
            Tuple[int, int]: Target position (row, column)
        """
        return (r, c)

    @staticmethod
    def OpponentOf(player: str) -> str:
        """
        Returns the opponent symbol: input 'w'->'b', 'b'->'w'.
        Use lowercase to denote side color; kings deduced in GameBoard.
        
        Args:
            player: Current player ('w' for white or 'b' for black)
            
        Returns:
            str: Opponent player symbol
        """
        return 'b' if player == 'w' else 'w'

