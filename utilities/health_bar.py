def health_bar(obj):
    """
        A visual representation of player's health, that changes color based upon their percentage of current health
        (green > 50%, yellow > 25%, red <= 25%).
        Uses Blessings module term options to color code the health display.
        N.B.: Because the f-string is returned to a function running Blessings module, the 'term' variable is used to
        modify the color.
    :param obj: Player object
    :return: fstring formatted with appropriate blessings term colors.
    """
    hp_out = f"HP:"
    if obj.current_hp <= obj.max_hp * 0.25:
        hp_out += f"{term.red}"
    elif obj.current_hp <= obj.max_hp * 0.5:
        hp_out += f"{term.yellow}"
    hp_out += f"{obj.current_hp}/{obj.max_hp}"
    return hp_out
