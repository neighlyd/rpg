class ItemBase:

    def __init__(self, name=None, description=None, weight=None, price=None):
        self.name = name
        self.description = description
        self.weight = weight
        self.price = price

    def describe(self):
        return f"{self.description}"


class LootItem(ItemBase):
    pass


class BatWing(LootItem):

    def __init__(self):
        super().__init__(
            name="Bat Wing",
            description="A leathery, tattered wing of a sky rat.",
            weight=0.1,
            price=1
        )