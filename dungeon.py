#
# dungeon.py: represents a dungeon in the style of Zork.
#
# Author: Robert W. Hasker, 2020
#

from enum import Enum
from typing import *
import json

Direction = Enum('Direction', 'EAST WEST NORTH SOUTH UP DOWN')


def opposite(d: Direction) -> Direction:
    """Given a direction, returns the opposite direction; eg: North <-> South.
    Fails if given an invalid direction.
    """
    if d.value == Direction.EAST.value:
        return Direction.WEST
    elif d.value == Direction.WEST.value:
        return Direction.EAST
    elif d.value == Direction.NORTH.value:
        return Direction.SOUTH
    elif d.value == Direction.SOUTH.value:
        return Direction.NORTH
    elif d.value == Direction.UP.value:
        return Direction.DOWN
    elif d.value == Direction.DOWN.value:
        return Direction.UP
    else:
        assert False


class Room:
    """Represents a room in a dungeon at a certain level. Tracks all
    neighbors; rooms that can be traveled to from this room. There are
    no passages from a room back to itself.

    Attributes:
        name (str): identifier for room; should be unique w/in a dungeon
        level (int): level of room, defaulting to 1
    """

    def __init__(self, name: str, level: int, north: int, east: int):
        """Create a room in a given level; level defaults to 1."""
        self._name = name
        self._level = level
        self._neighbors: List[Any] = [None for x in Direction]
        self.trap = None  # or a string giving the trap name
        self.monster = None  # or a string giving the monster name
        self._north = north
        self._east = east

    def to_json(self) -> str:
        """Return JSON representation of room that can be reloaded."""
        return json.dumps(self)

    @property
    def name(self) -> str:
        """Name used to identify room."""
        return self._name

    @property
    def level(self) -> int:
        """Level of room within dungeon."""
        return self._level

    def estimated_cost_to(self, other_room) -> int:
        """Returns the estimated cost of traveling from this room to
        another room using manhattan distance."""
        return (abs(other_room._north - self._north)
                + abs(other_room._east - self._east)
                + abs(other_room._level - self._level))

    def neighbor_to(self, d: Direction) -> Any:
        """Returns neighbor in given direction, or None if there is none."""
        return self._neighbors[d.value - 1]

    def neighbors(self) -> List[Any]:
        """Returns list of rooms reachable from current room."""
        return [n for n in self._neighbors if n is not None]

    def add_single_direction_neighbor(self, r, d: Direction) -> None:
        """Adds one-way passage from the current room (self) to another room r in the
        given direction.

        """
        assert r is not self  # no passages from room back to self
        self._neighbors[d.value - 1] = r

    def add_neighbor(self, r, d: Direction) -> None:
        """Adds two-way passage from this room (self) to another room r in the given
        direction. The passage back is in the opposite direction of the
        passage to r.
        """
        self.add_single_direction_neighbor(r, d)
        r.add_single_direction_neighbor(self, opposite(d))


class Dungeon:
    """Represents a dungeon as a collection of (possibly connected) rooms.  Each
    room in the dungeon is unique. A room can be connected to rooms that are
    not registered with the dungeon by calling add_room; this just means there
    is no way to look up the room, but it will still be possible to travel
    such a room.  Likewise, client code can start with other rooms besides the
    specified start room.

    Attributes:
        start (Room): recommended start location when exploring the dungeon.
    """

    def __init__(self, start: Room):
        """Initialize dungeon with a given starting room. The start room is
        searchable in the dungeon.
        """
        self._rooms = {start.name: start}
        self._start = start

    def to_json(self) -> str:
        """Returns a JSON string representation of the dungeon."""
        return json.dumps(self)

    @property
    def start(self) -> Room:
        """Recommended starting point for exploring the dungeon."""
        return self._start

    def add_room(self, r: Room) -> None:
        """Adds a new room to the dungeon, failing if it already exists.  Calling this
        allows using the name to look up a room in the dungeon.
        """
        assert r.name not in self._rooms
        self._rooms[r.name] = r

    def has(self, room_name: str) -> bool:
        """Returns true if the dungeon has a room with the given name."""
        return room_name in self._rooms.keys()

    def find(self, room_name: str) -> Room:
        """Returns the named room in the dungeon or fails."""
        assert self.has(room_name)
        return self._rooms[room_name]

    def size(self) -> int:
        return len(self._rooms)

    def valid_path(self, path: List[Room]) -> bool:
        """Returns true if dungeon supports following provided path"""
        copied_path = [r for r in path]
        current = copied_path.pop()
        while len(copied_path) > 0:
            next_room = copied_path.pop()
            if next_room not in current.neighbors():
                return False
            current = next_room
        return True


def read_room_from_json(source: str) -> Room:
    "Read a room from a JSON source string." ""
    result = json.loads(source)
    assert isinstance(result, Room)
    return result


def read_dungeon_from_json(source: str) -> Dungeon:
    "Read a full dungeon from a JSON source string." ""
    result = json.loads(source)
    assert isinstance(result, Dungeon)
    return result