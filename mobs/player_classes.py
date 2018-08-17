from .mob_classes import Mob
from items import Inventory, spawn_item, inspect_item, equip_action
from journal import Journal


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
        self.equipped_weapon.main_hand = spawn_item("Walking Staff")
        self.equipped_armor.chest = spawn_item("Rough-Spun Robe")


class Fighter(Character):

    def __init__(self, room):
        super().__init__("Fighter", max_hp=25, room=room)
        self.equipped_weapon.main_hand = spawn_item("Walking Staff")
        self.equipped_armor.chest = spawn_item("Rough-Spun Tunic")
