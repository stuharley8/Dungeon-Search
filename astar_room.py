#
# CS2400 Introduction to AI
# astar_room.py
#
# Spring, 2020
#
# Author: Stuart Harley
#
# This class holds the room, the cost it took to get to the room
# and the estimated cost to get to the goal as an object (Used for A* search)
#

from dungeon import Room


class AStarRoom:
    """Represents a room in the A* search

    Attributes:
        room (Room): the room
        cost_here (int): cost it took to get to the room
        cost_finish (int): estimated cost it will take to get to the goal
    """

    def __init__(self, room: Room, cost_here: int, cost_finish: int):
        """ This constructor stores the references when the AStarRoom is
        initialized. """
        self.__room = room
        self.__cost_here = cost_here
        self.__cost_finish = cost_finish

    @property
    def room(self) -> Room:
        """ This function returns a reference to the room.  """
        return self.__room

    def cost_here(self) -> int:
        """ This function returns a reference to the cost it took to get to the room.  """
        return self.__cost_here

    def cost_finish(self) -> int:
        """ This function returns a reference to the estimated cost to reach the goal.  """
        return self.__cost_finish
