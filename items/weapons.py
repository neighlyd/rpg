import operator
from items.items import ItemBase


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
    WEAPON_ADJECTIVES = {
        "clobbering": {
            "modifiers": {
                "stun": (operator.add, 1)
            },
            "description": "It's time."
        },
        "cracked": {
            "modifiers": {
                "attack": (operator.sub, 1),
            },
            "description": "A leftover weapon covered in poor, little lice."
        },
        "deft": {
            "modifiers": {
                "attack": (operator.add, 2)
            },
        },
        "flaming": {
            "modifiers": {
                "damage_min": (operator.add, 2),
                "damage_max": (operator.add, 2),
            },
            "description": "No relation to the game creator."
        },
        "rusty": {
            "modifiers": {
                "damage_max": (operator.sub, 1),
            },
            "description": "It actually goes by Rustin."
        },
        "smoldering": {
            "modifiers": {
                "damage_min": (operator.add, 1),
                "damage_max": (operator.add, 1),
            },
        },
        "twisted": {
            "modifiers": {
                "damage_min": (operator.add, 1)
            },
        },
        "wicked": {
            "modifiers": {
                "damage_max": (operator.add, 2),
            },
        },
        "quick": {
            "modifiers": {
                "cd_redux": (operator.add, 1),
            },
        }
    }

    def __init__(self, attack=0, damage_min=1, damage_max=None, main_stat=None, damage_type=None, special=None,
                 success_verb=None, fail_verb=None, adjectives=None, level=1, **kwargs):
        super().__init__(**kwargs)
        self.attack = attack
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.main_stat = main_stat
        self.damage_type = damage_type
        self.stun = 0
        self.cd_redux = 0  # for cooldown reduction.
        self.special = special
        self.success_verb = success_verb
        self.fail_verb = fail_verb
        self.adjectives = adjectives
        self.description = None
        if self.adjectives:
            self.apply_adjectives()

    def apply_adjectives(self):
        for adj in self.adjectives:
            self.name = adj.title() + " " + self.name
            for ability, amount in self.WEAPON_ADJECTIVES[adj.lower()]["modifiers"].items():
                attr = getattr(self, ability)
                # amount is a tuple containing an operator and an amount (e.g. (operator.mul, 2)). We take that operator
                # func and then put the existing attribute and amount through it to get the resulting attribute.
                attr = amount[0](attr, amount[1])
                setattr(self, ability, attr)
                if self.damage_max < 1:
                    self.damage_max = 1
                if self.damage_min < 1:
                    self.damage_min = 1
                if self.damage_max < self.damage_min:
                    self.damage_max = self.damage_min
            if "description" in self.WEAPON_ADJECTIVES[adj.lower()]:
                self.description = self.WEAPON_ADJECTIVES[adj.lower()]["description"]

    def brief_description(self):
        return f"{self.name} (Atk: +{self.attack}, Dam: {self.damage_min}-{self.damage_max})"

    def __str__(self):
        weapon_details = (
            f"{self.name} - Attack Bonus: {self.attack}, Damage Range: {self.damage_min}-{self.damage_max}\n"
            # f"(Weight: {self.weight}lbs. Value: {self.price} g):\n"
        )
        if self.stun > 0:
            weapon_details += f"Stun: {self.stun} "
        if self.cd_redux:
            weapon_details += f"Cooldown Redux: {self.cd_redux} "
        if self.description:
            weapon_details += (
                f"\n------------------------\n"
                f"{self.description}"
            )
        return weapon_details


class Fists(Weapon):
    # A special class for when the player doesn't have a weapon equipped (avoids having to import spawn_item here, which
    # results in a circular import).

    def __init__(self, **kwargs):
        super().__init__(
            name="Fists",
            damage_min=1,
            damage_max=2,
            main_stat="strength",
            damage_type="crush",
            **kwargs
        )
        self.description = "Good 'ole Lefty and Righty."
        self.success_verb = "punched"
        self.fail_verb = self.success_verb + " at"


class Bite(Weapon):

    def __init__(self, **kwargs):
        super().__init__(
            name="Teeth",
            damage_min=1,
            damage_max=2,
            damage_type="pierce",
            **kwargs
        )
        self.description = "Chompy Chompy!"
        self.success_verb = "bit"
        self.fail_verb = "tried to bite"


class Dagger(Weapon):

    def __init__(self, **kwargs):
        super().__init__(
            name="Dagger",
            weight=1.0,
            damage_min=1,
            damage_max=3,
            main_stat="dexterity",
            damage_type="pierce",
            **kwargs
        )
        self.success_verb = "stabbed"
        self.fail_verb = self.success_verb + " at"


class Sword(Weapon):

    def __init__(self, **kwargs):
        super().__init__(
            name="Sword",
            weight=5.0,
            price=0.0,
            attack=+2,
            damage_min=1,
            damage_max=5,
            main_stat="strength",
            damage_type="slash",
            **kwargs
        )
        self.success_verb = "swung at"
        self.fail_verb = self.success_verb + " at"
        self.main_stat = 'strength'


class Staff(Weapon):

    def __init__(self, **kwargs):
        super().__init__(
            name="Staff",
            weight=5.0,
            damage_min=1,
            damage_max=4,
            main_stat="intelligence",
            damage_type="crush",
            **kwargs,
        )
        self.success_verb = "smashed"
        self.fail_verb = "swung at"


class RustyDagger(Dagger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Rusty Dagger"
        self.description = "More rust now than metal; twisted and evil."


class BatFang(Dagger):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Bat Fang"
        self.description = ("You ripped the tooth out of a helpless flying rat, which you are now using to slaughter "
                            "its kin... And you call them the monsters.")
        self.damage_min = self.damage_min*2


class RustySword(Sword):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Rusty Sword"
        self.description = "A family heirloom that has seen better days."
        self.damage_min=200
        self.damage_max=200


class WalkingStaff(Staff):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Walking Staff"
        self.description = "A gnarled walking staff that you have used all your life."
