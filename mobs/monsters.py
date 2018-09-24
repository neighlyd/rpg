import copy
import math
import random
from collections import namedtuple

from algorithms.vose_sort import VoseSort
from combat import attack_action
from errors import EndGameDied
from items.armor import *
from items.weapons import *
from items.items import *
from utils import clear_screen

# TODO: Convert these functions into a single func and then turn LOOT_TABLE func calls into a dict that the single func
# can pull info from.


class Mob(object):

    miss = 0.05
    dodge = 0.17
    crit = 0.05

    def __init__(self, name=None, room=None, max_hp=None):
        self.max_hp = max_hp
        self.current_hp = self.max_hp
        self.base_defense = 0
        self.name = name
        self.room = room
        self.attack = 0
        self.equipped_armor = EquippedArmor()
        self.equipped_weapon = EquippedWeapon()

    def roll_attack(self):
        # Going to try percentage attacks for a bit and see how that goes.
        # Attack stat now adds a certain percentage to the attack roll, increasing likelihood of a hit.
        roll = random.uniform(0, 1)
        total = roll * (1 + self.attack) * (1 + self.equipped_weapon.main_hand.attack)
        return total

    def roll_damage(self):
        return random.randint(self.equipped_weapon.main_hand.damage_min, self.equipped_weapon.main_hand.damage_max)

    def current_phys_defense(self):
        return self.base_defense + self.equipped_armor.physical_defense()

    # def attack_action(self, target, damage_modifier=None):
    #     """
    #        Method for performing the logic to check attack rolls against hit tables.
    #     :param target: An object representing the target of the attack.
    #     :param damage_modifier: A tuple containing an operator function and what should be in the b position of said
    #                             operator. See https://docs.python.org/3.6/library/operator.html for more information.
    #     :return: A namedtuple with 3 positions: (Hit Success/Failure, Hit Type, Damage Amount)
    #     """
    #     atk_roll = self.roll_attack()
    #     atk_roll = target.reduce_attack_roll(atk_roll)
    #     damage = 0
    #     hit = False
    #     if atk_roll > target.miss:
    #         if atk_roll > target.miss + target.dodge:
    #             damage = self.roll_damage()
    #             if damage_modifier:
    #                 damage = math.ceil(damage_modifier[0](damage, damage_modifier[1]))
    #             if atk_roll > target.miss + target.dodge + target.crit:
    #                 hit_type = "hit"
    #                 hit = True
    #             else:
    #                 # Hit is a critical attack. Multiple damage by 2.
    #                 damage = self.roll_damage() * 2
    #                 hit_type = "crit"
    #                 hit = True
    #             target.current_hp -= damage
    #         else:
    #             # Hit will be a dodge.
    #             hit_type = "dodge"
    #     else:
    #         # Hit will be a miss.
    #         hit_type = "miss"
    #     Report = namedtuple("Report", ("hit", "hit_type", "damage"))
    #     report = Report(hit, hit_type, damage)
    #     return report

    def reduce_attack_roll(self, atk_roll):
        reduced_atk = atk_roll * (1 - self.base_defense)
        if self.equipped_armor.chest.name is not None:
            reduced_atk *= (1 - self.equipped_armor.physical_defense())
        return reduced_atk

    def examine(self):
        examine = (
            f"Name: {self.name}\n"
            f"Current HP: {self.current_hp}\n"
            f"Defense: {self.base_defense}\n"
        )
        return examine

    def __str__(self):
        return f"{self.name}"


class Corpse:
    _all = set()

    def __init__(self, name, room, loot=None, decay_counter=0):
        self.__class__._all.add(self)
        self.name = name
        self.loot = loot
        self.room = room
        self.decay_counter = decay_counter
        self.assign_to_room_dict(room)

    def examine_loot(self):
        if self.loot:
            loot_amount = len(self.loot)
            loot = (
                f"You find the following on the {self.name.lower()}:\n"
                f"0) Take Nothing\n"
            )
            if loot_amount > 1:
                loot += f"1) Take Everything\n"
                for idx, item in enumerate(self.loot):
                    loot += f"{idx + 2}) {item.name}\n"
            else:
                for idx, item in enumerate(self.loot):
                    loot += f"{idx + 1}) {item.name}\n"
            return loot, loot_amount
        else:
            return None, None

    def loot_corpse(self, player):
        while True:
            clear_screen()
            loot_list, loot_amount = self.examine_loot()
            if loot_list:
                loot_list += f"What would you like to take?"
                try:
                    loot_choice = int(input(loot_list))
                except ValueError:
                    continue
                else:
                    if loot_choice == 0:
                        player.add_messages(f"You didn't loot anything from the {self.name.lower()}.")
                        break
                    if loot_amount > 1:
                        if loot_choice == 1:
                            looted_items = copy.copy(self.loot)
                            loot_message = f"You looted the "
                            last = len(looted_items)
                            i = 1
                            for item in looted_items:
                                player.inventory.add_item(item)
                                self.remove_loot(item)
                                if last == 2 and i < last:
                                    loot_message += f"{item.name} "
                                    i += 1
                                elif last > 2 and i < last:
                                    loot_message += f"{item.name}, "
                                    i += 1
                                else:
                                    loot_message += f"and {item.name} "
                            loot_message += f"from the {self.name.lower()}"
                            loot_message_journal = loot_message + f" in {player.room}."
                            player.add_messages(loot_message + f".")
                            player.journal.add_entry(loot_message_journal)
                            break
                        else:
                            loot_choice -= 2
                            try:
                                looted_item = self.loot[loot_choice]
                                self.remove_loot(looted_item)
                                player.inventory.add_item(looted_item)
                                loot_message = f"You looted the {looted_item.name} from the {self.name.lower()}"
                                loot_message_journal = loot_message + f" in the {player.room}."
                                player.add_messages(loot_message + f".")
                                player.journal.add_entry(loot_message_journal)
                                break
                            except IndexError:
                                player.add_messages(f"That is an invalid loot choice")
                    else:
                        loot_choice -= 1
                        try:
                            looted_item = self.loot[loot_choice]
                            self.remove_loot(looted_item)
                            player.inventory.add_item(looted_item)
                            loot_message = f"You looted {looted_item.name} from the {self.name.lower()}"
                            loot_message_journal = loot_message + f" in the {player.room}."
                            player.add_messages(loot_message + f".")
                            player.journal.add_entry(loot_message_journal)
                            break
                        except IndexError:
                            player.add_messages(f"That is an invalid loot choice")
                            break
            else:
                player.add_messages(f"The {self.name.lower()} has no loot.")
                break

    def remove_loot(self, item):
        if item in self.loot:
            self.loot.remove(item)

    def remove_corpse(self):
        self.__class__._all.remove(self)
        # Check to see if mob corpse was in its room's corpse dictionary, if so remove it from the dictionary's
        # list. If the list has no elements left, remove the named entry from the dictionary.
        if self.name in self.room.mob_corpses:
            self.room.mob_corpses[self.name].remove(self)
            if len(self.room.mob_corpses[self.name]) < 1:
                del self.room.mob_corpses[self.name]

    def assign_to_room_dict(self, room):
        # Update a room's dictionary to reflect the presence of a mob's corpse.
        # Check if a mob corpse type has an entry in a room's dict. If so, add it to the list of mobs there. If not,
        # create a new list with this mob corpse as the first entry.
        if self.name in self.room.mob_corpses:
            self.room.mob_corpses[self.name].append(self)
        else:
            self.room.mob_corpses[self.name] = [self]

    def decay(self):
        self.decay_counter += 1
        if self.decay_counter >= 50:
            self.remove_corpse()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Monster(Mob):
    _all = set()

    def __init__(self, base_defense=None, xp=None, description=None, armor_options=None, weapon_options=None,
                 unarmed=None, special=None, loot_table=None, **kwargs):
        super().__init__(**kwargs)
        self.__class__._all.add(self)
        self.base_defense = base_defense
        self.xp = xp
        self.description = description
        self.unarmed = unarmed
        self.loot_table = loot_table
        self.stunned = 0
        self.check_for_armor(armor_options)
        self.check_for_weapon(weapon_options)
        self.assign_to_room_dict()

    def stun_monster(self, rounds):
        self.stunned = rounds

    def reduce_stun(self):
        if self.stunned >= 1:
            self.stunned -= 1

    def kill_monster(self):
        self._remove_from_old_room_dict()
        self.spawn_corpse()
        self.__class__._all.remove(self)

    def attack_player(self, player, sneak=None):
        # TODO: Implement sneak to give player chance to escape and avoid hit.
        combat_report = f""
        # Check to see if monster is stunned. If not, attack player.
        if self.stunned == 0:
            attack = attack_action(self, player)
            if attack.hit:
                attack_text = (
                    f"{self.equipped_weapon.main_hand.success_verb} you "
                    f"with their {self.equipped_weapon.main_hand.name}"
                               )
            else:
                attack_text = (
                    f"{self.equipped_weapon.main_hand.fail_verb} you "
                    f"with their {self.equipped_weapon.main_hand.name}"
                )
            if attack.hit_type == "hit":
                combat_report += (
                    f"The {self} {attack_text} for {attack.damage} points of damage"
                )
            elif attack.hit_type == "crit":
                combat_report += (
                    f"The {self} savagely {attack_text} for {attack.damage} "
                    f"points of damage"
                )
            elif attack.hit_type == "miss":
                combat_report += (
                    f"The {self} {attack_text} but missed"
                )
            elif attack.hit_type == "dodge":
                combat_report += (
                    f"The {self} {attack_text} but you dodged out of the way"
                )
            if player.current_hp <= 0:
                combat_report += (
                    f", killing you!\n"
                )
                raise EndGameDied(combat_report)
            else:
                combat_report += (
                    f".\n"
                )
            player.add_messages(combat_report)
            player.journal.add_entry(combat_report)

    def _remove_from_old_room_dict(self):
        # Check to see if mob was in its room's mob dictionary, if so remove it from the dictionary's list.
        # If the list has no elements left, remove the named entry from the dictionary.
        if self.name in self.room.mobs:
            self.room.mobs[self.name].remove(self)
            if len(self.room.mobs[self.name]) < 1:
                del self.room.mobs[self.name]

    def assign_to_room_dict(self, new_room=None):
        # Update a room's dictionary to reflect the presence of a mob.
        if new_room is not None:
            # If mob is moving into a new room, remove them from their old room's dictionary, move them to their new
            # room
            self._remove_from_old_room_dict()
            self.room = new_room
        # Check if a mob type has an entry in a room's dict. If so, add it to the list of mobs there. If not, create
        # a new list with this mob as the first entry.
        if self.name in self.room.mobs:
            self.room.mobs[self.name].append(self)
        else:
            self.room.mobs[self.name] = [self]

    def check_for_armor(self, armor_options):
        if armor_options is not None:
            if len(armor_options) > 1:
                for item in armor_options:
                    percent = random.randint(1, 100)
                    if percent <= item[1]:
                        self.equipped_armor.chest = item[0]()
                        break
            else:
                if armor_options[0][1] == 100:
                    # TODO: add logic for multiple armor slots.
                    self.equipped_armor.chest = armor_options[0][0]()
                else:
                    percent = random.randint(1, 100)
                    if percent <= armor_options[0][1]:
                        self.equipped_armor.chest = armor_options[0][0]()

    def check_for_weapon(self, weapon_options):
        if weapon_options is not None:
            if len(weapon_options) > 1:
                for item in weapon_options:
                    percent = random.randint(1, 100)
                    if percent <= item[1]:
                        self.equipped_weapon.main_hand = item[0]()
                        break
            else:
                if weapon_options[0][1] == 100:
                    self.equipped_weapon.main_hand = weapon_options[0][0]()
                else:
                    percent = random.randint(1, 100)
                    if percent <= weapon_options[0][1]:
                        self.equipped_weapon.main_hand = weapon_options[0][0]()

    def check_for_loot(self):
        loot = []
        try:
            if self.LOOT_TABLE:
                loot_quantity = self.LOOT_TABLE.alias_generation()
                if loot_quantity:
                    for quantity in loot_quantity:
                        if "item" in quantity:
                            for i in range(quantity[1]):
                                loot.append(self.LOOT_ITEMS.alias_generation()())
                        if "weapon" in quantity:
                            for i in range(quantity[1]):
                                weapon = self.LOOT_WEAPONS.alias_generation()
                                adjective = random.choice(list(Weapon.WEAPON_ADJECTIVES))
                                weapon = weapon(adjectives=[adjective])
                                loot.append(weapon)
                        if "armor" in quantity:
                            for i in range(quantity[1]):
                                armor = self.LOOT_ARMOR.alias_generation()
                                adjective = random.choice(list(Armor.ARMOR_ADJECTIVES))
                                armor = armor(adjectives=[adjective])
                                loot.append(armor)
        except AttributeError:
            pass
        return loot

    def spawn_corpse(self):
        corpse_name = f"{self.name} Corpse"
        loot = self.check_for_loot()
        return Corpse(corpse_name, self.room, loot=loot)


class Bat(Monster):

    LOOT_ITEMS = VoseSort({BatFang: .10, BatWing: .80})
    LOOT_TABLE = VoseSort({None: .5, (("item", 1),): .35, (("item", 2),): .15})

    def __init__(self, room):
        super().__init__(
            name="Bat",
            description="Basically, a flying rat.",
            room=room,
            max_hp=4,
            base_defense=0.01,
            xp=10,
            unarmed="bit",
            weapon_options=[(Bite, 100), ],
        )


class Goblin(Monster):
    LOOT_WEAPONS = VoseSort({Dagger: .50, Staff: .25, Sword: .25})
    LOOT_ARMOR = VoseSort({Tunic: .25, Robe: .75})
    LOOT_TABLE = VoseSort({None: .15, (("weapon", 1),): .5, (("armor", 1),): .15, (("weapon", 1), ("armor", 1)): .2})

    def __init__(self, room):
        super().__init__(
            name="Goblin",
            description="A pathetic, snivelling creature.",
            room=room,
            max_hp=7,
            base_defense=0.04,
            xp=15,
            armor_options=[(Tunic, 25), (Robe, 75)],
            weapon_options=[(Dagger, 100), ],
            unarmed="punched",
        )


class Orc(Monster):
    LOOT_WEAPONS = VoseSort({Sword: .40, Staff: .45, Dagger: .15})
    LOOT_ARMOR = VoseSort({Tunic: .50, Robe: .50})
    LOOT_TABLE = VoseSort({None: .15,
                           (("weapon", 1), ): .15,
                           (("armor", 1), ): 15,
                           (("weapon", 1), ("armor", 1)): 15,
                           (("weapon", 1), ("armor", 1), ("item", 1)): 15,
                           (("weapon", 1), ("armor", 1), ("item", 2)): 5
                           })

    def __init__(self, room):
        super().__init__(
            name="Orc",
            description="It's big, it's tough, it's green, and it's pissed off.",
            room=room,
            max_hp=15,
            base_defense=0.09,
            xp=25,
            armor_options=[(Tunic, 75), (Robe, 100)],
            weapon_options=[(Sword, 75), (Dagger, 100)],
            unarmed="punched",
        )
