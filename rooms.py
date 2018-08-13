import random


class Room(object):

    NORTH_DOOR = 1 << 1
    EAST_DOOR = 1 << 2
    SOUTH_DOOR = 1 << 3
    WEST_DOOR = 1 << 4

    def __init__(self, entry_direction, game_map, previous_room=None):
        self.name = ""
        self.description = ""
        self.active_doors = list()
        self.doors = [self.NORTH_DOOR, self.EAST_DOOR, self.SOUTH_DOOR, self.WEST_DOOR]
        if previous_room:
            self._assign_room_to_array(entry_direction, game_map, previous_room)
            self._assign_doors(game_map, previous_room)
        else:
            self._assign_room_to_array(entry_direction, game_map)
            self._assign_doors(game_map)

    def _pre_flight_expands(self, game_map, previous_room):
        prev_index = game_map.room_index[id(previous_room)]
        # Check if it is the Northern most room and add new row if so.
        if prev_index[0] == 0:
            game_map.expand_dungeon("north")
        # check if it is Eastern most room and add new row if so.
        elif prev_index[1] == len(game_map.room_array[0]) - 1:
            game_map.expand_dungeon("east")
        # check if it is the Southern most room and add new row if so.
        elif prev_index[0] == len(game_map.room_array) - 1:
            game_map.expand_dungeon("south")
        # check if it is the Western most room and add new row if so.
        elif prev_index[1] == 0:
            game_map.expand_dungeon("west")

    def _post_flight_expands(self, game_map):
        if game_map.room_index[id(self)][0] == 0:
            game_map.expand_dungeon('north')
        if game_map.room_index[id(self)][1] == 0:
            game_map.expand_dungeon('west')
        if game_map.room_index[id(self)][0] == len(game_map.room_array)-1:
            game_map.expand_dungeon('south')
        if game_map.room_index[id(self)][1] == len(game_map.room_array[0])-1:
            game_map.expand_dungeon('east')
        pass

    def _assign_room_to_array(self, entry_direction, game_map, previous_room=None):
        if previous_room is None:
            game_map.room_array[1][1] = self
            game_map.room_index[id(self)] = [1, 1]
        else:
            self._pre_flight_expands(game_map, previous_room)
            prev_index = game_map.room_index[id(previous_room)]
            if entry_direction == "north_door":
                game_map.room_array[prev_index[0]+1][prev_index[1]] = self
                game_map.room_index[id(self)] = [prev_index[0]+1, prev_index[1]]
            elif entry_direction == "east_door":
                game_map.room_array[prev_index[0]][prev_index[1]-1] = self
                game_map.room_index[id(self)] = [prev_index[0], prev_index[1]-1]
            elif entry_direction == "south_door":
                game_map.room_array[prev_index[0]-1][prev_index[1]] = self
                game_map.room_index[id(self)] = [prev_index[0]-1, prev_index[1]]
            elif entry_direction == "west_door":
                game_map.room_array[prev_index[0]][prev_index[1]+1] = self
                game_map.room_index[id(self)] = [prev_index[0], prev_index[1]+1]
            self._post_flight_expands(game_map)
            return

    def query_neighboring_rooms(self, game_map):
        # query neighboring rooms and see if they connect to the currently generating room. If so, create appropriate
        # doors. If they do not, remove the door from the currently generating room's door list so they don't
        # accidentally connect.
        this_room = game_map.room_index[id(self)]
        # Because rooms are defined as null in the 2D list of lists, try to fetch them. If they don't have attributes of
        # doors then simply pass over them.
        try:
            north_room = game_map.room_array[this_room[0]-1][this_room[1]]
            if north_room.SOUTH_DOOR in north_room.active_doors:
                self.active_doors.append(self.NORTH_DOOR)
            self.doors.remove(self.NORTH_DOOR)
        except AttributeError:
            pass
        try:
            east_room = game_map.room_array[this_room[0]][this_room[1]+1]
            if east_room.WEST_DOOR in east_room.active_doors:
                self.active_doors.append(self.EAST_DOOR)
            self.doors.remove(self.EAST_DOOR)
        except AttributeError:
            pass
        try:
            south_room = game_map.room_array[this_room[0]+1][this_room[1]]
            if south_room.NORTH_DOOR in south_room.active_doors:
                self.active_doors.append(self.SOUTH_DOOR)
            self.doors.remove(self.SOUTH_DOOR)
        except AttributeError:
            pass
        try:
            west_room = game_map.room_array[this_room[0]][this_room[1]-1]
            if west_room.EAST_DOOR in west_room.active_doors:
                self.active_doors.append(self.WEST_DOOR)
            self.doors.remove(self.WEST_DOOR)
        except AttributeError:
            pass

    def _assign_doors(self, game_map, previous_room=None):
        # Ensure that the first room has all four doors.
        if previous_room:
            self.query_neighboring_rooms(game_map)
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

    def __init__(self, game_map):
        super().__init__("north_door", game_map)
        self.description = "This is the starting room."
        self.name = "Starting Room"


class OtherRoom(Room):

    def __init__(self, entry_direction, game_map, previous_room ):
        super().__init__(entry_direction, game_map, previous_room)
        self.description = "This is just another room."
        self.name = "Another Room."


class MustyRoom(Room):

    def __init__(self, entry_direction, game_map, previous_room):
        super().__init__(entry_direction, game_map, previous_room)
        self.description = "This is a very musty room."
        self.name = "Musty Room"


class CoffinRoom(Room):

    def __init__(self, entry_direction, game_map, previous_room):
        super().__init__(entry_direction, game_map, previous_room)
        self.description = "This room is filled with coffins; just fuckin' chock fulla' them. You want a coffin? This place has gottem."
        self.name = "Coffin Room"


class CatRoom(Room):

    def __init__(self, entry_direction, game_map, previous_room):
        super().__init__(entry_direction, game_map, previous_room)
        self.description = "This room is nothing but cats. The floor is cats. The seats are cats. Even the oxygen molecules are little tiny kitties."
        self.name = "Cat Room"


class ChinaRoom(Room):

    def __init__(self, entry_direction, game_map, previous_room):
        super().__init__(entry_direction, game_map, previous_room)
        self.description = "This room is filled with priceless china. Please be careFUL-OHFUCKING GOD DAMN IT!."
        self.name = "China Room"




