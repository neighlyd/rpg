import random
from utils import flatten_two_dimensional_array, check_borders
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

    def update_zone_index(self, direction):
        # adding zones to the north or west increases the array indices by 1
        # (either main list for North or sublist for West).
        # We need to iterate through our zone_index and increment existing values to reflect these changes.
        if direction == "north":
            for key, value in self.zone_index.items():
                value[0] = value[0] + 1
        if direction == "west":
            for key, value in self.zone_index.items():
                value[1] = value[1] + 1

    def check_world_borders(self, previous_zone_index, travel_direction):
        world_map_width = len(self.zone_array[0]) - 1
        world_map_height = len(self.zone_array) - 1
        return check_borders(previous_zone_index, world_map_width, world_map_height, travel_direction)

    def expand_world_map(self, direction):
        # get current E/W width of dungeon.
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

    def create_random_zone(self, travel_direction, previous_zone):
        return random.choice(ZONE_REGISTRY)[0](self, travel_direction=travel_direction, previous_zone=previous_zone)
