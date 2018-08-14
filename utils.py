import os


class EndGame(Exception):
    pass


class EndGameDied(EndGame):
    print(f"You died")
    pass


class ZoneAlreadyExists(EndGame):
    pass


class ZoneCreationError(EndGame):
    print(f"Zone Creation Error")
    pass


class RoomDoesNotExist(EndGame):
    pass


def clear_screen():
    # Command to clear screen
    os.system("cls" if os.name == "nt" else "clear")


def clean_input(entry):
    user_input = input(entry)
    if user_input:
        return user_input.lower().lstrip()[0]
    else:
        print(f"You must enter something.")
        clean_input(entry)
