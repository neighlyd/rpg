import shutil

from blessings import Terminal

from errors import *
from world_map.world_map import WorldMap
from world_map.zones import DungeonZone
from utilities import turn, health_bar, clear_screen
from mobs.player import choose_class

# TODO: Rename Utils so it doesn't clash with standard library utils.

# initialize terminal
term = Terminal()

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
            # TODO: Implement and check DoT and HoT. Move counter has been moved to player.advance_turn(); Check will
            #   happen there. At end of player turn?
            columns = shutil.get_terminal_size().columns
            with term.location(x=0, y=0):
                print(f"Class: {player.name}")
            with term.location(x=term.width//2):
                print(health_bar(player))
            # Because the stamina can go off of the right side of the window, we pull back the length of both stamina
            # displays and all the needed space (i.e. 10 + 2*(len(stamina)))
            with term.location(x=term.width - (10 + len({player.stamina})*2)):
                print(f"Stamina: {player.stamina}/{player.stamina}")
            print("\n")
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
