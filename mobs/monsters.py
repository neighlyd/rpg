import random

from utils import clear_screen
from items.armor import *
from items.weapons import *
from errors import EndGameDied

LOOT_TABLE = {
    'A': [(RustySword, 100), ],
    'B': [(RoughSpunRobe, 50), (RoughSpunTunic, 25),]
}


class Mob(object):

    def __init__(self, name=None, max_hp=None, room=None):
        self.max_hp = max_hp
        self.current_hp = self.max_hp
        self.base_defense = 0
        self.name = name
        self.room = room
        self.attack = 0
        self.equipped_armor = EquippedArmor()
        self.equipped_weapon = EquippedWeapon()

    def roll_attack(self):
        roll = random.randint(1, 20)
        total = roll + self.attack + self.equipped_weapon.main_hand.attack
        return total

    def roll_damage(self):
        return random.randint(self.equipped_weapon.main_hand.damage_min, self.equipped_weapon.main_hand.damage_max)

    def current_defense(self):
        return self.base_defense + self.equipped_armor.physical_defense()

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
                            looted_items = self.loot
                            loot_message = f"You looted the "
                            first_iter = True
                            for item in looted_items:
                                self.remove_loot(item)
                                player.inventory.add_item(item)
                                if first_iter:
                                    loot_message += f"{item.name}"
                                    first_iter = False
                                else:
                                    loot_message += f", {item.name}"
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
        try:
            # Check to see if mob corpse was in its room's corpse dictionary, if so remove it from the dictionary's
            # list. If the list has no elements left, remove the named entry from the dictionary.
            if self.room.mob_corpses[self.name]:
                self.room.mob_corpses[self.name].remove(self)
                if len(self.room.mob_corpses[self.name]) < 1:
                    del self.room.mob_corpses[self.name]
        except KeyError:
            # Somehow the mob's corpse wasn't added to the room's mob corpse dictionary in the first place.
            pass
        pass

    def assign_to_room_dict(self, room):
        # Update a room's dictionary to reflect the presence of a mob's corpse.
        try:
            # Check if a mob corpse type has an entry in a room's dict. If so, add it to the list of mobs there. If not,
            # create a new list with this mob corpse as the first entry.
            if self.room.mob_corpses[self.name]:
                self.room.mob_corpses[self.name].append(self)
        except KeyError:
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
                 unarmed=None, loot_table=None, **kwargs):
        super().__init__(**kwargs)
        self.__class__._all.add(self)
        self.base_defense = base_defense
        self.xp = xp
        self.description = description
        self.unarmed = unarmed
        self.loot_table = loot_table
        self.check_for_armor(armor_options)
        self.check_for_weapon(weapon_options)
        self.assign_to_room_dict()

    def kill_monster(self):
        self._remove_from_old_room_dict()
        self.spawn_corpse()
        self.__class__._all.remove(self)

    def attack_player(self, player, sneak=None):
        combat_report = f""
        attack_text = f"{self.equipped_weapon.main_hand.success_verb} you with their {self.equipped_weapon.main_hand.name}"
        attack_roll = self.roll_attack()
        if attack_roll >= player.current_defense():
            damage = self.roll_damage()
            player.current_hp -= damage
            if player.current_hp <= 0:
                combat_report += (
                    f"The {self} hit you for {damage} points of damage, killing you!\n"
                    f"(Attack Roll: {attack_roll})"
                )
                raise EndGameDied(combat_report)
            else:
                combat_report += (
                    f"The {self} {attack_text} for {damage} points of damage.\n"
                    f"(Attack Roll: {attack_roll})"
                )
        else:
            combat_report += (
                f"The {self} "
                f"{self.equipped_weapon.main_hand.fail_verb} you but missed.\n"
                f"(Attack Roll: {attack_roll})"
            )
        player.add_messages(combat_report)
        player.journal.add_entry(combat_report)

    def _remove_from_old_room_dict(self):
        try:
            # Check to see if mob was in its room's mob dictionary, if so remove it from the dictionary's list.
            # If the list has no elements left, remove the named entry from the dictionary.
            if self.room.mobs[self.name]:
                self.room.mobs[self.name].remove(self)
                if len(self.room.mobs[self.name]) < 1:
                    del self.room.mobs[self.name]
        except KeyError:
            # Somehow the mob wasn't added to the room's mob dictionary in the first place.
            pass

    def assign_to_room_dict(self, new_room=None):
        # Update a room's dictionary to reflect the presence of a mob.
        if new_room is not None:
            # If mob is moving into a new room, remove them from their old room's dictionary, move them to their new
            # room
            self._remove_from_old_room_dict()
            self.room = new_room
        try:
            # Check if a mob type has an entry in a room's dict. If so, add it to the list of mobs there. If not, create
            # a new list with this mob as the first entry.
            if self.room.mobs[self.name]:
                self.room.mobs[self.name].append(self)
        except KeyError:
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
        if self.loot_table is not None:
            for item in LOOT_TABLE[self.loot_table]:
                if item[1] == 100:
                    loot.append(item[0]())
                else:
                    percent = random.randint(1, 100)
                    if percent <= item[1]:
                        loot.append(item[0]())
        return loot

    def spawn_corpse(self):
        corpse_name = f"{self.name} Corpse"
        loot = self.check_for_loot()
        return Corpse(corpse_name, self.room, loot=loot)


class Bat(Monster):

    def __init__(self, room):
        super().__init__(
            name="Bat",
            description="Basically, a flying rat.",
            room=room,
            max_hp=4,
            base_defense=7,
            xp=5,
            unarmed="bit",
            weapon_options=[(Bite, 100), ],
            loot_table='A'
        )


class Goblin(Monster):

    def __init__(self, room):
        super().__init__(
            name="Goblin",
            description="A pathetic, snivelling creature.",
            room=room,
            max_hp=7,
            base_defense=7,
            xp=10,
            armor_options=[(RoughSpunTunic, 25), (RoughSpunRobe, 75)],
            weapon_options=[(RustyDagger, 100), ],
            unarmed="punched",
            loot_table='A',
        )


class Orc(Monster):

    def __init__(self, room):
        super().__init__(
            name="Orc",
            description="It's big, it's tough, it's green, and it's pissed off.",
            room=room,
            max_hp=15,
            base_defense=12,
            xp=15,
            armor_options=[(RoughSpunTunic, 75), (RoughSpunRobe, 100)],
            weapon_options=[(RustySword, 75), (RustyDagger, 100)],
            unarmed="punched",
            loot_table='B',
        )