_weapon_template = {"Name": {"name": "<NAME HERE>",
                             "description": "<DESCRIPTION HERE>.",
                             "weight": "<WEIGHT FLOAT HERE>",
                             "price": "<PRICE FLOAT HERE>",
                             "attack": "<ATTACK BONUS HERE>"}
                   }

WEAPONS = {
    "Rusty Sword": {
        "name": "Rusty Sword",
        "description": "A family heirloom that has seen better days.",
        "weight": "5.0",
        "price": "0.0",
        "attack": "+5"
    },
    "Walking Staff": {
        "name": "Walking Staff",
        "description": "A trusty walking staff that you have used all your life.",
        "weight": "5.0",
        "price": "0.0",
        "attack": "+5"
    },
}


class ItemBase:

    def __init__(self, name, description, weight=None, price=None):
        self.name = name
        self.description = description
        self.weight = weight
        self.price = price


class Weapon(ItemBase):

    def __init__(self, name, description, weight, price, attack):
        super().__init__(name, description, weight, price)
        self.attack = attack

    def __str__(self):
        weapon_details = (
            f"{self.name} - Attack: {self.attack} (Weight: {self.weight}lbs. Value: {self.price} g):\n"
            f"{self.description}\n"
        )
        return weapon_details


class Armor(ItemBase):

    def __init__(self, name, description, weight, price, defense):
        super().__init__(name, description, weight, price)
        self.defense = defense

    def __str__(self):
        weapon_details = (
            f"{self.name} - {self.defense}\n"
            f"({self.weight}lbs., {self.price}g.)\n"
            f"{self.description}\n"
        )
        return weapon_details


class Inventory:

    def __init__(self):
        self.items = dict()

    def add_item(self, item):
        self.items[item] = item

    def __str__(self):
        inventory = f"Your Inventory:\n"
        i = 0
        for item in self.items:
            i += 1
            if i > 1:
                inventory = inventory + f"----------------------------\n"
                inventory = inventory + f"{item}\n"
            else:
                inventory = inventory + f"{item}\n"
        return inventory


