from .mobs import MOB_OPTIONS
from .mob_classes import Monster


def spawn_mob(mob_name, room):
    if mob_name in MOB_OPTIONS:
        mob = MOB_OPTIONS[mob_name]
        return Monster(
            mob["name"],
            mob["max_hp"],
            mob["physical_defense"],
            mob["xp"],
            room,
            mob["description"],
            mob["armor_options"],
            mob["weapon_options"],
        )
