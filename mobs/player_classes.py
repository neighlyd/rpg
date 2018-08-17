from .mob_classes import Mob
from items import Inventory, inspect_item, equip_action, armor, weapons
from journal import Journal
from utils import clear_screen, minimize_input


def choose_class(player, starting_room):
    clear_screen()
    class_choice = minimize_input(f"What class would you like to be?\nType either (F)ighter or (W)izard:")
    if class_choice == "f":
        player = Fighter(starting_room)
    elif class_choice == "w":
        player = Wizard(starting_room)
    else:
        player = None
        return player
    clear_screen()
    choice = (
        f"############################\n"
        f"You have chosen {player.name}.\n"
        f"{player.view_starting_stats()}\n"
        f"############################\n"
    )
    player.inventory.add_item(weapons.RustyDagger())
    print(choice)
    final = minimize_input(f"Would you like to keep this class? (Y/N)")
    if final == "y":
        clear_screen()
        player.journal.initialize_journal(starting_room)
        return player
    else:
        clear_screen()
        player = None


class Character(Mob):

    def __init__(self, name, max_hp, room):
        super().__init__(name, max_hp, room)
        self.base_defense = 10
        self.level = 1
        self.xp = 0
        self.inventory = Inventory()
        self.journal = Journal()
        self.explored_rooms = dict()
        self.messages = None
        self.assign_room(room)

    def assign_room(self, room):
        self.room = room
        if id(room.zone) in self.explored_rooms:
            if room not in self.explored_rooms[id(room.zone)]:
                self.explored_rooms[id(room.zone)].append(room)
        else:
            self.explored_rooms[id(room.zone)] = [room]

    def add_messages(self, message):
        if self.messages is None:
            self.messages = list()
        self.messages.append(message)

    def clear_messages(self):
        self.messages = None

    def print_messages(self):
        messages = f""
        for message in self.messages:
            messages += message + f"\n"
            messages += f"----------------------------\n"
        return print(messages)

    def view_starting_stats(self):
        stats = (
            f"Class: {self.name}\n"
            f"Level: {self.level}\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"Defense: {self.current_defense()}"
        )
        return stats

    def view_stats(self):
        stats = (
            f"Your Character Stats:\n"
            f"Class: {self.name}\n"
            f"Level: {self.level}\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"Defense: {self.current_defense()}"
        )
        self.add_messages(stats)

    def read_journal(self):
        self.add_messages(self.journal.read_journal())

    def show_world_map(self):
        self.room.zone.world_map.show_world_map(self)

    def show_zone_map(self):
        self.room.zone.show_zone_map(self)

    def inspect_room(self):
        self.add_messages(self.room.inspect())

    def view_equipped(self):
        equipped_armor = self.equipped_armor.__str__()
        equipped_weapons = self.equipped_weapon.__str__()
        self.add_messages(equipped_armor)
        self.add_messages(equipped_weapons)

    def view_inventory(self):
        self.add_messages(self.inventory.__str__())

    def inspect_item(self, item):
        return inspect_item(self, item)

    def equip_item(self, item):
        return equip_action(self, item)

class Wizard(Character):
    name = "Wizard"

    def __init__(self, room):
        super().__init__("Wizard", max_hp=25, room=room)
        self.equipped_weapon.main_hand = weapons.WalkingStaff()
        self.equipped_armor.chest = armor.RoughSpunRobe()


class Fighter(Character):

    def __init__(self, room):
        super().__init__("Fighter", max_hp=25, room=room)
        self.equipped_weapon.main_hand = weapons.RustySword()
        self.equipped_armor.chest = armor.RoughSpunTunic()
