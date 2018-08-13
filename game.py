from character_classes import *
from monsters import *
from world_map import WorldMap
from rooms import *
from utils import *
import random

player = None
world_map = WorldMap()
starting_room = StartingRoom(world_map)
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
ROOM_OPTIONS = (OtherRoom, MustyRoom, CoffinRoom, CatRoom, ChinaRoom,)
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
    elif class_choice == "w":
        player = Wizard(starting_room)
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
    current_room = player.room
    monster = Goblin(current_room)
    print(f"You are in a {current_room.name}\n")
    print(player.room.inspect())
    player_actions(player, current_room, monster)


def move_action(player, room, choice):
    room_choice = random.choice(ROOM_OPTIONS)
    if movement_index[choice] in room.active_doors:
        this_room_index = world_map.room_index[id(room)]
        if choice == "n":
            if world_map.room_array[this_room_index[0] - 1][this_room_index[1]]:
                new_room = world_map.room_array[this_room_index[0] - 1][this_room_index[1]]
            else:
                new_room = room_choice("south_door", world_map, room)
        elif choice == "e":
            if world_map.room_array[this_room_index[0]][this_room_index[1] + 1]:
                new_room = world_map.room_array[this_room_index[0]][this_room_index[1] + 1]
            else:
                new_room = room_choice("west_door", world_map, room)
        elif choice == "s":
            if world_map.room_array[this_room_index[0] + 1][this_room_index[1]]:
                new_room = world_map.room_array[this_room_index[0] + 1][this_room_index[1]]
            else:
                new_room = room_choice("north_door", world_map, room)
        elif choice == "w":
            if world_map.room_array[this_room_index[0]][this_room_index[1] - 1]:
                new_room = world_map.room_array[this_room_index[0]][this_room_index[1] - 1]
            else:
                new_room = room_choice("east_door", world_map, room)
        update_journal(room, new_room, choice)
        player.room = new_room
        clear_screen()
    else:
        clear_screen()
        print(f"You run into a wall.\n")
        journal.append(f"You ran into a wall in {room}\n")


def move_choice(player, room, monster=None):
    clear_screen()
    # if monster:
    #     print(f"You can't leave the room while the {monster.name} still draws breath!")
    #     return
    # else:
    print(f"{room.door_list()}")
    choice = clean_input(f"Which door would you like to go through?")
    if choice == "n" or choice == "e" or choice == "s" or choice == "w":
        move_action(player, room, choice)
    else:
        pass


def inspect(player, monster):
    clear_screen()
    print(player.room.inspect())


def player_actions(player, room, monster):
    action_input = (
        f"(Type (H)elp for assistance)\n"
        f"What would you like to do?"
    )
    choice = clean_input(action_input)
    if choice == "a":
        # player_attack(player, monster)
        print(f"Combat pending.")
    elif choice == "i":
        inspect(player, monster)
    elif choice == "c":
        clear_screen()
        print(f"{player.list_stats()}")
    elif choice == "h":
        list_commands()
    elif choice == "m":
        move_choice(player, room, monster)
    elif choice == "q":
        print(f"Thank you for playing.")
        raise EndGame
    elif choice == "n" or choice == "e" or choice == "s" or choice == "w":
        move_action(player, room, choice)
    elif choice == "z":
        print(f"{world_map._show_map()}")
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
        print(f"You died.")
        pass
    except EndGame:
        pass


if __name__ == "__main__":
    Main()
