class ItemBase:

    def __init__(self, name, description, weight=None, price=None):
        self.name = name
        self.description = description
        self.weight = weight
        self.price = price


class EquippedArmor:

    def __init__(self, head=None, chest=None, feet=None):
        self.head = head if head else NullArmor()
        self.chest = chest if chest else NullArmor()
        self.feet = feet if feet else NullArmor()

    def physical_defense(self):
        return self.head.physical_defense + self.chest.physical_defense + self.feet.physical_defense

    def __str__(self):
        equipped_armor = (
            f"Equipped Armor (Total Def: {self.physical_defense()})\n"
            f"Head: {self.head.brief_description() if self.head.name is not None else 'Nothing'}\n"
            f"Chest: {self.chest.brief_description() if self.chest.name is not None else 'Nothing'}\n"
            f"Feet: {self.feet.brief_description() if self.feet.name is not None else 'Nothing'}\n"
        )
        return equipped_armor


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


class Armor(ItemBase):

    def __init__(self, name, description, weight, price, physical_defense, slot=None, special=None):
        super().__init__(name, description, weight, price)
        self.physical_defense = physical_defense
        self.slot = slot
        self.special = special

    def brief_description(self):
        brief_description = (
            f"{self.name} (Def: {self.physical_defense})"
        )
        return brief_description

    def __str__(self):
        if self.name is not None:
            armor_details = (
                f"{self.name} - Defense: {self.physical_defense} (Weight: {self.weight}lbs. Value: {self.price} g)\n"
                f"{self.description}\n"
            )
        else:
            armor_details = f"You are not wearing any armor.\n"
        return armor_details


class NullArmor(Armor):
    # A special class for when the player isn't wearing any armor (avoids having to import spawn_item here, which
    # results in a circular import).

    def __init__(self):
        super().__init__(None, None, None, None, 0, None)


class Weapon(ItemBase):

    def __init__(self, name, description, weight, price, attack, damage_min, damage_max, special=None):
        super().__init__(name, description, weight, price)
        self.attack = attack
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.special = special

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

    def __init__(self):
        super().__init__(
            "Fists",
            "Good 'ole Lefty and Righty.",
            None,
            None,
            +0,
            1,
            2,
            None
        )
