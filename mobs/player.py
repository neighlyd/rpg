import operator
import math
import random

from .monsters import Mob, Corpse, Monster
from items import Inventory, equip_action, armor, weapons
from examine import examine_object, search
from journal import Journal
from utils import clear_screen, minimize_input
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


ACTION_INDEX = {
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
            "open": "loot",
        },
        "nouns": [
            "character",
            "cooldowns",
            "cooldown",
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


class Character(Mob):

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
        self.dexterity = 8
        self.intelligence = 8
        self.strength = 8
        self.inventory = Inventory()
        self.journal = Journal()
        self.explored_rooms = dict()
        self.messages = None
        self.find_traps = 50
        self.turn_counter = 1
        self.action_index = ACTION_INDEX
        self.cooldowns = dict()
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
        for monster in Monster._all:
            monster.reduce_stun()
        self.check_level_up()
        self.reduce_cooldowns()
        self.turn_counter += 1

    def assign_room(self, room):
        self.room = room
        if id(room.zone) in self.explored_rooms:
            if room not in self.explored_rooms[id(room.zone)]:
                self.explored_rooms[id(room.zone)].append(room)
        else:
            self.explored_rooms[id(room.zone)] = [room]

    def attack_action(self, text_input, attack_modifier=None, damage_modifier=None, success_verb=None, fail_verb=None, outcome=f""):
        entry = f""
        target, search_term = search(self, text_input, "room.mobs")
        if target:
            mob = target[0]
            # Just going to have the player attack the first mob of that type in the room for now. I'll figure out how
            # I want to do selection later.
            attack_roll = self.roll_attack()
            if attack_modifier:
                attack_roll += attack_modifier
            if attack_roll >= mob.current_phys_defense():
                damage = self.roll_damage()
                # damage_modifier is a tuple containing an operator function and what should be in the b position of
                # said operator. See https://docs.python.org/3.6/library/operator.html for more information on operator
                # functions.
                if damage_modifier:
                    damage = math.ceil(damage_modifier[0](damage, damage_modifier[1]))
                mob.current_hp -= damage
                if success_verb:
                    attack_verb = f"You {success_verb} the {mob}"
                else:
                    attack_verb = (
                        f"You {self.equipped_weapon.main_hand.success_verb} the {mob} with your "
                        f"{self.equipped_weapon.main_hand.name}"
                    )
                if mob.current_hp <= 0:
                    self.xp += mob.xp
                    entry += (
                        f"{attack_verb} for {damage} damage, killing it!\n"
                        f"You gained {mob.xp} xp."
                    )
                    mob.kill_monster()
                else:
                    entry += (
                        f"{attack_verb} for {damage} damage{outcome}."
                    )
                report = True
            else:
                if fail_verb:
                    attack_verb = f"You {fail_verb} the {mob}"
                else:
                    attack_verb = (
                        f"You {self.equipped_weapon.main_hand.fail_verb} the {mob} with your "
                        f"{self.equipped_weapon.main_hand.name}"
                    )
                entry += (
                    f"{attack_verb} but missed."
                )
                report = False
            self.add_messages(entry)
            self.journal.add_entry(f"(Round {self.turn_counter}): " + entry)
            return report, mob
        else:
            self.add_messages(f"You do not see one of those.")
            return False, None

    def basic_attack(self, text_input):
        success, mob = self.attack_action(text_input)
        if mob:
            if mob.current_hp >= 1:
                self.advance_turn(mob)
            else:
                self.advance_turn()
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
                        if mob.stunned == 0:
                            monster_aoo = (f"The {mob.name} was still in the {self.room} while you were attempting to "
                                           f"{text_input}. It gets a free attack against you.")
                            monster_aoo_journal = (f"The {mob.name} was still in the {self.room} while you were attempting"
                                                   f" to {text_input}. It got a free attack against you.")
                            self.add_messages(monster_aoo)
                            self.journal.add_entry(f"(Round {self.turn_counter}): " + monster_aoo_journal)
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

    def check_cooldowns(self):
        cds = f""
        first = True
        for abil, cd in self.cooldowns.items():
            if first:
                cds += f"{abil.title()}: {cd} rounds\n"
                first = False
            else:
                cds += (
                    f"{abil.title()}: {cd} rounds\n"
                    f"----------------------"
                )
        self.add_messages(cds)

    def check_turn(self):
        self.add_messages(f"Turn: {self.turn_counter}")

    def clear_messages(self):
        self.messages = None

    def examine_object(self, item):
        return examine_object(self, item)

    def examine_room(self):
        self.add_messages(self.room.examine())

    def haste_amount(self):
        return self.equipped_weapon.main_hand.cd_redux

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

    def reduce_cooldowns(self):
        for abil, cd in self.cooldowns.items():
            if cd > 0:
                self.cooldowns[abil] = cd - 1

    def roll_damage(self):
        base_damage = random.randint(self.equipped_weapon.main_hand.damage_min, self.equipped_weapon.main_hand.damage_max)
        bonus_stat = self.equipped_weapon.main_hand.main_stat
        bonus_amount = getattr(self, bonus_stat)
        total_damage = int(base_damage * (1 + (1/1-math.exp(-bonus_amount/255))))
        return total_damage

    def show_world_map(self):
        self.room.zone.world_map.show_world_map(self)

    def show_zone_map(self):
        self.room.zone.show_zone_map(self)

    def view_stats_no_header(self):
        stats = (
            f"Class: {self.name}\n"
            f"Level: {self.level} ({self.xp}/{self.LEVEL_CHART[self.level]} xp.)\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"Defense: {self.current_phys_defense()}"
        )
        return stats

    def view_stats_header(self):
        stats = (
            f"Your Character Stats:\n"
            f"Class: {self.name}\n"
            f"Level: {self.level} ({self.xp}/{self.LEVEL_CHART[self.level]} xp.)\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"Defense: {self.current_phys_defense()}"
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
        self.intelligence = 10
        self.equipped_weapon.main_hand = weapons.Dagger(adjectives=['rusty'])
        self.equipped_armor.chest = armor.Robe()
        self.action_index["verbs"]["cast"] = "cast"
        self.action_index["nouns"].append("fireblast")
        self.cooldowns["spell"] = 0

    def cast_fireblast(self, text_input):
        verb = f"threw a blast of fire at"
        # TODO: introduce DoT
        outcome = f" lighting it on fire."
        # TODO: Figure out what the real damage of spells should be. Ideally, make lots of unique spells
        damage_modifier = (operator.mul, 1.75)
        if self.cooldowns["spell"] == 0:
            self.cooldowns["spell"] = 6 - self.haste_amount()
            success, mob = self.attack_action(
                text_input,
                damage_modifier=damage_modifier,
                success_verb=verb,
                fail_verb=verb
            )
            if mob:
                if mob.current_hp >= 1:
                    self.advance_turn(mob)
                else:
                    self.advance_turn()
            else:
                self.advance_turn()
        else:
            combat_report = (
                f"You are still weary from casting your last fireball.\n"
                f"Please wait to try again."
            )
            self.add_messages(combat_report)


class Fighter(Character):

    def __init__(self, room):
        super().__init__("Fighter", max_hp=25, room=room)
        self.strength = 10
        self.equipped_weapon.main_hand = weapons.RustySword()
        self.equipped_armor.chest = armor.Tunic()
        self.action_index["verbs"]["kick"] = "kick"
        self.cooldowns["kick"] = 0

    def kick(self, text_input):
        success_verb = f"kicked"
        fail_verb = f"kicked at"
        outcome = f" stunning it for a round"
        damage_modifier = (operator.truediv, 1.75)
        kicked = False
        if self.cooldowns["kick"] == 0:
            self.cooldowns["kick"] = 6 - self.haste_amount()
            kicked, mob = self.attack_action(
                text_input,
                success_verb=success_verb,
                fail_verb=fail_verb,
                outcome=outcome,
                damage_modifier=damage_modifier
            )
            if kicked:
                stun_dur = 2 + self.equipped_weapon.main_hand.stun
                mob.stun_monster(stun_dur)
                self.advance_turn()
            else:
                if mob:
                    if mob.current_hp >= 1:
                        self.advance_turn(mob)
                    else:
                        self.advance_turn()
                else:
                    self.advance_turn()
        else:
            combat_report = (
                f"You are still tired from your last kick.\n"
                f"Please wait to try again."
            )
            self.add_messages(combat_report)
