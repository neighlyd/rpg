import operator
import math
import random
from collections import namedtuple

from .monsters import Mob, Corpse, Monster
from combat import attack_action, attack_of_opportunity
from examine import examine_object, search
from items import Inventory, equip_action, armor, weapons
from utilities.movement import move_action
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
        f"{player.view_stats_no_header()}\n"
        f"############################\n"
    )
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
            "what is": "look",
            "what's": "look",
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

    def __init__(self, name, room):
        self.action_index = ACTION_INDEX
        self.base_defense = 10
        self.attack = 0.01
        self.xp = 0
        self.level = 1
        self.xp_to_level = self.set_xp_to_level()
        self.constitution = 10
        self.dexterity = 10
        self.intelligence = 10
        self.strength = 10
        self.find_traps = 50
        self.turn_counter = 1
        self.max_hp = self.set_max_hp()
        # TODO: Figure out how to calculate Stamina and Mana;
        # TODO: Implement stamina and mana drain from certain abilities.
        # TODO: Implement stamina and mana regen during advance_turn().
        self.stamina = 0
        self.mana = 0
        self.inventory = Inventory()
        self.journal = Journal()
        self.explored_rooms = dict()
        self.cooldowns = dict()
        self.messages = None
        super().__init__(name, room, max_hp=self.max_hp)
        self.assign_room(room)

    def ability_mod(self, abil):
        ability = getattr(self, abil)
        return int((ability/2)-5)

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

    def attack_target_mob(self, text_input, dam_mod=None, success_verb=None, fail_verb=None, outcome=f""):
        """
            Check a player's attack on a mob and modify the journal appropriately.
        :param text_input: A string representing the intended target.
        :param dam_mod: A modifier when using a special attack.
        :param success_verb: A verb overriding the player's equipped weapon verb; used in special attacks.
        :param fail_verb: A verb overriding the player's equipped weapon verb; used in special attacks.
        :param outcome: An appendix to add to attacks if they have a special outcome (e.g. a target is stunned or on
                        fire)
        :return: A namedtuple with 2 positions - (Bool: was hit successful, target object)
        """
        # TODO: Time to kill bats and goblins is good (2-3 rounds, max end is 5-6 with bad luck).
        # TODO: They hit too frequently/do too much damage without being able to heal or mitigate damage.
        # TODO: Add in heal ability/potions (how to make it useful, but not too easy? - extended CD?)
        # TODO: Increase monster EXP to reduce levelling rate (too slow ATM).
        # TODO: Damage mitigation via armor (both reduce to-hit and reduce damage amount?)
        entry = f""
        target, search_term = search(self, text_input, "room.mobs")
        Report = namedtuple("Report", ("success", "target"))
        if target:
            # Just going to have the player attack the first mob of that type in the room for now. I'll figure out how
            # I want to do selection later.
            mob = target[0]
            attack = attack_action(self, mob, dam_mod)
            if attack.hit:
                if success_verb:
                    attack_verb = f"{success_verb} the {mob}"
                else:
                    attack_verb = (
                        f"{self.equipped_weapon.main_hand.success_verb} the {mob} with your "
                        f"{self.equipped_weapon.main_hand.name}"
                    )
                if attack.hit_type == "hit":
                    entry += f"You {attack_verb}"
                elif attack.hit_type == "crit":
                    entry += f"You savagely {attack_verb}"
                entry += f" for {attack.damage} damage"
                if mob.current_hp <= 0:
                    self.xp += mob.xp
                    entry += (
                        f", killing it!\n"
                        f"You gain {mob.xp} xp."
                    )
                    mob.kill_monster()
                else:
                    entry += f"{outcome}.\n"
            else:
                if fail_verb:
                    attack_verb = f"{fail_verb} the {mob}"
                else:
                    attack_verb = (
                        f"{self.equipped_weapon.main_hand.fail_verb} the {mob} with your "
                        f"{self.equipped_weapon.main_hand.name}"
                    )
                entry += f"You {attack_verb} but"
                if attack.hit_type == "miss":
                    entry += (
                        f" missed."
                    )
                if attack.hit_type == "dodge":
                    entry += (
                        f" the {mob} dodged out of the way."
                    )
            self.add_messages(entry)
            self.journal.add_entry(f"(Round {self.turn_counter}): " + entry)
            return Report(attack.hit, mob)
        else:
            self.add_messages(f"You do not see one of those.")
            return Report(False, None)

    def basic_attack(self, text_input):
        attack = self.attack_target_mob(text_input)
        if attack.target:
            if attack.target.current_hp >= 1:
                self.advance_turn(attack.target)
            else:
                self.advance_turn()
        else:
            self.advance_turn()

    def check_level_up(self):
        if self.xp >= self.xp_to_level:
            # Just gonna have hp double at the moment.
            self.level += 1
            self.max_hp = self.set_max_hp()
            self.current_hp = self.max_hp
            self.xp_to_level = self.set_xp_to_level()
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
        attack_of_opportunity(self, text_input)
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

    def set_max_hp(self):
        return (self.level*20) + self.ability_mod("constitution")

    def set_xp_to_level(self):
        return int(80*((1+.25)**self.level))

    def show_world_map(self):
        self.room.zone.world_map.show_world_map(self)

    def show_zone_map(self):
        self.room.zone.show_zone_map(self)

    def view_stats_no_header(self):
        stats = (
            f"Class: {self.name}\n"
            f"Level: {self.level} ({self.xp}/{self.xp_to_level} xp.)\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"Defense: {self.current_phys_defense()}"
        )
        return stats

    def view_stats_header(self):
        stats = (
            f"Your Character Stats:\n"
            f"Class: {self.name}\n"
            f"Level: {self.level} ({self.xp}/{self.xp_to_level} xp.)\n"
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
        attack_of_opportunity(self, text_input)
        equip_action(self, text_input)
        self.advance_turn()

    def loot_corpse(self):
        pass


class Wizard(Character):
    name = "Wizard"

    def __init__(self, room):
        super().__init__("Wizard", room=room)
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
            attack = self.attack_target_mob(
                text_input,
                dam_mod=damage_modifier,
                success_verb=verb,
                fail_verb=verb
            )
            if attack.target:
                if attack.target.current_hp >= 1:
                    self.advance_turn(attack.target)
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
        super().__init__("Fighter", room=room)
        self.strength = 10
        self.equipped_weapon.main_hand = weapons.Sword()
        self.equipped_armor.chest = armor.Tunic()
        self.action_index["verbs"]["kick"] = "kick"
        self.cooldowns["physical"] = 0

    def kick(self, text_input):
        success_verb = f"kicked"
        fail_verb = f"kicked at"
        outcome = f", stunning it for a round"
        dam_mod = (operator.truediv, 1.75)
        if self.cooldowns["physical"] == 0:
            self.cooldowns["physical"] = 6 - self.haste_amount()
            attack = self.attack_target_mob(
                text_input,
                success_verb=success_verb,
                fail_verb=fail_verb,
                outcome=outcome,
                dam_mod=dam_mod
            )
            if attack.success:
                stun_dur = 2 + self.equipped_weapon.main_hand.stun
                attack.target.stun_monster(stun_dur)
                self.advance_turn()
            else:
                if attack.target:
                    if attack.target.current_hp >= 1:
                        self.advance_turn(attack.target)
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
