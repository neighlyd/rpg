import re
import operator

from utils import clear_screen


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
    regex_search = re.search(temp_regex, text_to_scan, re.IGNORECASE)
    if regex_search:
        return regex_search[0]
    else:
        return None


def recurse_search_terms(obj, search_scope):
    if not search_scope:
        return obj
    else:
        first_item = search_scope[0]
        search_level = getattr(obj, first_item)
        return recurse_search_terms(search_level, search_scope[1:])


def search(player, text_input, search_scope):
    search_depth = search_scope.split('.')
    thing_to_search = recurse_search_terms(player, search_depth)
    if thing_to_search:
        for scope in thing_to_search:
            search_term = find_item(scope, text_input)
            if search_term is not None:
                return thing_to_search[search_term.title()], search_term
    return None, ''


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


def examine_object(player, text_input):
    search_terms = dict()
    items_to_inspect, search_terms["item"] = search(player, text_input, "inventory.items")
    mob_to_inspect, search_terms["mob"] = search(player, text_input, "room.mobs")
    corpse_to_inspect, search_terms["corpse"] = search(player, text_input, "room.mob_corpses")
    longest_search_term = max(search_terms.items(), key=operator.itemgetter(1))[0]
    if longest_search_term == "item" and len(search_terms["item"]) > 0:
        if items_to_inspect:
            if len(items_to_inspect) > 1:
                item_list = f""
                for item in enumerate(items_to_inspect):
                    item_list += f"{item[1]}\n"
                player.add_messages(item_list)
            else:
                player.add_messages(f"{items_to_inspect[0]}")
    elif longest_search_term == "mob"and len(search_terms["mob"]) > 0:
        if mob_to_inspect:
            examine_message = (
                f"You examine the {mob_to_inspect[0].name}.\n"
                f"{mob_to_inspect[0].description}"
            )
            examine_message_journal = (
                f"You examined the {mob_to_inspect[0].name} in {player.room}.\n"
                f"{mob_to_inspect[0].description}"
            )
            player.add_messages(examine_message)
            player.journal.add_entry(examine_message_journal)
    elif longest_search_term == "corpse"and len(search_terms["corpse"]) > 0:
        if corpse_to_inspect:
            corpse = player.room.mob_corpses[search_terms["corpse"].title()][0]
            corpse.loot_corpse(player)
    else:
        player.add_messages(f"You do not see one of those.")
