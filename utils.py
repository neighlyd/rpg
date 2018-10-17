import os
from errors import EndGame


def clear_screen():
    """
        Determines whether player is using windows or *nix machine, then issues appropriate clear screen command.
    :return: clear screen command.
    """
    os.system("cls" if os.name == "nt" else "clear")


def clean_input(entry):
    """
        Used to turn a user's input, make it all lower case, and convert to a list. This list is then suitable to be fed
        into the first_verb() and first_noun() functions.
    :param entry: User input.
    :return: Lower-case list of user input.
    """
    user_input = input(entry)
    if user_input:
        return user_input.lower().split(' ')
    else:
        print(f"You must enter something.")
        clean_input(entry)


def minimize_input(entry):
    """
        Used to capture only the lower-case, first letter of a user's input. This output is not suitable for the
        first_verb() and first_noun() functions.
    :param entry: User's input.
    :return: lower-case, first letter of user's input.
    """
    user_input = input(entry)
    if user_input:
        return user_input.lower().lstrip()[0]
    else:
        return user_input


def flatten_two_dimensional_array(array):
    """
        Flattens a 2-dimensional array into a flat list of elements.
    :param array: A 2-dimensional array
    :return: A flat list
    """
    return [item for sublist in array for item in sublist if item is not None]


def check_borders(input_index, width, height, travel_direction):
    """
        Check to see if the player is entering an undefined region of the map. This function is Zone/Room agnostic.
    :param input_index: The index of the player's current Zone/Room
    :param width: The total width of the Zone/Room array that the Zone/Room being checked is in.
    :param height: The total height of the Zone/Room array that the Zone/Room being checked is in.
    :param travel_direction: The direction that the player is travelling.
    :return: True if there is no Zone/Room beyond the current one, False if there is a Zone/Room beyond the current one.
    """
    if \
            (input_index[0] == 0 and travel_direction == "north") \
            or (input_index[1] == width and travel_direction == "east") \
            or (input_index[0] == height and travel_direction == "south") \
            or (input_index[1] == 0 and travel_direction == "west"):
        return True
    else:
        return False


def first_verb(player, entry):
    """
        Searches through action_index dictionary for first verb in user input and returns the normalized value.
    :param entry: User's cleaned input.
    :return: value from action_index dictionary for first verb in user's input.
    """
    if entry:
        for word in entry:
            if word in player.action_index["verbs"]:
                return player.action_index["verbs"][word]


def first_noun(player, entry):
    """
        Searches through action_index dictionary for a noun in user input.
    :param entry: User's cleaned input.
    :return: first noun found in action_index.
    """
    if entry:
        for word in entry:
            if word in player.action_index["nouns"]:
                return word


def confirm_exit():
    """
        Confirms that the player wishes to exit the game.
    :return: EndGame exception to quit the game.
    """
    confirm = minimize_input("Are you sure? (Y/N)")
    if confirm == "y":
        print(f"Thank you for playing.")
        raise EndGame
    else:
        clear_screen()
        pass


def show_commands(player):
    """
        Displays the commands available to a player
    :param player: The player object
    :return: A formatted list of valid commands available to a player.
    """
    commands = (
        f"Combine verbs with nouns from the list below.\n"
        f"You can also use item or monster names in place of nouns.\n"
        f"\n"
    )
    for idx, val in player.action_index.items():
        commands += (
            f"{idx}:\n"
            f"\n"
            f"[ "
        )
        first = True
        for v in val:
            if first:
                commands += f"{v}"
                first = False
            else:
                commands += f", {v}"
        commands += (
            f" ]\n"
            f"\n"
        )
    player.add_messages(commands)
