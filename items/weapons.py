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

    def __init__(self, attack_bonus=None, damage_min=None, damage_max=None, special=None, **kwargs):
        super().__init__(**kwargs)
        self.attack_bonus = attack_bonus
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.special = special

    def brief_description(self):
        return f"{self.name} (Atk: +{self.attack_bonus}, Dam: {self.damage_min}-{self.damage_max})"

    def __str__(self):
        weapon_details = (
            f"{self.name} - Attack Bonus: +{self.attack_bonus}, Damage Range: {self.damage_min}-{self.damage_max}\n"
            f"(Weight: {self.weight}lbs. Value: {self.price} g):\n"
            f"{self.description}\n"
        )
        return weapon_details


class Fists(Weapon):
    # A special class for when the player doesn't have a weapon equipped (avoids having to import spawn_item here, which
    # results in a circular import).

    def __init__(self):
        super().__init__(
            name="Fists",
            description="Good 'ole Lefty and Righty.",
            weight=None,
            price=None,
            attack_bonus=+0,
            damage_min=1,
            damage_max=2,
            special=None
        )


class Blade(Weapon):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Dagger(Blade):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Sword(Blade):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Staff(Weapon):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RustyDagger(Dagger):

    def __init__(self):
        super().__init__(
            name="Rusty Dagger",
            description="More rust now than metal; twisted and evil.",
            weight=1.0,
            price=0.0,
            attack_bonus=+0,
            damage_min=1,
            damage_max=3,
            special=None
        )


class RustySword(Sword):

    def __init__(self):
        super().__init__(
            name="Rusty Sword",
            description="A family heirloom that has seen better days.",
            weight=5.0,
            price=0.0,
            attack_bonus=+2,
            damage_min=1,
            damage_max=5,
            special=None
        )


class WalkingStaff(Staff):

    def __init__(self):
        super().__init__(
            name="Walking Staff",
            description="A gnarled walking staff that you have used all your life.",
            weight=5.0,
            price=0.0,
            attack_bonus=+2,
            damage_min=1,
            damage_max=5,
            special=None
        )