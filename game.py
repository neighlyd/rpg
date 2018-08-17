from errors import *
from mapping.mapping import WorldMap, Zone
from mapping.movement import movement_index, move_action
from mobs import *
from utils import *
from items import spawn_item

player = None
world_map = WorldMap()
starting_zone = Zone(world_map, zone_type="Dungeon")
starting_room = starting_zone.room_array[1][1]
g = spawn_mob("Goblin", starting_room)
messages = None


def list_commands(player):
    commands = (
        f"Combine verbs with nouns from the list below.\n"
        f"You can also use item or monster names in place of nouns.\n"
        f"\n"
    )
    for idx, val in action_index.items():
        commands += (
            f"{idx}:\n"
            f"\n"
            f"[ "
        )
        i = 0
        for v in val:
            if i == 0:
                commands += f"{v}"
            else:
                commands += f", {v}"
            i += 1
        commands += (
            f" ]\n"
            f"\n"
        )
    player.add_messages(commands)


def choose_class(player):
    clear_screen()
    class_choice = minimize_input(f"What class would you like to be?\nType either (F)ighter or (W)izard:")
    if class_choice == "f":
        player = Fighter(starting_room)
    elif class_choice == "w":
        player = Wizard(starting_room)
    choice = (
        f"############################\n"
        f"You have chosen {player.name}.\n"
        f"{player.view_starting_stats()}\n"
        f"############################\n"
    )
    player.inventory.add_item(spawn_item("Rusty Dagger"))
    clear_screen()
    print(choice)
    final = minimize_input(f"Would you like to keep this class? (Y/N)")
    if final == "n":
        clear_screen()
        player = None
    else:
        clear_screen()
        player.journal.initialize_journal(starting_room)
        return player


def player_actions(player, invalid_input=None):
    if player.room.name.startswith(("a", "A", "e", "E", "i", "I", "o", "O", "u", "U")):
        definite_article = 'the'
    else:
        definite_article = 'a'

    action_input = f""

    if invalid_input:
        action_input += (
            f"'{invalid_input}' is an invalid choice.\n"
            f"\n"
        )

    action_input += (
            f"You are in {definite_article} {player.room.name}\n"
    )

    if player.room.mobs:
        for mob in player.room.mobs:
            action_input += f"There is a {mob} in the room with you.\n"

    action_input += (
            f"\n"
            f"{player.room.door_list()}"
            f"\n"
            f"(Type help for assistance)\n"
            f"What would you like to do?"
        )
    choice = clean_input(action_input)
    verb = first_verb(choice)
    noun = first_noun(choice)
    if verb == "attack":
        # player_attack(player, monster)
        player.add_messages(f"Combat pending.")
    elif verb == "look":
        if noun:
            if noun == "character" or noun == "stats":
                player.view_stats()
            elif noun == "equipment":
                player.view_equipped()
            elif noun == "inventory":
                player.view_inventory()
                pass
            elif noun == "journal":
                player.read_journal()
            elif noun == "monster":
                pass
            elif noun == "room":
                player.inspect_room()
            elif noun == "world":
                player.show_world_map()
            elif noun == "zone" or noun == "map":
                player.show_zone_map()
        else:
            player.inspect_item(choice)
    elif verb == "equip":
        if attack_of_opportunity(player, choice):
            player.equip_item(choice)
        else:
            player.equip_item(choice)
    elif verb == "help":
        list_commands(player)
    elif verb == "move":
        if noun in movement_index:
            move_action(player, noun, world_map)
        else:
            player_actions(player, ' '.join(choice))
    elif verb == "read":
        if noun == "journal":
            player.read_journal()
    elif verb == "quit":
        confirm_exit()
    elif verb == "use":
        pass
    elif noun == "world":
        player.show_world_map()
    elif noun == "zone" or noun == "map":
        player.show_zone_map()
    else:
        clear_screen()
        player_actions(player, ' '.join(choice))


class Main:
    # test for Python 2
    try:
        input = raw_input
    except NameError:
        pass

    while player is None:
        player = choose_class(player)

    try:
        while True:
            clear_screen()
            if player.messages:
                player.print_messages()
                player.messages = None
            player_actions(player)
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
