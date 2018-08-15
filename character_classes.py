from dice import roll_dice
from items.inventory import Inventory
from items.armor import EquippedArmor


class Mob(object):

    stat_bonuses = {1: -5,
                    2: -4, 3: -4,
                    4: -3, 5: -3,
                    6: -2, 7: -2,
                    8: -1, 9: -1,
                    10: 0, 11: 0,
                    12: +1, 13: +1,
                    14: +2, 15: +2,
                    16: +3, 17: +3,
                    18: +4, 19: +4,
                    20: +5, 21: +5}

    def __init__(self, room):
        self.strength = 8
        self.dexterity = 8
        self.constitution = 8
        self.intelligence = 8
        self.wisdom = 8
        self.charisma = 8
        self.proficiency = 2
        self.hp = 0
        self.ac = 10
        self.name = ""
        self.room = room

    def _base_roll_with_proficiency(self, stat):
        roll = roll_dice(1, 20)
        bonus = self.stat_bonuses[stat]
        total = roll + self.proficiency + bonus
        return total, f'Total: {total} (roll: {roll}, proficiency: {self.proficiency}, stat bonus: {bonus})'

    def _base_roll_without_proficiency(self, stat):
            roll = roll_dice(1, 20)
            bonus = self.stat_bonuses[stat]
            total = roll + bonus
            return total, f'Total: {total} (roll: {roll},  stat bonus: {bonus})'

    def _damage(self, n, d, stat):
        return roll_dice(n, d) + self.stat_bonuses[stat]

    def inspect(self):
        inspected = (
            f"Name: {self.name}\n"
            f"Current HP: {self.hp}\n"
            f"AC: {self.ac}\n"
        )
        return inspected

    def initiative(self):
        return roll_dice(1, 20) + self.stat_bonuses[self.dexterity]

    def __str__(self):
        return f"{self.name}"


class Character(Mob):

    def __init__(self, room):
        super().__init__(room)
        self.level = 1
        self.xp = 0
        self.inventory = Inventory()
        self.equipped_armor = EquippedArmor()
    
    def list_stats(self):
        stats = (
            f"Your stats are:\n"
            f"Class: {self.name}\n"
            f"Strength: {self.strength}\n"
            f"Constitution: {self.constitution}\n"
            f"Dexterity: {self.dexterity}\n"
            f"Intelligence: {self.intelligence}\n"
            f"Wisdom: {self.wisdom}\n"
            f"Charisma: {self.charisma}\n"
        )
        return stats

    def current_hp(self):
        return f'Current HP: {self.hp}'

    def current_level(self):
        return f'Current level: {self.level}'


class Wizard(Character):

    def __init__(self, room):
        super().__init__(room)
        self.strength = 8
        self.dexterity = 14
        self.constitution = 13
        self.intelligence = 15
        self.wisdom = 12
        self.charisma = 10
        self.hp = 6 + self.stat_bonuses[self.constitution]
        self.name = "Wizard"

    def attack(self):
        return self._base_roll_with_proficiency(self.intelligence)

    def damage(self):
        return self._damage(1, 6, self.intelligence)


class Fighter(Character):

    def __init__(self, room):
        super().__init__(room)
        self.strength = 15
        self.dexterity = 13
        self.constitution = 14
        self.intelligence = 8
        self.wisdom = 10
        self.charisma = 12
        self.hp = 10 + self.stat_bonuses[self.constitution]
        self.name = "Fighter"

    def attack(self):
        return self._base_roll_with_proficiency(self.strength)

    def damage(self):
        return self._damage(1, 6, self.strength)


