import re

from items.items import WEAPON_OPTIONS, ARMOR_OPTIONS
from items.item_classes import Weapon, Armor
from errors import ItemNotInDictionary
from utils import clear_screen


def spawn_item(item_name):
    if item_name in WEAPON_OPTIONS:
        item = WEAPON_OPTIONS[item_name]
        return Weapon(
            item["name"],
            item["description"],
            item["weight"],
            item["price"],
            item["attack_bonus"],
            item["damage_min"],
            item["damage_max"],
            item["special"]
        )
    elif item_name in ARMOR_OPTIONS:
        item = ARMOR_OPTIONS[item_name]
        return Armor(
            item['name'],
            item['description'],
            item['weight'],
            item['price'],
            item['physical_defense'],
            item['slot']
        )
    else:
        error_message = f"{item_name} is not in the item dictionary."
        return ItemNotInDictionary(error_message)


def find_item(item, text_input):
    """
    A function to search user text entry for regex patterns. We first rejoin the text list into a string separated with
    spaces. We then create a regex item using the value entered into the function. We then check to see if the reunified
    string contains this regex pattern. If it does, return this element, if not return None.
    :param item: The regex pattern to be searched for in the string
    :param text_input: The user input list which will need to be rejoined into a space separated string.
    :return: Either the found regex pattern or None.
    """
    text_to_scan = ' '.join(text_input)
    temp_regex = r"\b(" + re.escape(item) + r")\b"
    search = re.search(temp_regex, text_to_scan, re.IGNORECASE)
    if search:
        return search[0]
    else:
        return None


def choose_item_from_list(player, search_term, items):
    while True:
        clear_screen()
        item_list = f""
        for idx, item in enumerate(items):
            item_list += f"{idx + 1}) {item}\n"
        item_list += f"Which {search_term} would you like to choose?"
        try:
            item_choice = int(input(item_list))
        except ValueError:
            continue
        else:
            item_choice -= 1
            if 0 <= item_choice < len(player.inventory.items[search_term.title()]):
                return player.inventory.items[search_term.title()][item_choice]
            else:
                continue


def search_inventory(player, text_input):
    """
    Iterate through a player's inventory dict and see if the text they have entered contains a item that is a key in
    their inventory. If so, return the instance referred to by that key. If not, this function will return None.
    :param player: The player calling the function.
    :param text_input: The user input list. We feed this into find_item() to search it for a regex pattern.
    :return: A tuple containing the list of object instances referenced by the regex pattern found by find_item if the
            item is in the player's inventory or None. In addition, return the discovered regex itself, or None.
    """
    for item in player.inventory.items:
        search_term = find_item(item, text_input)
        if search_term is not None:
            items_in_inventory = player.inventory.items[search_term.title()]
            return items_in_inventory, search_term
    return None, None


def search_room(player, text_input):
    for mob in player.room.mobs:
        search_term = find_item(mob, text_input)
        if search_term is not None:
            return player.room.mobs[search_term.title()], search_term
    return None, None


def equip_action(player, text_input):
    item_to_equip, search_term = search_inventory(player, text_input)
    if item_to_equip:
        if len(item_to_equip) > 1:
            item_to_equip = choose_item_from_list(player, search_term, item_to_equip)
            return equip_item(player, item_to_equip)
        else:
            item_to_equip = item_to_equip[0]
        return equip_item(player, item_to_equip)
    else:
        player.add_messages(f"You do not have one of those.")


def equip_item(player, item):
    swap_message_present = f""
    swap_message_journal = f""
    if isinstance(item, Weapon):
        currently_equipped = player.equipped_weapon.main_hand
        if currently_equipped.name != "Fists":
            swap_message_present += f"Swapping {currently_equipped.name} for {item.name}"
            swap_message_journal += f"Swapped {currently_equipped.name} for {item.name}"
            player.inventory.add_item(currently_equipped)
        else:
            swap_message_present += f"Equipping {item.name}."
            swap_message_journal += f"Equipped {item.name}"
        player.equipped_weapon.main_hand = item
    elif isinstance(item, Armor):
        currently_equipped = player.equipped_armor.chest
        if currently_equipped.name is not None:
            swap_message_present += f"Swapping {currently_equipped.name} for {item.name}"
            swap_message_journal += f"Swapped {currently_equipped.name} for {item.name}"
            player.inventory.add_item(currently_equipped)
        else:
            swap_message_present += f"Equipping {item.name}."
            swap_message_journal += f"Equipped {item.name}"
        player.equipped_armor.chest = item
    player.add_messages(swap_message_present)
    player.journal.add_entry(swap_message_journal)
    player.inventory.remove_item(item)


def inspect_item(player, text_input):
    items_to_inspect, search_term = search_inventory(player, text_input)
    if items_to_inspect:
        if len(items_to_inspect) > 1:
            return choose_item_from_list(player, search_term, items_to_inspect)
        else:
            player.add_messages(f"{items_to_inspect[0]}")
    else:
        mob_to_inspect, search_term = search_room(player, text_input)
        if mob_to_inspect:
            if len(mob_to_inspect) == 1:
                examine_message = (
                    f"You examine the {mob_to_inspect[0].name}\n"
                    f"{mob_to_inspect[0].description}"
                )
                examine_message_journal = (
                    f"You examined a {mob_to_inspect[0].name} in {player.room}."
                    f"{mob_to_inspect[0].description}"
                )

                player.add_messages(examine_message)
                player.journal.add_entry(examine_message_journal)
        else:
            player.add_messages(f"You do not have one of those.")
