# Percentage chances should go in ascending order and are not cumulative (i.e. if one item has 25% chance and another
# has 75, it will check for the 25% item first, then the 75% item next. It will not have a 100% chance of having
# an item)

MOB_OPTIONS = {
    "Goblin": {
        "name": "Goblin",
        "description": "A pathetic, snivelling creature.",
        "max_hp": 7,
        "physical_defense": 7,
        "xp": 10,
        "armor_options": [(RoughSpunTunic, 25), (RoughSpunRobe, 75)],
        "weapon_options": [(RustyDagger, 100), ],
    }
}
