from .armor import Armor
from .weapons import Weapon
from examine import search, choose_item_from_list


def equip_action(player, text_input):
    item_to_equip, search_term = search(player, text_input, "inventory.items")
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