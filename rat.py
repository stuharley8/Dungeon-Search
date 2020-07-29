#
# CS2400 Introduction to AI
# rat.py
#
# Spring, 2020
#
# Author: Stuart Harley
#
# Stub class for Lab 2
# This class creates a Rat agent to be used to explore a Dungeon
#
# Note: Instance variables with a single preceding underscore are intended
# to be protected, so setters and getters are included to enable this convention.
#
# Note: The -> notation in the function definition line is a type hint.  This
# will make identifying the appropriate return type easier, but they are not
# enforced by Python.
#
from typing import Dict, Any, Tuple, Union

from dungeon import Dungeon, Room, Direction
from astar_room import AStarRoom
from typing import *
from queue import Queue
import sys


class Rat:
    """Represents a Rat agent in a dungeon. It enables navigation of the
    dungeon space through searching.

    Attributes:
        dungeon (Dungeon): identifier for the dungeon to be explored
        start_location (Room): identifier for current location of the rat
        echo_rooms_searched (bool): state indicator to print the room names as they are searched
        rooms_visited_by_last_search (List[str]): list of room names visited in the last search algorithm
    """

    def __init__(self, dungeon: Dungeon, start_location: Room):
        """ This constructor stores the references when the Rat is
        initialized. """
        self._dungeon = dungeon
        self.start_location = start_location
        self._echo_rooms_searched = False
        self._rooms_visited_by_last_search = [Type[str]]

    @property
    def dungeon(self) -> Dungeon:
        """ This function returns a reference to the dungeon.  """
        return self._dungeon

    def set_echo_rooms_searched(self) -> None:
        """ The _echo_rooms_searched variable is used as a flag for whether
        the rat should display rooms as they are visited. """
        self._echo_rooms_searched = True

    @dungeon.setter
    def dungeon(self, value):
        self._dungeon = value

    def path_to(self, target_location: Room) -> List[Room]:
        """ This function finds and returns a list of rooms from
        start_location to target_location.  The list will include
        both the start and destination, and if there isn't a path
        the list will be empty. This function uses depth first search. """
        self._rooms_visited_by_last_search = []
        candidates = [self.start_location]
        prev = {Type[Room]: Type[Room]}
        while len(candidates) != 0:
            next_room = candidates.pop()
            self._rooms_visited_by_last_search.append(next_room.name)
            if self._echo_rooms_searched:
                print("Visiting: " + next_room.name)
            if next_room is target_location:
                path = [next_room]
                while next_room is not self.start_location:
                    path.append(prev[next_room])
                    next_room = prev[next_room]
                path.reverse()
                return path
            else:
                for room in reversed(next_room.neighbors()):
                    if room not in prev.values():
                        prev[room] = next_room
                        candidates.append(room)
        return []  # empty list signifies failure

    def directions_to(self, target_location: Room) -> List[str]:
        """ This function returns a list of the names of the rooms from the
        start_location to the target_location. """
        rooms = self.path_to(target_location)
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

    def bfs_path_to(self, target_location: Room) -> List[Room]:
        """Returns the list of rooms from the start location to the
        target location, using breadth-first search to find the path."""
        self._rooms_visited_by_last_search = []
        candidates: Queue[Room] = Queue()
        candidates.put(self.start_location)
        visited = set()
        visited.add(self.start_location)
        prev = {Type[Room]: Type[Room]}
        while not candidates.empty():
            next_room = candidates.get()
            self._rooms_visited_by_last_search.append(next_room.name)
            if self._echo_rooms_searched:
                print("Visiting: " + next_room.name)
            if next_room is target_location:
                path = [next_room]
                while next_room is not self.start_location:
                    path.append(prev[next_room])
                    next_room = prev[next_room]
                path.reverse()
                return path
            else:
                for room in next_room.neighbors():
                    if room not in visited:
                        visited.add(room)
                        prev[room] = next_room
                        candidates.put(room)
        return []  # empty list signifies failure

    def bfs_directions_to(self, target_location: Room) -> List[str]:
        """Return the list of rooms names from the rat's current location to
        the target location. Uses breadth-first search."""
        rooms = self.bfs_path_to(target_location)
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

    def id_path_to(self, target_location: Room) -> List[Room]:
        """Returns the list of rooms from the start location to the
        target location, using iterative deepening."""
        self._rooms_visited_by_last_search = []
        path = [Type[Room]]
        for depth in range(0, self.dungeon.size()):
            path = self.__dfs_path_to(target_location, depth)
            if len(path) != 0:
                break
        return path

    def id_directions_to(self, target_location: Room) -> List[str]:
        """Return the list of rooms names from the rat's current location to
        the target location. Uses iterative deepening."""
        rooms = self.id_path_to(target_location)
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

    def __dfs_path_to(self, target_location: Room, depth: int) -> List[Room]:
        """Private helper method used in iterative deepening search.
        Returns the list of rooms from the start location to the
        target location, using depth first search, up to a specified depth."""
        candidates = [(self.start_location, 0)]  # list of candidates to search stored with their depth
        prev = {Type[Tuple[Room, int]]: Type[Tuple[Room, int]]}
        while len(candidates) != 0:
            (next_room, d) = candidates.pop()
            self._rooms_visited_by_last_search.append(next_room.name)
            if self._echo_rooms_searched:
                print("Visiting: " + next_room.name)
            if next_room is target_location:
                path = [next_room]
                while next_room is not self.start_location:
                    path.append(prev[(next_room, d)][0])
                    (next_room, d) = prev[(next_room, d)]
                path.reverse()
                return path
            else:
                if d <= depth:
                    for room in reversed(next_room.neighbors()):
                        prev[(room, d + 1)] = (next_room, d)
                        candidates.append((room, d + 1))
        return []  # empty list signifies failure

    def astar_path_to(self, target_location: Room) -> List[Room]:
        """Returns the list of rooms from the start location to the
        target location, using A* search to find the path."""
        self._rooms_visited_by_last_search = []
        candidates = [AStarRoom(self.start_location, 0, self.start_location.estimated_cost_to(target_location))]
        cost_searched = {self.start_location: self.start_location.estimated_cost_to(target_location)}
        prev = {Type[AStarRoom]: Type[AStarRoom]}
        while len(candidates) != 0:
            next_astar_room = candidates[0]
            next_astar_room_index = 0
            for i in range(len(candidates)):
                if candidates[i].cost_here() + candidates[i].cost_finish() \
                        < next_astar_room.cost_here() + next_astar_room.cost_finish():
                    next_astar_room = candidates[i]
                    next_astar_room_index = i
            del candidates[next_astar_room_index]  # removes the selected room from the candidates list
            if next_astar_room.cost_here() > self.dungeon.size()+1:  # Used in cases where there is not solution
                break
            self._rooms_visited_by_last_search.append(next_astar_room.room.name)
            if self._echo_rooms_searched:
                print("Visiting: " + next_astar_room.room.name)
            if next_astar_room.room is target_location:
                path = [next_astar_room.room]
                while next_astar_room.room is not self.start_location:
                    path.append(prev[next_astar_room].room)
                    next_astar_room = prev[next_astar_room]
                path.reverse()
                return path
            else:
                for room in reversed(next_astar_room.room.neighbors()):
                    astar_room = AStarRoom(room, next_astar_room.cost_here() + 1, room.estimated_cost_to(target_location))
                    if cost_searched.get(room, sys.maxsize) > astar_room.cost_here() + astar_room.cost_finish():
                        prev[astar_room] = next_astar_room
                        candidates.append(astar_room)
                        cost_searched[astar_room.room] = astar_room.cost_here() + astar_room.cost_finish()
        return []  # empty list signifies failure

    def astar_directions_to(self, target_location: Room) -> List[str]:
        """Return the list of room names from the rat's current location to
        the target location. Uses A* search."""
        rooms = self.astar_path_to(target_location)
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

    def rooms_visited_by_last_search(self) -> List[str]:
        """Return the list of rooms visited (in any order)"""
        return self._rooms_visited_by_last_search
