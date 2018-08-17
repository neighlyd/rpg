from mapping.movement import movement_index, move_action
from utils import *


def player_actions(player, world_map, invalid_input=None):
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
        attack_of_opportunity(player, choice)
        player.equip_item(choice)
    elif verb == "help":
        show_commands(player)
    elif verb == "move":
        if noun in movement_index:
            attack_of_opportunity(player, choice)
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
