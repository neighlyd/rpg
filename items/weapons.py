from .inventory import ItemBase


class Weapon(ItemBase):

    def __init__(self, name, description, weight, price, attack, special=None):
        super().__init__(name, description, weight, price)
        self.attack = attack
        self.special = special

    def __str__(self):
        weapon_details = (
            f"{self.name} - Attack: {self.attack} (Weight: {self.weight}lbs. Value: {self.price} g):\n"
            f"{self.description}\n"
        )
        return weapon_details


class NullWeapon(Weapon):

    def __init__(self):
        super().__init__("", "", "", "", 0)


class RustySword(Weapon):

    def __init__(self):
        super().__init__(
            "Rusty Sword",
            "A family heirloom that has seen better days.",
            5.0,
            0.0,
            +1
        )


class WalkingStaff(Weapon):

    def __init__(self):
        super().__init__(
            "Walking Staff",
            "A gnarled walking staff that you have used all your life.",
            5.0,
            0.0,
            +2
        )
