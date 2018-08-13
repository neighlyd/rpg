from game import world_map
from utils import ZoneAlreadyExists

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
        print(self.zone_index)

    def _show_map(self):
        known_map = (f"\n")
        for row in self.zone_array:
            known_map = known_map + f"{row}\n"
        return known_map

    def expand_dungeon(self, direction):
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

    def create_zone(self, travel_direction, previous_zone):
        prev_zone_index = self.zone_index[id(previous_zone)]
        if prev_zone_index[0] == 0:
            if travel_direction == "north":
                new_zone = Zone(self)
        pass


class Zone:

    def __init__(self, world_map, zone_type=None):
        self.world_map = world_map
        self.room_index = list()
        self.room_array = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.zone_type = zone_type

    def _assign_zone_to_world_map_array(self, travel_direction=None, previous_zone=None):
        # create initial Zone.
        if previous_zone is None:
            self.world_map.zone_array[1][1] = self
            self.world_map.zone_index[id(self)] = [1, 1]
        # create new Zones and assign to World Map array and index.
        else:
            prev_zone_index = self.world_map.zone_index[id(previous_zone)]
            # if the player is exiting the bounds of the existing map, then expand the map.
            if (prev_zone_index[0] == 0 and travel_direction == "north") \
                    or (prev_zone_index[1] == len(world_map.zone_array[0]) - 1 and travel_direction == "east") \
                    or (prev_zone_index[0] == len(world_map.zone_array) - 1 and travel_direction == "south") \
                    or (prev_zone_index[1] == 0 and travel_direction == "west"):
                self.world_map.expand_dungeon(travel_direction)
                # TODO: Assign new zone to WorldMap array and Index. Remember to requery the previous zone index.
            # The player is staying within the bounds of the extant world, no need to expand. Create zone and assign to
            # World Map Array and Index. If this overlaps with an existing Zone then we fucked up somewhere along the
            # way (i.e. the chain of commands that led to this zone creation is faulty).
            else:
                if travel_direction == "north":
                    if self.world_map.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]]:
                        raise ZoneAlreadyExists
                    else:
                        self.world_map.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]] = self
                        self.world_map.zone_index[id(self)] = [prev_zone_index[0] - 1, prev_zone_index[1]]
                if travel_direction == "east":
                    if self.world_map.zone_array[prev_zone_index[0]][prev_zone_index[1] + 1]:
                        raise ZoneAlreadyExists
                    else:
                        self.world_map.zone_array[prev_zone_index[0]][prev_zone_index[1] + 1] = self
                        self.world_map.zone_index[id(self)] = [prev_zone_index[0], prev_zone_index[1] + 1]
                if travel_direction == "south":
                    if self.world_map.zone_array[prev_zone_index[0] + 1][prev_zone_index[1]]:
                        raise ZoneAlreadyExists
                    else:
                        self.world_map.zone_array[prev_zone_index[0] + 1][prev_zone_index[1]] = self
                        self.world_map.zone_index[id(self)] = [prev_zone_index[0] + 1, prev_zone_index[1]]
                if travel_direction == "west":
                    if self.world_map.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]]:
                        raise ZoneAlreadyExists
                    else:
                        self.world_map.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]] = self
                        self.world_map.zone_index[id(self)] = [prev_zone_index[0] - 1, prev_zone_index[1]]

    def query_neighbor(self, direction):
        # Query neighboring spaces in WorldMap array to see if there are zones there. If not, create them.
        this_zone_index = self.world_map.zone_index[id(self)]
        if direction == "north":
            try:
                north_zone = self.world_map.zone_array[this_zone_index[0] - 1][this_zone_index[1]]
                north_zone_index = self.world_map.zone_index[id(north_zone)]
                return north_zone_index
            except AttributeError:
                return False
        if direction == "east":
            try:
                east_zone = self.world_map.zone_array[this_zone_index[0]][this_zone_index[1] + 1]
                east_zone_index = self.world_map.zone_index[id(east_zone)]
                return east_zone_index
            except AttributeError:
                return False
        if direction == "south":
            try:
                south_zone = self.world_map.zone_array[this_zone_index[0] + 1][this_zone_index[1]]
                south_zone_index = self.world_map.zone_index[id(south_zone)]
                return south_zone_index
            except AttributeError:
                return False
        if direction == "west":
            try:
                west_zone = self.world_map.zone_array[this_zone_index[0]][this_zone_index[1] - 1]
                west_zone_index = self.world_map.zone_index[id(west_zone)]
                return west_zone_index
            except AttributeError:
                return False

    def expand_world_map(self, direction):
        pass

    # Moved from Room class.
    # def _pre_flight_expands(self, game_map, previous_room):
    #     prev_index = game_map.room_index[id(previous_room)]
    #     # Check if it is the Northern most room and add new row if so.
    #     if prev_index[0] == 0:
    #         game_map.expand_dungeon("north")
    #     # check if it is Eastern most room and add new row if so.
    #     elif prev_index[1] == len(game_map.room_array[0]) - 1:
    #         game_map.expand_dungeon("east")
    #     # check if it is the Southern most room and add new row if so.
    #     elif prev_index[0] == len(game_map.room_array) - 1:
    #         game_map.expand_dungeon("south")
    #     # check if it is the Western most room and add new row if so.
    #     elif prev_index[1] == 0:
    #         game_map.expand_dungeon("west")
    #
    # def _post_flight_expands(self, game_map):
    #     if game_map.room_index[id(self)][0] == 0:
    #         game_map.expand_dungeon('north')
    #     if game_map.room_index[id(self)][1] == 0:
    #         game_map.expand_dungeon('west')
    #     if game_map.room_index[id(self)][0] == len(game_map.room_array)-1:
    #         game_map.expand_dungeon('south')
    #     if game_map.room_index[id(self)][1] == len(game_map.room_array[0])-1:
    #         game_map.expand_dungeon('east')
    #     pass