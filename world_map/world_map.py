import random
from utilities import flatten_two_dimensional_array, check_borders
from .zones import *


"""
    Rooms will be stored in a 2-dimensional array. The room_index var will be a key-index pair linking a room's ID with
    its location within this array for quick lookup. When the Room Array is updated with a new row or column, the
    room_index will also be updated to reflect changes to existing room's indices.
"""


class WorldMap:

    def __init__(self):
        self.zone_index = dict()
        self.zone_array = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def assign_zone_to_map(self, zone, previous_zone=None, travel_direction=None):
        """
            Assigns newly created zones to `zone_array` and adds their array index to `zone_index`.
        :param zone: The zone to be added.
        :param previous_zone: Zone that the user is travelling from. Optional param, if none is provided then the room
                will be placed at [1][1] (the initial center of the map for first room generation).
        :param travel_direction: Direction that the player is travelling.
        :return: None (updates `zone_array` and `zone_index` in place)
        """
        if previous_zone is None:
            self.zone_array[1][1] = zone
            self.zone_index[zone] = [1, 1]
        # create new Zones and assign to World Map array and index.
        else:
            prev_zone_index = self.zone_index[previous_zone]
            # Check to see if the player is exiting the bounds of the existing map. If so expand the map and re-query
            # previous Zone's index.
            if self.check_world_borders(prev_zone_index, travel_direction):
                self.expand_world_map(travel_direction)
                prev_zone_index = self.zone_index[previous_zone]
            # Assign Zone to World Map Array and Index. If this overlaps with an existing Zone then we fucked up
            # somewhere along the way (i.e. the chain of commands that led to this zone creation is faulty).
            if travel_direction == "north":
                if self.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]]:
                    raise ZoneAlreadyExists
                else:
                    self.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]] = zone
                    self.zone_index[zone] = [prev_zone_index[0] - 1, prev_zone_index[1]]
            if travel_direction == "east":
                if self.zone_array[prev_zone_index[0]][prev_zone_index[1] + 1]:
                    raise ZoneAlreadyExists
                else:
                    self.zone_array[prev_zone_index[0]][prev_zone_index[1] + 1] = zone
                    self.zone_index[zone] = [prev_zone_index[0], prev_zone_index[1] + 1]
            if travel_direction == "south":
                if self.zone_array[prev_zone_index[0] + 1][prev_zone_index[1]]:
                    raise ZoneAlreadyExists
                else:
                    self.zone_array[prev_zone_index[0] + 1][prev_zone_index[1]] = zone
                    self.zone_index[zone] = [prev_zone_index[0] + 1, prev_zone_index[1]]
            if travel_direction == "west":
                if self.zone_array[prev_zone_index[0]][prev_zone_index[1] - 1]:
                    raise ZoneAlreadyExists
                else:
                    self.zone_array[prev_zone_index[0]][prev_zone_index[1] - 1] = zone
                    self.zone_index[zone] = [prev_zone_index[0], prev_zone_index[1] - 1]

    def check_world_borders(self, previous_zone_index, travel_direction):
        """
            Checks to see if the player is on the edge of the current world map and is attempting to enter an
            un-populated section of the `zone_array`.
        :param previous_zone_index: The location of the player's previous location.
        :param travel_direction: The direction in which the player is travelling.
        :return: Boolean return from `check_borders` function.
        """
        world_map_width = len(self.zone_array[0]) - 1
        world_map_height = len(self.zone_array) - 1
        return check_borders(previous_zone_index, world_map_width, world_map_height, travel_direction)

    def create_random_zone(self, travel_direction, previous_zone):
        """
            Spawns a zone into newly created zone cells within `zone_array`, selecting them randomly from the choice of
            available zones.
        :param travel_direction: Direction in which a player is travelling
        :param previous_zone: Zone from which a player is coming.
        :return: A zone object
        """
        return random.choice(ZONE_REGISTRY)(self, travel_direction=travel_direction, previous_zone=previous_zone)

    def expand_world_map(self, direction):
        """
            Adds new rows or columns to `zone_array` if the player is attempting to enter a zone area that is not
            currently in the `zone_array` matrix. If 0th element is added to row or columns, calls `update_zone_index`
            to increment all indices.
        :param direction: Direction in which to expand `zone_array`
        :return: None (mutates `zone_array` in place)
        """
        # add new row to North (i.e. index 0 of main list).
        if direction == "north":
            width = len(self.zone_array[0])
            self.zone_array.insert(0, [None for x in range(width)])
            # because the indices of the array items changed, update zone_index dict.
            self.update_zone_index(direction)
        # add a new column to the East (i.e. the very last index of all sublists)
        if direction == "east":
            for row in self.zone_array:
                row.append(None)
        # add new row to South (i.e. the very last index of main list).
        if direction == "south":
            width = len(self.zone_array[0])
            self.zone_array.append([None for x in range(width)])
        # add a new column to the West (i.e. index 0 of all sublists)
        if direction == "west":
            for row in self.zone_array:
                row.insert(0, None)
            # because the indices of the array items changed, update zone_index dict.
            self.update_zone_index(direction)

    def show_world_map(self, player):
        """
            A function to prettify the world map (broken down by zone) to present to the player.
        :param player: Player object
        :return: None (calls `player.add_messages()` in order to append prettified world_map to next round's messages)
        """
        # get the length of the longest zone name to normalize the distance used for the map display.
        width = len(max(flatten_two_dimensional_array(self.zone_array), key=len)) + 14
        world_map = f"Known Map:\n"
        for row in self.zone_array:
            world_map = world_map + f"["
            for zone in row:
                if zone:
                    if zone == player.room.zone:
                        zone_map = f"{zone.zone_type} Zone"
                        world_map += f" [*{zone_map:^{width-2}}*] "
                    else:
                        zone_map = f"{zone.zone_type} Zone"
                        world_map += f" [{zone_map:^{width}}] "
                else:
                    zone_map = "?" * (width-4)
                    world_map += f" [{zone_map:^{width}}] "
            world_map = world_map + f"]\n"
        player.add_messages(world_map)

    def update_zone_index(self, direction):
        """
            Updates the `zone_index` when new rows or columns are added to the `zone_array`. Indices are only increased
            when zones are added to the North (i.e. a new row is added to the 0th index of the array) or to the West
            (i.e. a new column is added in the 0th index of each row).
        :param direction: Direction in which to update the `zone_array`.
        :return: None (mutates the `zone_index` values in place)
        """
        # Iterate through zone_index and increment existing values to reflect changes in index values when new rows or
        # columns are added to 0th element.
        if direction == "north":
            for key, value in self.zone_index.items():
                value[0] = value[0] + 1
        if direction == "west":
            for key, value in self.zone_index.items():
                value[1] = value[1] + 1