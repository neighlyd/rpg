from items.item_classes import ItemBase


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


class Armor(ItemBase):

    def __init__(self, physical_defense=None, slot=None, special=None, **kwargs):
        super().__init__(**kwargs)
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
        super().__init__(physical_defense=0)


class Cloth(Armor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RoughSpunTunic(Cloth):

    def __init__(self):
        super().__init__(
            name="Rough-Spun Tunic",
            description="A tattered, sweat-stained, and road-worn tunic that is more patches than shirt at this point.",
            weight=2.0,
            price=0.0,
            physical_defense=+2,
            slot="chest",
        )


class RoughSpunRobe(Cloth):

    def __init__(self):
        super().__init__(
            name="Rough-Spun Robe",
            description="A tattered, sweat-stained, and road-worn set of robes.",
            weight=2.0,
            price=0.0,
            physical_defense=+1,
            slot="chest",
        )
