import random
import utils

"""
    Rooms will be stored in a 2-dimensional array. The room_index var will be a key-index pair linking a room's ID with
    its location within this array for quick lookup. When the Room Array is updated with a new row or column, the
    room_index will also be updated to reflect changes to existing room's indices.
"""


def check_borders(input_index, width, height, travel_direction):
    # Check to see if the player is at the border of something.
    # If they are leaving the boundaries return True, if not False.
    # This is Zone/Room agnostic.
    if \
            (input_index[0] == 0 and travel_direction == "north") \
            or (input_index[1] == width and travel_direction == "east") \
            or (input_index[0] == height and travel_direction == "south") \
            or (input_index[1] == 0 and travel_direction == "west"):
        return True
    else:
        return False


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

    def show_map(self, player=None):
        known_map = (f"\n")
        for row in self.zone_array:
            known_map = known_map + f"[ "
            for zone in row:
                if zone:
                    if player:
                        if zone == player.room.zone:
                            known_map = known_map + f"[*{zone.zone_type} {self.zone_index[id(zone)][0], self.zone_index[id(zone)][1]}*]"
                        else:
                            known_map = known_map + f"[{zone.zone_type} {self.zone_index[id(zone)][0], self.zone_index[id(zone)][1]}]"
                    else:
                        known_map = known_map + f"[{zone.zone_type} {self.zone_index[id(zone)][0], self.zone_index[id(zone)][1]}]"
                else:
                    known_map = known_map + f"[Unknown]"
            known_map = known_map + f" ]\n"
        return known_map


class Zone:
    # Set up as a dictionary so I can expand it easily later.
    ROOM_OPTIONS = [
        {"name": "Dungeon", "description": "A dank dungeon filled with all sorts of nasty implements."},
        {"name": "Kitchen", "description": "A kitchen where foul and unspeakable cuisines are prepared."},
        {"name": "Library", "description": "A fiendish library stuffed with decaying books filled with the most eldritch secrets."},
        {"name": "Hallway", "description": "A hallway. Even dungeon residents need to get around somehow."},
        {"name": "Armory", "description": "An armory full of rusted and half-broken implements of war."},
        {"name": "Barracks", "description": "This room of cots and storage chests reeks of mildew and mold."},
        {"name": "Storeroom", "description": "This storeroom contains several barrels and boxes filled with rotted meats."},
        {"name": "Laboratory", "description": "Bubbling cauldrons and alembics line the tables of this nefarious workshop."},
        {"name": "Shrine", "description": "There's blood everywhere. So much blood!"},
    ]

    def __init__(self, world_map, travel_direction=None, previous_zone=None, zone_type="Generic"):
        self.world_map = world_map
        self.room_index = dict()
        self.room_array = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.zone_type = zone_type
        self._assign_to_world_map(travel_direction, previous_zone)
        self._spawn_rooms()

    def _assign_to_world_map(self, travel_direction=None, previous_zone=None):
        # create initial Zone.
        if previous_zone is None:
            self.world_map.zone_array[1][1] = self
            self.world_map.zone_index[id(self)] = [1, 1]
        # create new Zones and assign to World Map array and index.
        else:
            prev_zone_index = self.world_map.zone_index[id(previous_zone)]
            # Check to see if the player is exiting the bounds of the existing map. If so expand the map and re-query
            # previous Zone's index.
            world_map_width = len(self.world_map.zone_array[0]) - 1
            world_map_height = len(self.world_map.zone_array) - 1
            if check_borders(prev_zone_index, world_map_width, world_map_height, travel_direction):
                self.world_map.expand_world_map(travel_direction)
                prev_zone_index = self.world_map.zone_index[id(previous_zone)]
            # Assign Zone to World Map Array and Index. If this overlaps with an existing Zone then we fucked up
            # somewhere along the way (i.e. the chain of commands that led to this zone creation is faulty).
            if travel_direction == "north":
                if self.world_map.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]]:
                    raise utils.ZoneAlreadyExists
                else:
                    self.world_map.zone_array[prev_zone_index[0] - 1][prev_zone_index[1]] = self
                    self.world_map.zone_index[id(self)] = [prev_zone_index[0] - 1, prev_zone_index[1]]
            if travel_direction == "east":
                if self.world_map.zone_array[prev_zone_index[0]][prev_zone_index[1] + 1]:
                    raise utils.ZoneAlreadyExists
                else:
                    self.world_map.zone_array[prev_zone_index[0]][prev_zone_index[1] + 1] = self
                    self.world_map.zone_index[id(self)] = [prev_zone_index[0], prev_zone_index[1] + 1]
            if travel_direction == "south":
                if self.world_map.zone_array[prev_zone_index[0] + 1][prev_zone_index[1]]:
                    raise utils.ZoneAlreadyExists
                else:
                    self.world_map.zone_array[prev_zone_index[0] + 1][prev_zone_index[1]] = self
                    self.world_map.zone_index[id(self)] = [prev_zone_index[0] + 1, prev_zone_index[1]]
            if travel_direction == "west":
                if self.world_map.zone_array[prev_zone_index[0]][prev_zone_index[1] - 1]:
                    raise utils.ZoneAlreadyExists
                else:
                    self.world_map.zone_array[prev_zone_index[0]][prev_zone_index[1] - 1] = self
                    self.world_map.zone_index[id(self)] = [prev_zone_index[0], prev_zone_index[1] - 1]

    def _spawn_rooms(self):
        random.shuffle(self.ROOM_OPTIONS)
        i = 0
        j = 0
        # Establish a counter to construct the location within the Zone array for the Room.
        for room in self.ROOM_OPTIONS:
            location = (i, j)
            Room(self, location, room["name"], room["description"])
            j += 1
            if j > 2:
                i += 1
                j = 0

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
        this_zone_index = self.world_map.zone_index[id(self)]
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

    def zone_map(self, player=None):
        zone_map = (f"")
        i = 0
        for row in self.room_array:
            zone_map = zone_map + f"[ "
            for room in row:
                if player:
                    if room == player.room:
                        zone_map = zone_map + f"[*{room.name} {room.zone.room_index[id(room)][0], room.zone.room_index[id(room)][1]}*]"
                    else:
                        zone_map = zone_map + f"[{room.name} {room.zone.room_index[id(room)][0], room.zone.room_index[id(room)][1]}]"
                else:
                    zone_map = zone_map + f"[{room.name} {room.zone.room_index[id(room)][0], room.zone.room_index[id(room)][1]}]"
            zone_map = zone_map + f" ]\n"
        return zone_map


class Room:

    DOORS = {
        "north": 1 << 1,
        "east": 1 << 2,
        "south": 1 << 3,
        "west": 1 << 4,
    }

    def __init__(self, zone, location, name, description, travel_direction=None, previous_room=None):
        self.zone = zone
        self.name = name
        self.description = description
        self.active_doors = list()
        self.doors = [self.DOORS["north"], self.DOORS["east"], self.DOORS["south"], self.DOORS["west"]]
        self._assign_room_to_zone_array(location)
        self._assign_doors()

    # Need to assign room to Zone Array & Index here, so that way we can query neighbors and assign doors appropriately.
    def _assign_room_to_zone_array(self, location):
        self.zone.room_array[location[0]][location[1]] = self
        self.zone.room_index[id(self)] = [location[0], location[1]]

    def query_neighbors_for_doors(self):
        # query neighboring rooms and see if they connect to the currently generating room. If so, create appropriate
        # doors. If they do not, remove the door from the currently generating room's door list so they don't
        # accidentally connect.
        this_room_index = self.zone.room_index[id(self)]
        # Because rooms are defined as null in the 2D list of lists, try to fetch them. If they don't have attributes of
        # doors then simply pass over them.
        # However, because these rooms may abut against other zones, we need to query those regions for their doors too.

        # Starting from a Northern Room and travelling North
        if this_room_index[0] == 0:
            neighboring_zone = self.zone.query_neighbor("north")
            if neighboring_zone:
                north_room_other_zone = neighboring_zone.room_array[len(neighboring_zone.room_array) - 1][this_room_index[1]]
                if north_room_other_zone.DOORS["south"] in north_room_other_zone.active_doors:
                    self.active_doors.append(self.DOORS["north"])
                self.doors.remove(self.DOORS["north"])
        elif this_room_index[0] != 0:
            try:
                north_room = self.zone.room_array[this_room_index[0]-1][this_room_index[1]]
                if north_room.DOORS["south"] in north_room.active_doors:
                    self.active_doors.append(self.DOORS["north"])
                self.doors.remove(self.DOORS["north"])
            except AttributeError:
                pass

        # Starting from an Eastern Room and travelling East.
        if this_room_index[1] == len(self.zone.room_array[0]) - 1:
            neighboring_zone = self.zone.query_neighbor("east")
            if neighboring_zone:
                east_room_other_zone = neighboring_zone.room_array[this_room_index[0]][0]
                if east_room_other_zone.DOORS["west"] in east_room_other_zone.active_doors:
                    self.active_doors.append(self.DOORS["east"])
                self.doors.remove(self.DOORS["east"])
        elif this_room_index[1] < len(self.zone.room_array[0]) - 1:
            try:
                east_room = self.zone.room_array[this_room_index[0]][this_room_index[1]+1]
                if east_room.DOORS["west"] in east_room.active_doors:
                    self.active_doors.append(self.DOORS["east"])
                self.doors.remove(self.DOORS["east"])
            except AttributeError:
                pass

        # Starting from a Southern Room and travelling South.
        if this_room_index[0] == len(self.zone.room_array) - 1:
            neighboring_zone = self.zone.query_neighbor("south")
            if neighboring_zone:
                south_room_other_zone = neighboring_zone.room_array[0][this_room_index[1]]
                if south_room_other_zone.DOORS["north"] in south_room_other_zone.active_doors:
                    self.active_doors.append(self.DOORS["south"])
                self.doors.remove(self.DOORS["south"])
        elif this_room_index[0] < len(self.zone.room_array) - 1:
            try:
                south_room = self.zone.room_array[this_room_index[0] + 1][this_room_index[1]]
                if south_room.DOORS["north"] in south_room.active_doors:
                    self.active_doors.append(self.DOORS["south"])
                self.doors.remove(self.DOORS["south"])
            except AttributeError:
                pass

        # Starting from a Western Room and travelling West.
        if this_room_index[1] == 0:
            neighboring_zone = self.zone.query_neighbor("west")
            if neighboring_zone:
                west_room_other_zone = neighboring_zone.room_array[this_room_index[0]][len(neighboring_zone.room_array[0]) - 1]
                if west_room_other_zone.DOORS["east"] in west_room_other_zone.active_doors:
                    self.active_doors.append(self.DOORS["west"])
                self.doors.remove(self.DOORS["west"])
            pass
        elif this_room_index[1] != 0:
            try:
                west_room = self.zone.room_array[this_room_index[0]][this_room_index[1] - 1]
                if west_room.DOORS["east"] in west_room.active_doors:
                    self.active_doors.append(self.DOORS["west"])
                self.doors.remove(self.DOORS["west"])
            except AttributeError:
                pass

    def _assign_doors(self):
        self.query_neighbors_for_doors()
        if len(self.doors):
            for i in range(random.randint(1, len(self.doors))):
                d = random.choice(self.doors)
                self.active_doors.append(d)
                self.doors.remove(d)
        # Ensure that the first room has all 4 doors.
        # else:
        #     self.active_doors = [d for d in self.doors]
        #     self.doors = []

    def door_list(self):
        door_list = (f"")
        for door in self.active_doors:
            if door == self.DOORS["north"]:
                door_list = door_list + f"There is a door to the (N)orth.\n"
            if door == self.DOORS["east"]:
                door_list = door_list + f"There is a door to the (E)ast.\n"
            if door == self.DOORS["south"]:
                door_list = door_list + f"There is a door to the (S)outh.\n"
            if door == self.DOORS["west"]:
                door_list = door_list + f"There is a door to the (W)est.\n"
        return door_list

    # TODO add door function.
    def add_door(self, direction):
        self.active_doors.append(self.DOORS[direction])
        self.doors.remove(self.DOORS[direction])

    def inspect(self):
        inspection = (
            f"{self.description}\n"
            f"There are {len(self.active_doors)} doors.\n\n"
        )
        inspection = inspection + self.door_list()
        return inspection

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
