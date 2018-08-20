from .monsters import Mob, Corpse
from items import Inventory, equip_action, armor, weapons
from examine import examine_object
from journal import Journal
from utils import clear_screen, minimize_input
from examine import search
from mapping.movement import move_action


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
        f"{player.view_stats_no_header()}\n"
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

    action_index = {
        "verbs": {
            "attack": "attack",
            "check": "look",
            "equip": "equip",
            "examine": "look",
            "exit": "quit",
            "fight": "attack",
            "help": "help",
            "investigate": "look",
            "look": "look",
            "move": "move",
            "quit": "quit",
            "read": "read",
            "show": "look",
            "travel": "travel",
            "use": "use",
            "view": "look",
            "list": "look",
            "go": "move",
            "pet": "pet",
            "inspect": "look",
            "debug": "debug",
            "loot": "loot",
        },
        "nouns": [
            "character",
            "east",
            "equipment",
            "inventory",
            "journal",
            "map",
            "north",
            "room",
            "south",
            "stats",
            "west",
            "world",
            "zone",
            "turn",
        ]
    }

    # Stand-in numbers.
    LEVEL_CHART = {
        1: 20,
        2: 50,
        3: 100,
        4: 175,
        5: 300,
        6: 600,
    }

    def __init__(self, name, max_hp, room):
        super().__init__(name, max_hp, room)
        self.base_defense = 10
        self.level = 1
        self.xp = 0
        self.inventory = Inventory()
        self.journal = Journal()
        self.explored_rooms = dict()
        self.messages = None
        self.turn_counter = 1
        self.assign_room(room)

    def add_messages(self, message):
        if self.messages is None:
            self.messages = []
        self.messages.append(message)

    def advance_turn(self, mob=None):
        if mob is not None:
            if mob.current_hp >= 1:
                mob.attack_player(self)
        for corpse in Corpse._all:
            corpse.decay()
        self.check_level_up()
        self.turn_counter += 1

    def assign_room(self, room):
        self.room = room
        if id(room.zone) in self.explored_rooms:
            if room not in self.explored_rooms[id(room.zone)]:
                self.explored_rooms[id(room.zone)].append(room)
        else:
            self.explored_rooms[id(room.zone)] = [room]

    def attack_monster(self, text_input):
        mob, search_term = search(self, text_input, "room.mobs")
        combat_report = f""
        if mob is not None:
            # Just going to have the player attack the first mob of that type in the room for now. I'll figure out how
            # I want to do selection later.
            mob = mob[0]
            attack_roll = self.roll_attack()
            if attack_roll >= mob.current_defense():
                damage = self.roll_damage()
                mob.current_hp -= damage
                if mob.current_hp <= 0:
                    self.xp += mob.xp
                    combat_report += (
                        f"You {self.equipped_weapon.main_hand.success_verb} the {mob} with your "
                        f"{self.equipped_weapon.main_hand.name} for {damage} points of "
                        f"damage, killing it!\n"
                        f"(Attack Roll: {attack_roll})\n"
                        f"You gained {mob.xp} xp."
                    )
                    mob.kill_monster()
                else:
                    combat_report += (
                        f"You {self.equipped_weapon.main_hand.success_verb} the {mob} with your "
                        f"{self.equipped_weapon.main_hand.name} for {damage} points of "
                        f"damage!\n"
                        f"(Attack Roll: {attack_roll})\n"
                    )
            else:
                combat_report += (
                    f"You {self.equipped_weapon.main_hand.fail_verb} the {mob} with your "
                    f"{self.equipped_weapon.main_hand.name} but missed.\n"
                    f"(Attack Roll: {attack_roll})"
                )
            self.add_messages(combat_report)
            self.journal.add_entry(combat_report)
            if mob.current_hp >= 1:
                self.advance_turn(mob)
            else:
                self.advance_turn()

    def attack_of_opportunity(self, text_input, sneak=None):
        text_input = ' '.join(text_input)
        if sneak:
            # TODO: Add sneak percent chance for Rogues.
            pass
        else:
            if len(self.room.mobs) > 0:
                for idx, mobs in self.room.mobs.items():
                    for mob in mobs:
                        monster_aoo = (f"The {mob.name} was still in the {self.room} while you were attempting to "
                                       f"{text_input}. It gets a free attack against you.")
                        monster_aoo_journal = (f"The {mob.name} was still in the {self.room} while you were attempting to"
                                               f" {text_input}. It got a free attack against you.")
                        self.add_messages(monster_aoo)
                        self.journal.add_entry(monster_aoo_journal)
                        mob.attack_player(self)

    def check_level_up(self):
        ding = f""
        if self.xp >= self.LEVEL_CHART[self.level]:
            # Just gonna have hp double at the moment.
            self.max_hp *= 2
            self.current_hp = self.max_hp
            self.level += 1
            ding = f"DING! You've leveled up to {self.level}!\n"
            self.journal.add_entry(ding)
            ding += (
                f"Your stats are now:\n"
                f"{self.view_stats_no_header()}"
            )
            self.add_messages(ding)
        else:
            pass

    def check_turn(self):
        self.add_messages(f"Turn: {self.turn_counter}")

    def clear_messages(self):
        self.messages = None

    def examine_object(self, item):
        return examine_object(self, item)

    def examine_room(self):
        self.add_messages(self.room.examine())

    def move_action(self, noun, text_input):
        # TODO: Add sneak action for Rogues.
        self.attack_of_opportunity(text_input)
        move_action(self, noun)
        self.advance_turn()

    def print_messages(self):
        messages = f""
        for message in self.messages:
            messages += message + f"\n"
            messages += f"----------------------------\n"
        return print(messages)

    def read_journal(self):
        self.add_messages(self.journal.read_journal())

    def show_world_map(self):
        self.room.zone.world_map.show_world_map(self)

    def show_zone_map(self):
        self.room.zone.show_zone_map(self)

    def view_stats_no_header(self):
        stats = (
            f"Class: {self.name}\n"
            f"Level: {self.level} ({self.xp}/{self.LEVEL_CHART[self.level]} xp.)\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"Defense: {self.current_defense()}"
        )
        return stats

    def view_stats_header(self):
        stats = (
            f"Your Character Stats:\n"
            f"Class: {self.name}\n"
            f"Level: {self.level} ({self.xp}/{self.LEVEL_CHART[self.level]} xp.)\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"Defense: {self.current_defense()}"
        )
        self.add_messages(stats)

    def view_equipped(self):
        equipped_armor = self.equipped_armor.__str__()
        equipped_weapons = self.equipped_weapon.__str__()
        self.add_messages(equipped_armor)
        self.add_messages(equipped_weapons)

    def view_inventory(self):
        self.add_messages(self.inventory.__str__())

    def equip_item(self, text_input):
        self.attack_of_opportunity(text_input)
        equip_action(self, text_input)
        self.advance_turn()

    def loot_corpse(self):
        pass

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
        self.inventory.add_item(weapons.BatSlayer())
        self.inventory.add_item(weapons.BatSlayer())
