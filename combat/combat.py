import math
from collections import namedtuple


def attack_of_opportunity(player, text_input, sneak=None):
    text_input = ' '.join(text_input)
    if sneak:
        # TODO: Add sneak percent chance for Rogues.
        pass
    else:
        if len(player.room.mobs) > 0:
            for idx, mobs in player.room.mobs.items():
                for mob in mobs:
                    if mob.stunned == 0:
                        monster_aoo = (f"The {mob.name} was still in the {player.room} while you were attempting to "
                                       f"{text_input}. It got a free attack against you.")
                        player.add_messages(monster_aoo)
                        player.journal.add_entry(f"(Round {player.turn_counter}): " + monster_aoo)
                        mob.attack_player(player)
    player.turn_counter += 1


def attack_action(attacker, target, damage_modifier=None):
    """
       Method for performing the logic to check attack rolls against hit tables.
    :param attacker: An object representing the creature doing the attack.
    :param target: An object representing the target of the attack.
    :param damage_modifier: A tuple containing an operator function and what should be in the b position of said
                            operator. See https://docs.python.org/3.6/library/operator.html for more information.
    :return: A namedtuple with 3 positions: (Hit Success/Failure, Hit Type, Damage Amount)
    """
    atk_roll = attacker.roll_attack()
    atk_roll = target.reduce_attack_roll(atk_roll)
    damage = 0
    hit = False
    if atk_roll > target.miss:
        if atk_roll > target.miss + target.dodge:
            damage = attacker.roll_damage()
            if damage_modifier:
                damage = math.ceil(damage_modifier[0](damage, damage_modifier[1]))
            if atk_roll > target.miss + target.dodge + target.crit:
                hit_type = "hit"
                hit = True
            else:
                # Hit is a critical attack. Multiple damage by 2.
                damage = attacker.roll_damage() * 2
                hit_type = "crit"
                hit = True
            target.current_hp -= damage
        else:
            # Hit will be a dodge.
            hit_type = "dodge"
    else:
        # Hit will be a miss.
        hit_type = "miss"
    Report = namedtuple("Report", ("hit", "hit_type", "damage"))
    report = Report(hit, hit_type, damage)
    return report

