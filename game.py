from errors import *
from mapping.world_map import WorldMap
from mapping.zones import DungeonZone
from actions import turn
from mobs.player import choose_class
from utils import *

# initialization values
player = None
world_map = WorldMap()
starting_zone = DungeonZone(world_map)
starting_room = starting_zone.room_array[1][1]


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
            """
            TODO: Implement and check DoT and HoT. Move counter has been moved to player.advance_turn(); Check will 
            happen there. At end of player turn?
            """
            if player.messages:
                player.print_messages()
                player.messages = None
            turn(player)

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
