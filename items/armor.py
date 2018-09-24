import operator

from items.items import ItemBase


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

    ARMOR_ADJECTIVES = {
        "rough spun": {
            "int_boost": (operator.add, 1)
        },
        "hardy": {
            "str_boost": (operator.add, 1)
        },
        "deft": {
            "dex_boost": (operator.add, 1)
        }
    }

    def __init__(self, physical_defense=None, slot=None, adjectives=None, reductions=None, **kwargs):
        super().__init__(**kwargs)
        self.physical_defense = physical_defense
        self.slot = slot
        self.int_boost = 0
        self.str_boost = 0
        self.dex_boost = 0
        self.adjectives = adjectives
        self.reductions = []
        if adjectives:
            self.apply_adjectives()

    def apply_adjectives(self):
        for adj in self.adjectives:
            self.name = adj.title() + " " + self.name
            for ability, amount in self.ARMOR_ADJECTIVES[adj.lower()].items():
                attr = getattr(self, ability)
                # amount is a tuple containing an operator and an amount (e.g. (operator.mul, 2)). We take that operator
                # func and then put the existing attribute and amount through it to get the resulting attribute.
                attr = amount[0](attr, amount[1])
                setattr(self, ability, attr)

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
    pass


class Chain(Armor):

    def __init__(self, **kwargs):
        super().__init__(
            reductions=[('slashing', 0.05)],
            **kwargs
        )


class Tunic(Cloth):

    def __init__(self, **kwargs):
        super().__init__(
            name="Tunic",
            description="A tattered, sweat-stained, and road-worn tunic that is more patches than shirt at this point.",
            weight=2.0,
            price=0.0,
            physical_defense=0.02,
            slot="chest",
            **kwargs
        )


class Robe(Cloth):

    def __init__(self, **kwargs):
        super().__init__(
            name="Robes",
            description="A tattered, sweat-stained, and road-worn set of robes.",
            weight=2.0,
            price=0.0,
            physical_defense=0.02,
            slot="chest",
            **kwargs
        )
