from items.item_classes import ItemBase


class EquippedWeapon:

    def __init__(self, main_hand=None):
        self.main_hand = main_hand if main_hand else Fists()

    def attack_bonus(self):
        return self.main_hand.attack

    def damage_range(self):
        return f"{self.main_hand.damage_min}-{self.main_hand.damage_max}"

    def __str__(self):
        equipped_weapons = (
            f"Equipped Weapons:\n"
            f"Main Hand: {self.main_hand.brief_description()}\n"
        )
        return equipped_weapons


class Weapon(ItemBase):

    def __init__(self, attack=None, damage_min=None, damage_max=None, special=None, success_verb=None, fail_verb=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.attack = attack
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.special = special
        self.success_verb = success_verb
        self.fail_verb = fail_verb

    def brief_description(self):
        return f"{self.name} (Atk: +{self.attack}, Dam: {self.damage_min}-{self.damage_max})"

    def __str__(self):
        weapon_details = (
            f"{self.name} - Attack Bonus: +{self.attack}, Damage Range: {self.damage_min}-{self.damage_max}\n"
            f"(Weight: {self.weight}lbs. Value: {self.price} g):\n"
            f"{self.description}\n"
        )
        return weapon_details


class Fists(Weapon):
    # A special class for when the player doesn't have a weapon equipped (avoids having to import spawn_item here, which
    # results in a circular import).

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Fists"
        self.description = "Good 'ole Lefty and Righty."
        self.weight = None
        self.price = None
        self.attack = +0
        self.damage_min = 1
        self.damage_max = 2
        self.special = None
        self.success_verb = "punched"
        self.fail_verb = self.success_verb + " at"


class Bite(Weapon):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Teeth"
        self.description = "Chompy Chompy!"
        self.weight = None
        self.price = None
        self.attack = +0
        self.damage_min = 1
        self.damage_max = 1
        self.special = None
        self.success_verb = "bit"
        self.fail_verb = "tried to bite"


class Blade(Weapon):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Dagger(Blade):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.success_verb = "stabbed"
        self.fail_verb = self.success_verb + " at"
        self.weight = 1.0
        self.price = 0.0
        self.attack = +0
        self.damage_min = 1
        self.damage_max = 3
        self.special = None


class Sword(Blade):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.success_verb = "swung at"
        self.fail_verb = self.success_verb + " at"
        self.weight = 5.0
        self.price = 0.0
        self.attack = +2
        self.damage_min = 1
        self.damage_max = 5
        self.special = None


class Staff(Weapon):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.success_verb = "smashed"
        self.fail_verb = "swung at"
        self.weight = 5.0
        self.price = 0.0
        self.attack = +2
        self.damage_min = 1
        self.damage_max = 5
        self.special = None


class RustyDagger(Dagger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Rusty Dagger"
        self.description = "More rust now than metal; twisted and evil."


class RustySword(Sword):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Rusty Sword"
        self.description = "A family heirloom that has seen better days."


class WalkingStaff(Staff):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Walking Staff"
        self.description = "A gnarled walking staff that you have used all your life."


class BatSlayer(Dagger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name="Bat Slayer"
