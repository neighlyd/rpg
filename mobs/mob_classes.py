import random
from items.armor import *
from items.weapons import *


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
        print(f"{roll} + {self.attack} + {self.equipped_weapon.main_hand.attack}")
        return total

    def roll_damage(self):
        return random.randint(self.equipped_weapon.main_hand.damage_min, self.equipped_weapon.main_hand.damage_max)

    def current_defense(self):
        return self.base_defense + self.equipped_armor.physical_defense()

    def inspect(self):
        inspected = (
            f"Name: {self.name}\n"
            f"Current HP: {self.current_hp}\n"
            f"Defense: {self.base_defense}\n"
        )
        return inspected

    def __str__(self):
        return f"{self.name}"


class Monster(Mob):

    def __init__(self, base_defense=None, xp=None, description=None, armor_options=None, weapon_options=None, **kwargs):
        super().__init__(**kwargs)
        self.base_defense = base_defense
        self.xp = xp
        self.description = description
        self.check_for_armor(armor_options)
        self.check_for_weapon(weapon_options)
        self.assign_to_room_dict()

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
        )