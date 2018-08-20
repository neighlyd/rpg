import random
from mobs.monsters import Bat, Goblin, Orc

MONSTER_OPTIONS = {
    "A": [(Goblin, 15), (Bat, 45)],
    "B": [(Orc, 5)],
}

ROOM_REGISTRY = []


class Room:

    DOORS = {
        "north": 1 << 1,
        "east": 1 << 2,
        "south": 1 << 3,
        "west": 1 << 4,
    }

    def __init__(self, name, description, zone=None, location=None, monster_list=None,
                 travel_direction=None, previous_room=None):
        self.zone = zone
        self.name = name
        self.description = description
        self.monster_list = monster_list
        self.active_doors = list()
        self.doors = [self.DOORS["north"], self.DOORS["east"], self.DOORS["south"], self.DOORS["west"]]
        self.mobs = dict()
        self.mob_corpses = dict()
        self._assign_room_to_zone_array(location)
        self._assign_doors()
        self._spawn_monster()

    def __init_subclass__(cls, **kwargs):
        # See Zone __init_subclass__ for explanation.
        if cls not in ROOM_REGISTRY:
            try:
                ROOM_REGISTRY.append((cls, cls.zone_list))
            except AttributeError:
                ROOM_REGISTRY.append((cls, ["Generic"]))
        super().__init_subclass__(**kwargs)

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

    def _spawn_monster(self, monster=None):
        if not monster:
            if self.monster_list:
                for opt in self.monster_list:
                    for mob in MONSTER_OPTIONS[opt]:
                        if mob[1] != 100:
                            if random.randint(1, 100) <= mob[1]:
                                return mob[0](self)
                        else:
                            return mob[0](self)
            # If rare monsters don't spawn, check to see if the Zone monsters still spawn.
            for opt in self.zone.monster_list:
                for mob in MONSTER_OPTIONS[opt]:
                    if mob[1] != 100:
                        if random.randint(1, 100) <= mob[1]:
                            return mob[0](self)
                    else:
                        return mob[0](self)
        else:
            if monster == "bat":
                return Bat(self)
            elif monster == "goblin":
                return Goblin(self)
            elif monster == "orc":
                return Orc(self)

    def door_list(self):
        door_list = f""
        for door in self.active_doors:
            if door == self.DOORS["north"]:
                door_list += f"There is a door to the North.\n"
            if door == self.DOORS["east"]:
                door_list += f"There is a door to the East.\n"
            if door == self.DOORS["south"]:
                door_list += f"There is a door to the South.\n"
            if door == self.DOORS["west"]:
                door_list += f"There is a door to the West.\n"
        return door_list

    def add_door(self, direction):
        self.active_doors.append(self.DOORS[direction])
        self.doors.remove(self.DOORS[direction])

    def examine(self):
        examination = (
            f"{self.description}\n"
            f"\n"
        )
        examination = examination + self.door_list()
        return examination

    def __len__(self):
        return len(self.name)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Dungeon(Room):

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Dungeon",
            description="A dank dungeon filled with all sorts of nasty implements.",
            monster_list=["B"]
        )


class Kitchen(Room):

    zone_list = ["Dungeon", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Kitchen",
            description="A kitchen where foul and unspeakable cuisines are prepared.",
        )


class Library(Room):

    zone_list = ["Dungeon", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Library",
            description="A fiendish library stuffed with decaying books filled with the most eldritch secrets.",

        )


class Hallway(Room):

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Hallway",
            description="A hallway. Even dungeon residents need to get around somehow."
        )


class Armory(Room):

    zone_list = ["Dungeon", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Armory",
            description="An armory full of rusted, half-broken, and crude implements of war.",

            monster_list=["B"],
        )


class Barracks(Room):

    zone_list = ["Dungeon", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Barracks",
            description="This room of cots and storage chests reeks of mildew and mold.",
            monster_list=["B", ]
        )


class StoreRoom(Room):

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Store Room",
            description="This storeroom contains several barrels and boxes filled with rotted meats.",
        )


class Laboratory(Room):

    zone_list = ["Dungeon", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Laboratory",
            description="Bubbling cauldrons and alembics line the tables of this nefarious workshop.",

        )


class Shrine(Room):

    zone_list = ["Dungeon", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Shrine",
            description="There's blood everywhere. So much blood!",
        )


class LavaTube(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Lava Tube",
            description=("A naturally formed corridor stretches out before you caused by a flow of molten rock that "
                         "once moved beneath the hardened surface of a lava flow. The lava is long gone, but the "
                         "extreme heat of this place is nevertheless unnerving.")
        )


class SteamVent(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Steam Vent",
            description=("You hear this chamber before you see it. A low hissing fills the cavern, increasing in volume"
                         " as you approach. Inside it’s almost deafening. Steam pours out of cracks in the walls and"
                         " floor around which bioluminescent blue lichen has grown.")
        )


class ThermalPool(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Thermal Pool",
            description="This chamber is filled with large steaming pools of water."
        )


class GeodeCathedral(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Geode Cathedral",
            description=(
                "An absolutely dazzling array of shimmering geodes line this room, covering it from floor to ceiling in"
                " a sparkling purple hue.")
        )


class ChamberOfAsh(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Chamber of Ash",
            description=(
                "You come upon a vast chamber that stretches upward far beyond your feeble torch. The air inside "
                "is so still it makes you want to scream just to break the pressure on your ears, but when you open "
                "your mouth the sound dies in your throat. As you step inside your feet sink into what feels like snow"
                ".")
        )


class MagmaChamber(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Magma Chamber",
            description=("This room glows bright orange with the light of living rock. Rivers of molten lava course "
                         "dangerously through the space. It's best to "
                         "watch your step.")
        )


class SulfurousWastes(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Sulfurous Wastes",
            description=("This expanse of yellowed and soiled ground is permeated with the most obscene stench you have"
                         " encountered. Deviled eggs? More like devil eggs!")
        )


class BoilingMudPits(Room):

    zone_list = ["Lava", ]

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name="Boiling Mud Pits",
            description=("Vats of stinking, roiling mud dot the floor of this chamber, occasionally lobbing scorching "
                         "globules at unwary travellers.")
        )
