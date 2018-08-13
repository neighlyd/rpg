from character_classes import Mob


class Monster(Mob):

    def __init__(self, room):
        super().__init__(room)
        self.cr = 0
        self.xp = 0


class Goblin(Monster):

    def __init__(self, room):
        super().__init__(room)
        self.strength = 8
        self.dexterity = 14
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 8
        self.charisma = 8
        self.proficiency = 2
        self.hp = 7
        self.ac = 15
        self.cr = .25
        self.xp = 50
        self.name = "Goblin"

    def attack(self):
        return self._base_roll_with_proficiency(self.dexterity)

    def damage(self):
        return self._damage(1, 6, self.dexterity)
