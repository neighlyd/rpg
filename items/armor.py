from items.inventory import ItemBase


class EquippedArmor:

    def __init__(self, head=None, chest=None, feet=None):
        self.head = head if head else NullArmorPiece()
        self.chest = chest if chest else NullArmorPiece()
        self.feet = feet if feet else NullArmorPiece()

    def physical_defense(self):
        return self.head.physical_defense + self.chest.physical_defense + self.feet.physical_defense

    def __str__(self):
        equipped_armor = (
            f"Equipped Armor\n"
            f"Head: {self.head if not NullArmorPiece else 'Nothing'}\n"
            f"Chest: {self.chest if not NullArmorPiece else 'Nothing'}\n"
            f"Feet: {self.feet if not NullArmorPiece else 'Nothing'}\n"
        )
        return equipped_armor



class ArmorPiece(ItemBase):

    def __init__(self, name, description, weight, price, physical_defense, slot=None, special=None):
        super().__init__(name, description, weight, price)
        self.physical_defense = physical_defense
        self.slot = slot
        self.special = special

    def __str__(self):
        weapon_details = (
            f"{self.name} - Defense: {self.physical_defense} (Weight: {self.weight}lbs. Value: {self.price} g)\n"
            f"{self.description}\n"
        )
        return weapon_details


class NullArmorPiece(ArmorPiece):

    def __init__(self):
        super().__init__("Nothing", "", "", "", 0)


class RoughSpunTunic(ArmorPiece):

    def __init__(self):
        super().__init__(
            "Rough-Spun Tunic",
            "A tattered, sweat-stained, and road-worn tunic that is more patches than shirt at this point.",
            2.0,
            0.0,
            +2,
            "chest",
        )


class RoughSpunRobe(ArmorPiece):

    def __init__(self):
        super().__init__(
            "Rough-Spun Robe",
            "A tattered, sweat-stained, and road-worn set of robes.",
            3.0,
            0.0,
            +1,
            "chest",
        )
