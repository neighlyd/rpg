import os

from commands import action_index
from errors import EndGame, EndGameDied


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
    if user_input:
        return user_input.lower().lstrip()[0]
    else:
        return user_input


def flatten_two_dimensional_array(array):
    return [item for sublist in array for item in sublist if item is not None]


def first_verb(entry):
    """
    Return action for first verb in user input.
    :param entry: User's cleaned input.
    :return: action for first verb found in action_index.
    """
    for word in entry:
        if word in action_index["verbs"]:
            return action_index["verbs"][word]


def first_noun(entry):
    """
    Return first noun in user input.
    :param entry: User's cleaned input.
    :return: first noun found in action_index.
    """
    for word in entry:
        if word in action_index["nouns"]:
            return word


def confirm_exit():
    confirm = minimize_input("Are you sure? (Y/N)")
    if confirm == "y":
        print(f"Thank you for playing.")
        raise EndGame
    else:
        clear_screen()
        pass


def show_commands(player):
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


def attack_of_opportunity(player, text_input):
    text_input = ' '.join(text_input)
    import ipdb
    ipdb.set_trace()
    if len(player.room.mobs) > 0:
        for idx, mobs in player.room.mobs.items():
            for mob in mobs:
                monster_aoo = f"The {mob.name} was still in the {player.room} while you were attempting to {text_input}. It gets a free attack against you."
                monster_aoo_journal = f"The {mob.name} was still in the {player.room} while you were attempting to {text_input}. It got a free attack against you."
                player.add_messages(monster_aoo)
                player.journal.add_entry(monster_aoo_journal)
                # TODO: Add monster attack.
                if player.current_hp <= 0:
                    entry = f"You were killed by the {mob.name}."
                    player.journal.add_entry(entry)
                    raise EndGameDied(entry)
