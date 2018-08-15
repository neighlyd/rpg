# _weapon_template = {"<NAME>": {"name": "<NAME HERE>",
#                              "description": "<DESCRIPTION HERE>.",
#                              "weight": "<WEIGHT FLOAT HERE>",
#                              "price": "<PRICE FLOAT HERE>",
#                              "attack": "<ATTACK BONUS/PENALTY HERE>"}
#                     }
#
# _armor_template = {"<NAME>": {"name": "<NAME HERE>",
#                               "description": "<DESCRIPTION HERE>",
#                               "weight": "<WEIGHT FLOAT HERE>",
#                               "price": "<PRICE FLOAT HERE>",
#                               "defense": "<DEFENSE BONUS/PENALTY HERE>"}
#                    }
#
# WEAPONS = {
#     "Rusty Sword": {"name": "Rusty Sword",
#                     "description": "A family heirloom that has seen better days.",
#                     "weight": "5.0",
#                     "price": "0.0",
#                     "attack": "+1"
#                     },
#     "Walking Staff": {"name": "Walking Staff",
#                       "description": "A trusty walking staff that you have used all your life.",
#                       "weight": "5.0",
#                       "price": "0.0",
#                       "attack": "+2"
#                       },
# }
#
# ARMOR = {
#     "Rough-Spun Tunic": {"name": "Rough-Spun Tunic",
#                          "description": "A tattered, sweat-stained, and road-worn tunic that is more patches than shirt at this point.",
#                          "weight": "2.0",
#                          "price": "0.0",
#                          "physical_defense": "+2"
#                          },
#     "Rough-Spun Robes": {"name": "Rough-Spun Robes",
#                          "description": "A tattered, sweat-stained, and road-worn set of robes.",
#                          "weight": "3.0",
#                          "price": "0.0",
#                          "physical_defense": "+1"
#                          },
# }


class ItemBase:

    def __init__(self, name, description, weight=None, price=None):
        self.name = name
        self.description = description
        self.weight = weight
        self.price = price


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


