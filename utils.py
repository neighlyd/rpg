import os


class EndGame(Exception):
    pass


class EndGameDied(EndGame):
    print(f"You died")
    pass


class ZoneAlreadyExists(EndGame):
    print(f"A Zone Already Exists In This Location.")
    pass


def clear_screen():
    # Command to clear screen
    os.system("cls" if os.name == "nt" else "clear")


def clean_input(entry):
    user_input = input(entry)
    if user_input:
        return user_input.lower().lstrip()[0]
    else:
        return print(f"You must enter something.")