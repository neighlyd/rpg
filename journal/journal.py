class Journal:

    def __init__(self):
        self.entries = list()

    def add_entry(self, entry):
        self.entries.append(entry)

    def initialize_journal(self, starting_room):
        entry = f"You began your journey in {starting_room}"
        self.add_entry(entry)

    def travel_entry(self, room, new_room, direction):
        # TODO: Change so player.turn_counter can get added.
        entry = f"You travelled {direction} from {room} to {new_room}."
        self.add_entry(entry)

    def read_journal(self):
        journal_entries = f"Your Journal Entries:\n"
        journal_entries += f"------------------------\n"
        for row in self.entries:
            journal_entries += row + f"\n"
            journal_entries += f"------------------------\n"
        return journal_entries


