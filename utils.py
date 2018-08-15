import os


action_index = {
    "verbs": [
        "attack",
        "check",
        "equip",
        "examine",
        "help",
        "inspect",
        "look",
        "move",
        "quit",
        "use",
    ],
    "nouns": [
        "character",
        "east",
        "equipment",
        "inventory",
        "journal",
        "map",
        "monster",
        "north",
        "room",
        "south",
        "west",
        "world",
        "zone",
    ]
}


class EndGame(Exception):
    pass


class EndGameDied(EndGame):
    pass


class ZoneAlreadyExists(EndGame):
    pass


class ZoneCreationError(EndGame):
    pass


class RoomDoesNotExist(EndGame):
    pass


def clear_screen():
    # Command to clear screen
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
    return user_input.lower().lstrip()[0]


def first_verb(entry):
    """
    Return first verb in user input.
    :param entry: User's cleaned input.
    :return: first verb found in action_index.
    """
    for word in entry:
        if word in action_index["verbs"]:
            return word


def first_noun(entry, player):
    """
    Return first noun in user input.
    :param entry: User's cleaned input.
    :return: first noun found in action_index.
    """
    for word in entry:
        if word in action_index["nouns"]:
            return word
