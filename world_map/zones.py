import random
from .rooms import *
from errors import ZoneAlreadyExists
from utilities import flatten_two_dimensional_array, check_borders
from algorithms.vose_sort import VoseSort


ZONE_REGISTRY = []


class Zone:

    def __init__(self, world_map, travel_direction=None, previous_zone=None, zone_type=None, monster_list=None):
        super().__init__()
        self.world_map = world_map
        self.room_index = dict()
        self.room_array = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.zone_type = zone_type
        self.monster_list = monster_list
        self.world_map.assign_zone_to_map(self, previous_zone, travel_direction)
        self._spawn_rooms()

    def __init_subclass__(cls, **kwargs):
        # Create a list of tuples that contains the object and zone_type of all Zones (that are subclasses of Zone).
        # Not sure if this only applies to immediate subclasses or works recursively... if I need to do branching
        # inheritance I'll find out!
        if cls not in ZONE_REGISTRY:
            ZONE_REGISTRY.append(cls)
        super().__init_subclass__(**kwargs)

    def _spawn_rooms(self):
        x = 0
        y = 0
        for i in range(9):
            location = (x, y)
            self.ROOM_LIST.alias_generation()(zone=self, location=location)
            y += 1
            if y > 2:
                x += 1
                y = 0

    def assign_room_to_zone_array(self, room, location):
        self.room_array[location[0]][location[1]] = room
        self.room_index[room] = [location[0], location[1]]

    def check_zone_borders(self, room_index, travel_direction):
        zone_width = len(self.room_array) - 1
        zone_height = len(self.room_array[0]) - 1
        return check_borders(room_index, zone_width, zone_height, travel_direction)

    def place_outer_doors(self):
        northern_doors = list()
        southern_doors = list()
        western_doors = list()
        eastern_doors = list()
        for idx, row in enumerate(self.room_array):
            if idx == 0:
                for room in row:
                    if room.DOORS["north"] not in room.active_doors:
                        northern_doors.append(room)
            if idx == len(self.room_array) - 1:
                for room in row:
                    if room.DOORS["south"] not in room.active_doors:
                        southern_doors.append(room)
            for sub_idx, room in row:
                if sub_idx == 0:
                    if room.DOORS["west"] not in room.active_doors:
                        western_doors.append(room)
                if sub_idx == len(self.room_array[0]) - 1:
                    if room.DOORS["east"] not in room.active_doors:
                        eastern_doors.append(room)
        if len(northern_doors) < 1:
            random_northern_room = random.choice(self.room_array[0])
            random_northern_room.add_door("north")
        if len(eastern_doors) < 1:
            random_eastern_room = random.choice(self.room_array[0])
            random_eastern_room.add_door("east")
        if len(southern_doors) < 1:
            random_southern_room = random.choice(self.room_array[0])
            random_southern_room.add_door("south")
        if len(western_doors) < 1:
            random_western_room = random.choice(self.room_array[0])
            random_western_room.add_door("west")

    def query_neighbor(self, direction):
        """Check to see if a neighboring Zone exists in a certain direction.
        :param direction: the direction in relation to this zone that we are looking
        :return: the object of the neighboring Zone if it exists. None if it does not.
        """

        # Query neighboring spaces in WorldMap array to see if there are zones there. If not, create them.
        this_zone_index = self.world_map.zone_index[self]
        if direction == "north":
            if this_zone_index[0] == 0:
                return None
            else:
                try:
                    north_zone = self.world_map.zone_array[this_zone_index[0] - 1][this_zone_index[1]]
                    if north_zone:
                        return north_zone
                    else:
                        return None
                except AttributeError:
                    return None
        if direction == "east":
            if this_zone_index[1] == len(self.world_map.zone_array[0]) - 1:
                return None
            else:
                try:
                    east_zone = self.world_map.zone_array[this_zone_index[0]][this_zone_index[1] + 1]
                    if east_zone:
                        return east_zone
                    else:
                        return None
                except AttributeError:
                    return None
        if direction == "south":
            if this_zone_index[0] == len(self.world_map.zone_array) - 1:
                return None
            else:
                try:
                    south_zone = self.world_map.zone_array[this_zone_index[0] + 1][this_zone_index[1]]
                    if south_zone:
                        return south_zone
                    else:
                        return None
                except AttributeError:
                    return None
        if direction == "west":
            if this_zone_index[1] == 0:
                return None
            else:
                try:
                    west_zone = self.world_map.zone_array[this_zone_index[0]][this_zone_index[1] - 1]
                    if west_zone:
                        return west_zone
                    else:
                        return None
                except AttributeError:
                    return None

    def show_zone_map(self, player=None):
        # get the length of the longest room name to normalize the distance used for the map display.
        width = len(max(flatten_two_dimensional_array(self.room_array), key=len)) + 2
        zone_map = f"Current Zone Map:\n"
        for row in self.room_array:
            zone_map = zone_map + f"["
            for room in row:
                if room == player.room:
                    room_map = f"{room.name}"
                    zone_map += f" [*{room_map:^{width-2}}*] "
                else:
                    if room in player.explored_rooms[self]:
                        room_map = f"{room.name}"
                        zone_map += f" [{room_map:^{width}}] "
                    else:
                        room_map = "?" * (width-4)
                        zone_map += f" [{room_map:^{width}}] "
                        # Remove hashes to enable admin map (shows all spawned rooms in Zone).
                        # room_map = f"{room.name}"
                        # zone_map += f" [{room_map:^{width}}] "
            zone_map += f"]\n"
        player.add_messages(zone_map)

    def __len__(self):
        return len(self.zone_type)

    def __str__(self):
        return f"{self.zone_type}"

    def __repr__(self):
        return f"{self.zone_type}"


class DungeonZone(Zone):

    ROOM_LIST = VoseSort({
        Dungeon: .11,
        Kitchen: .11,
        Library: .11,
        Hallway: .11,
        Armory: .11,
        Barracks: .11,
        StoreRoom: .11,
        Laboratory: .11,
        Shrine: .11,
    })

    def __init__(self, world_map, **kwargs):
        super().__init__(
            world_map=world_map,
            zone_type="Dungeon",
            monster_list=["A", ],
            **kwargs
        )


class LavaZone(Zone):

    ROOM_LIST = VoseSort({
        Hallway: .13,
        StoreRoom: .09,
        LavaTube: .15,
        SteamVent: .14,
        ThermalPool: .15,
        GeodeCathedral: .05,
        ChamberOfAsh: .05,
        MagmaChamber: .07,
        SulfurousWastes: .07,
        BoilingMudPits: .09,
    })

    def __init__(self, world_map, **kwargs):
        super().__init__(
            world_map=world_map,
            zone_type="Lava",
            monster_list=["A", "B"],
            **kwargs,
        )


