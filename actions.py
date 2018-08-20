from mapping.movement import movement_index
from utils import *


def invalid_player_input(player, text_input):
    clear_screen()
    turn(player, ' '.join(text_input))


def turn(player, invalid_input=None):
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
        for idx, mob in player.room.mobs.items():
            action_input += f"There is a {mob[0]} in the room with you.\n"

    if player.room.mob_corpses:
        for idx, corpse in player.room.mob_corpses.items():
            if corpse[0].loot:
                corpse_name = f"{corpse[0]}"
            else:
                corpse_name = f"{corpse[0]} (empty)"
            action_input += f"There is a {corpse_name} in the room with you.\n"

    action_input += (
            f"\n"
            f"{player.room.door_list()}"
            f"\n"
            f"(Type help for assistance)\n"
            f"What would you like to do?"
        )
    text_input = clean_input(action_input)
    verb = first_verb(player, text_input)
    noun = first_noun(player, text_input)
    if verb == "attack":
        player.attack_monster(text_input)
    elif verb == "look":
        if noun:
            if noun == "character" or noun == "stats":
                player.view_stats_header()
            elif noun == "equipment":
                player.view_equipped()
            elif noun == "inventory":
                player.view_inventory()
            elif noun == "journal":
                player.read_journal()
            elif noun == "room":
                player.examine_room()
            elif noun == "turn":
                player.check_turn()
            elif noun == "world":
                player.show_world_map()
            elif noun == "zone" or noun == "map":
                player.show_zone_map()
        else:
            player.examine_object(text_input)
    elif verb == "equip":
        player.equip_item(text_input)
    elif verb == "help":
        show_commands(player)
    elif verb == "loot":
        player.examine_object(text_input)
    elif verb == "move":
        if noun in movement_index:
            player.move_action(noun, text_input)
        else:
            invalid_player_input(player, text_input)
    elif verb == "pet":
        pass
    elif verb == "read":
        if noun == "journal":
            player.read_journal()
    elif noun == "turn":
        player.check_turn()
    elif verb == "quit":
        confirm_exit()
    elif verb == "use":
        pass
    elif noun == "world":
        player.show_world_map()
    elif noun == "zone" or noun == "map":
        player.show_zone_map()
    elif verb == "debug":
        from debug import spawn_monster, kill_monster
        import ipdb
        ipdb.set_trace()
    else:
        invalid_player_input(player, text_input)
