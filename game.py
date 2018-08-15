from character_classes import *
from mapping import WorldMap, Zone, check_borders
from utils import *
from items.weapons import *
from items.armor import *

player = None
world_map = WorldMap()
starting_zone = Zone(world_map)
starting_room = starting_zone.room_array[1][1]
first_turn = True
movement_index = {
    "n": 1 << 1,
    "e": 1 << 2,
    "s": 1 << 3,
    "w": 1 << 4
}
direction_index = {
    "n": "North",
    "e": "East",
    "s": "South",
    "w": "West"
}
journal = [f"You began your journey in {starting_room.name}\n"]


def update_journal(room, new_room, direction):
    global journal
    journal.append(f"You travelled {direction_index[direction]} from {room.name} to {new_room.name}.\n")


def read_journal():
    global journal
    journal_entries = (f"\n")
    for row in journal:
        journal_entries = journal_entries + row
    return journal_entries


def list_commands():
    commands = (
        f"(A)ttack Monster\n"
        f"(I)nspect Room\n"
        f"(M)ove\n"
        f"(C)haracter Sheet\n"
        f"(H)elp\n"
        f"(Q)uit\n"
    )
    clear_screen()
    return print(commands)


def choose_class(player):
    clear_screen()
    class_choice = clean_input(f"What class would you like to be?\nType either (F)ighter or (W)izard:")
    if class_choice == "f":
        player = Fighter(starting_room)
        player.inventory.add_item(RustySword())
        player.inventory.add_item(RoughSpunTunic())
    elif class_choice == "w":
        player = Wizard(starting_room)
        player.inventory.add_item(WalkingStaff())
        player.inventory.add_item(RoughSpunRobe())
    choice = (
        f"############################\n"
        f"You have chosen {player.name}.\n"
        f"{player.list_stats()}\n"
        f"{player.current_hp()} hp.\n"
        f"############################\n"
    )
    clear_screen()
    print(choice)
    final = clean_input(f"Would you like to keep this class? (Y/N)")
    if final == 'n':
        clear_screen()
        player = None
    else:
        clear_screen()
        return player


def move_choice(player, room, monster=None):
    clear_screen()
    # if monster:
    #     print(f"You can't leave the room while the {monster.name} still draws breath!")
    #     return
    # else:
    print(f"{room.door_list()}")
    choice = clean_input(f"Which door would you like to go through?")
    if choice in movement_index:
        move_action(player, choice)
    else:
        pass


def move_action(player, choice):
    if movement_index[choice] in player.room.active_doors:
        this_room_index = player.room.zone.room_index[id(player.room)]
        zone_width = len(player.room.zone.room_array) - 1
        zone_height = len(player.room.zone.room_array) - 1
        # See if the player is leaving the Zone. If not, simply move them to the next room in the Zone array.
        if check_borders(this_room_index, zone_width, zone_height, choice):
            # Check to see if a Zone exists in the direction that the player is travelling.
            neighboring_zone = player.room.zone.query_neighbor(choice)
            if not neighboring_zone:
                # Create a new Zone if one doesn't exist.
                neighboring_zone = Zone(world_map, choice, player.room.zone)
            # Move player to new Room in new Zone.
            if choice == "n":
                new_room = neighboring_zone.room_array[len(neighboring_zone.room_array) - 1][this_room_index[1]]
            if choice == "e":
                new_room = neighboring_zone.room_array[this_room_index[0]][0]
            if choice == "s":
                new_room = neighboring_zone.room_array[0][this_room_index[1]]
            if choice == "w":
                new_room = neighboring_zone.room_array[this_room_index[0]][len(neighboring_zone.room_array[0]) - 1]
        # If player is staying in the same Zone, assign to room as needed.
        else:
            if choice == "n":
                if player.room.zone.room_array[this_room_index[0] - 1][this_room_index[1]]:
                    new_room = player.room.zone.room_array[this_room_index[0] - 1][this_room_index[1]]
                else:
                    raise RoomDoesNotExist
            elif choice == "e":
                if player.room.zone.room_array[this_room_index[0]][this_room_index[1] + 1]:
                    new_room = player.room.zone.room_array[this_room_index[0]][this_room_index[1] + 1]
                else:
                    raise RoomDoesNotExist
            elif choice == "s":
                if player.room.zone.room_array[this_room_index[0] + 1][this_room_index[1]]:
                    new_room = player.room.zone.room_array[this_room_index[0] + 1][this_room_index[1]]
                else:
                    raise RoomDoesNotExist
            elif choice == "w":
                if player.room.zone.room_array[this_room_index[0]][this_room_index[1] - 1]:
                    new_room = player.room.zone.room_array[this_room_index[0]][this_room_index[1] - 1]
                else:
                    raise RoomDoesNotExist
        update_journal(player.room, new_room, choice)
        player.room = new_room
        clear_screen()
    else:
        clear_screen()
        print(f"You run into a wall.\n")
        journal.append(f"You ran into a wall in {player.room.name}\n")
# def player_attack(player, monster):
#     clear_screen()
#     atk = player.attack()
#     print(f"{atk[1]}")
#     if atk[0] >= monster.ac:
#         dmg = player.damage()
#         monster.hp = monster.hp - dmg
#         print(f"You hit the {monster} for {dmg}, leaving it with {monster.hp} hp left.\n")
#     else:
#         print(f"You miss.\n")
#
#
# def monster_attack(player, monster):
#     atk = monster.attack()
#     print(f"The {monster} attacks you.")
#     print(f"{atk[1]}")
#     if atk[0] >= player.ac:
#         dmg = monster.damage()
#         player.hp = player.hp - dmg
#         print(f"The {monster} hit you for {dmg}, leaving you with {player.hp} hp left.\n")
#         if player.hp <= 0:
#             raise EndGameDied
#     else:
#         print(f"The {monster} swung at you and missed.")
#
#
# def combat(player):
#     monster = Goblin()
#     monster_init = monster.initiative()
#     player_init = player.initiative()
#     while player.hp > 0 or monster.hp > 0:
#         # TODO: Implement initiative and monster attacks.
#         if player_init >= monster_init:
#             print(f"You see a {monster} before you.\n")
#             player_actions(player, monster)
#             monster_attack(player, monster)
#         elif monster_init > player_init:
#             print(f"You see a {monster} before you. It got the drop on you.\n")
#             monster_attack(player, monster)
#             player_actions(player, monster)
#         if player.hp <= 0:
#             print(f"You died.")
#             break
#         if monster.hp <= 0:
#             player.xp = player.xp + monster.xp
#             print(f"You killed the {monster} and received {monster.xp} xp. You now have {player.xp} xp.\n")
#             break


def turn(player):
    if player.room.name.startswith(("a", "A", "e", "E", "i", "I", "o", "O", "u", "U")):
        print(f"You are in the {player.room.name}\n")
    else:
        print(f"You are in a {player.room.name}\n")
    print(player.room.inspect())
    player_actions(player)


def inspect(player):
    clear_screen()
    print(player.room.inspect())


def player_actions(player):
    action_input = (
        f"(Type (H)elp for assistance)\n"
        f"What would you like to do?"
    )
    choice = clean_input(action_input)
    if choice == "a":
        # player_attack(player, monster)
        print(f"Combat pending.")
    elif choice == "i":
        inspect(player)
    elif choice == "c":
        clear_screen()
        print(f"{player.list_stats()}")
    elif choice == "u":
        clear_screen()
        print(f"{player.inventory.__str__()}")
        print(f"{player.equipped_armor.__str__()}")
    elif choice == "h":
        list_commands()
    elif choice == "m":
        move_choice(player)
    elif choice == "q":
        print(f"Thank you for playing.")
        raise EndGame
    elif choice == "n" or choice == "e" or choice == "s" or choice == "w":
        move_action(player, choice)
    elif choice == "p":
        clear_screen()
        print(f"Known World Map:\n")
        print(f"{world_map.show_map(player)}")
    elif choice == "z":
        clear_screen()
        print(f"Current Zone Map:\n")
        print(f"{player.room.zone.zone_map(player)}")
    elif choice == "x":
        clear_screen()
        print(f"{player.room.zone.room_index}")
    elif choice == "j":
        clear_screen()
        print(read_journal())


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
            turn(player)
            # combat(player)

    except EndGameDied:
        pass
    except ZoneAlreadyExists:
        print(f"A Zone Already Exists In This Location.")
        pass
    except ZoneCreationError:
        print(f"Zone Creation Error.")
        pass
    except RoomDoesNotExist:
        print(f"A Room Does Not Exist In This Location.")
        pass
    except EndGame:
        pass


if __name__ == "__main__":
    Main()
