from errors import *
from mapping.mapping import WorldMap, Zone
from actions import player_actions
from mobs import *
from utils import *

# initialization values
player = None
world_map = WorldMap()
starting_zone = Zone(world_map, zone_type="Dungeon")
starting_room = starting_zone.room_array[1][1]
g = Goblin(starting_room)


class Main:
    # test for Python 2
    try:
        input = raw_input
    except NameError:
        pass

    while player is None:
        player = choose_class(player, starting_room)

    try:
        while True:
            clear_screen()
            if player.messages:
                player.print_messages()
                player.messages = None
            player_actions(player, world_map)
            # turn(player, messages)

    except EndGameDied as e:
        print(f"{e.message}")
        pass
    except ZoneAlreadyExists:
        print(f"Zone already exists. The dev done fucked up.")
        pass
    except ZoneCreationError:
        print(f"Zone Creation Error")
        pass
    except RoomDoesNotExist:
        print(f"Room does not exist. The dev done fucked up.")
        pass
    except NotEnoughRoomsInZone:
        print(f"There aren't enough rooms in the Zone List to create this Zone Type.")
        pass
    except ItemNotInDictionary as e:
        print(f"{e.message}")
        pass
    except EndGame:
        pass


if __name__ == "__main__":
    Main()
