import random
from game import world_map


class Room(object):

    NORTH_DOOR = 1 << 1
    EAST_DOOR = 1 << 2
    SOUTH_DOOR = 1 << 3
    WEST_DOOR = 1 << 4

    def __init__(self, travel_direction=None, zone=None, previous_room=None):
        self.zone = None
        self.name = ""
        self.description = ""
        self.active_doors = list()
        self.doors = [self.NORTH_DOOR, self.EAST_DOOR, self.SOUTH_DOOR, self.WEST_DOOR]
        if previous_room:
            self._assign_room_to_zone_array(travel_direction, previous_room)
            self._assign_doors(zone, previous_room)
        else:
            self._assign_room_to_zone_array(travel_direction)
            self._assign_doors(zone)

    def _assign_room_to_zone_array(self, travel_direction=None, previous_room=None):
        # create starting room in starting zone.
        if previous_room is None:
            self.zone = world_map.zone_index[0]
            self.zone.room_array[1][1] = self
            self.zone.room_index[id(self)] = [1, 1]
        else:
            # check the index location of where player is coming from to see if they will be a new Zone or staying in
            # their current one.
            prev_room_index = previous_room.zone.room_index[id(previous_room)]
            # if the player is staying in the same Zone, assign this room to the same Zone, add it to that Zone's index
            # and array.
            if (prev_room_index[0] != 0 and travel_direction == "north") \
                    or (prev_room_index[1] != 2 and travel_direction == "east") \
                    or (prev_room_index[0] != 2 and travel_direction == "south") \
                    or (prev_room_index[1] != 0 and travel_direction == "west"):
                self.zone = previous_room.zone
                if travel_direction == "north":
                    self.zone.room_array[prev_room_index[0] - 1][prev_room_index[1]] = self
                    self.zone.room_index[id(self)] = [prev_room_index[0] - 1, prev_room_index[1]]
                elif travel_direction == "east":
                    self.zone.room_array[prev_room_index[0]][prev_room_index[1] + 1] = self
                    self.zone.room_index[id(self)] = [prev_room_index[0], prev_room_index[1] + 1]
                elif travel_direction == "south":
                    self.zone.room_array[prev_room_index[0] + 1][prev_room_index[1]] = self
                    self.zone.room_index[id(self)] = [prev_room_index[0] + 1, prev_room_index[1]]
                elif travel_direction == "west":
                    self.zone.room_array[prev_room_index[0]][prev_room_index[1] - 1] = self
                    self.zone.room_index[id(self)] = [prev_room_index[0], prev_room_index[1] - 1]
            # If the player is entering a new zone, check to see if the zone exists. If not, create it.
            else:
                if prev_room_index[0] == 0 and travel_direction == "north":
                    north_zone_index = previous_room.zone.query_neighbor("north")
                    if north_zone_index:
                        self.zone = world_map.zone_array[north_zone_index[0]-1][north_zone_index[1]]
                        # Assign room to Zone Array and Index.
                    else:
                        world_map.expand_dungeon("north")
                        # Expand WorldMap by creating zone and returning its ID.
                        pass

            return

    def query_neighboring_rooms(self, zone):
        # query neighboring rooms and see if they connect to the currently generating room. If so, create appropriate
        # doors. If they do not, remove the door from the currently generating room's door list so they don't
        # accidentally connect.
        this_room = zone.room_index[id(self)]
        # Because rooms are defined as null in the 2D list of lists, try to fetch them. If they don't have attributes of
        # doors then simply pass over them.
        try:
            north_room = zone.room_array[this_room[0] - 1][this_room[1]]
            if north_room.SOUTH_DOOR in north_room.active_doors:
                self.active_doors.append(self.NORTH_DOOR)
            self.doors.remove(self.NORTH_DOOR)
        except AttributeError:
            pass
        try:
            east_room = zone.room_array[this_room[0]][this_room[1] + 1]
            if east_room.WEST_DOOR in east_room.active_doors:
                self.active_doors.append(self.EAST_DOOR)
            self.doors.remove(self.EAST_DOOR)
        except AttributeError:
            pass
        try:
            south_room = zone.room_array[this_room[0] + 1][this_room[1]]
            if south_room.NORTH_DOOR in south_room.active_doors:
                self.active_doors.append(self.SOUTH_DOOR)
            self.doors.remove(self.SOUTH_DOOR)
        except AttributeError:
            pass
        try:
            west_room = zone.room_array[this_room[0]][this_room[1] - 1]
            if west_room.EAST_DOOR in west_room.active_doors:
                self.active_doors.append(self.WEST_DOOR)
            self.doors.remove(self.WEST_DOOR)
        except AttributeError:
            pass

    def _assign_doors(self, zone, previous_room=None):
        # Ensure that the first room has all four doors.
        if previous_room:
            self.query_neighboring_rooms(zone)
            if len(self.doors):
                for i in range(random.randint(1, len(self.doors))):
                    d = random.choice(self.doors)
                    self.active_doors.append(d)
                    self.doors.remove(d)
        else:
            self.active_doors = [d for d in self.doors]
            self.doors = []

    def door_list(self):
        door_list = (f"")
        for door in self.active_doors:
            if door == self.NORTH_DOOR:
                door_list = door_list + f"There is a door to the (N)orth.\n"
            if door == self.EAST_DOOR:
                door_list = door_list + f"There is a door to the (E)ast.\n"
            if door == self.SOUTH_DOOR:
                door_list = door_list + f"There is a door to the (S)outh.\n"
            if door == self.WEST_DOOR:
                door_list = door_list + f"There is a door to the (W)est.\n"
        return door_list

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


class StartingRoom(Room):

    def __init__(self, zone):
        super().__init__("north", zone)
        self.description = "This is the starting room."
        self.name = "Starting Room"


class OtherRoom(Room):

    def __init__(self, travel_direction, zone, previous_room):
        super().__init__(travel_direction, zone, previous_room)
        self.description = "This is just another room."
        self.name = "Another Room."


class MustyRoom(Room):

    def __init__(self, travel_direction, zone, previous_room):
        super().__init__(travel_direction, zone, previous_room)
        self.description = "This is a very musty room."
        self.name = "Musty Room"


class CoffinRoom(Room):

    def __init__(self, travel_direction, zone, previous_room):
        super().__init__(travel_direction, zone, previous_room)
        self.description = "This room is filled with coffins; just fuckin' chock fulla' them. You want a coffin? This place has gottem."
        self.name = "Coffin Room"


class CatRoom(Room):

    def __init__(self, travel_direction, zone, previous_room):
        super().__init__(travel_direction, zone, previous_room)
        self.description = "This room is nothing but cats. The floor is cats. The seats are cats. Even the oxygen molecules are little tiny kitties."
        self.name = "Cat Room"


class ChinaRoom(Room):

    def __init__(self, travel_direction, zone, previous_room):
        super().__init__(travel_direction, zone, previous_room)
        self.description = "This room is filled with priceless china. Please be careFUL-OHFUCKING GOD DAMN IT!."
        self.name = "China Room"




