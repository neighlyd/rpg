import random
from .items import ItemBase


class RoomItem(ItemBase):

    def __init__(self, room=None, items=None, trap_options=None, **kwargs):
        super().__init__(**kwargs)
        self.room = room
        self.items = items
        self.trapped = False
        self.trap = None
        self.checked = False
        self.checked_message = None
        self.assign_to_room_dict()
        if trap_options:
            self.place_trap(trap_options)

    def assign_to_room_dict(self):
        if self.name in self.room.items:
            self.room.items[self.name].append(self)
        else:
            self.room.items[self.name] = [self]

    def check_for_traps(self, player):
        if not self.checked:
            trap_check = f""
            if self.trapped:
                if random.randint(1, 100) <= player.find_traps:
                    trap_check += f"The {self.name} appears to be trapped"
                else:
                    trap_check += f"The {self.name} does not appear to be trapped."
            player.journal.add_entry(trap_check)
            player.add_messages(trap_check)
            self.checked_message = trap_check
        else:
            player.journal.add_entry(self.checked_message)
            player.add_messages(self.checked_message)

    def detonate_trap(self):
        pass

    def examine(self, player):
        examine_message = (
            f"You examine the {self.name}.\n"
            f"{self.description}"
        )
        player.add_messages(examine_message)
        player.journal.add_entry(examine_message)
        self.check_for_traps(player)

    def place_trap(self, trap_options):
        if random.randint(1, 100) <= trap_options[1]:
            self.trapped = True
            self.trap = trap_options[0]
        else:
            pass

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class TreasureChest(RoomItem):

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            name='Treasure Chest',
            description='It is a large, banded treasure chest.',
            weight=100
        )
