def attack_of_opportunity(player, text_input):
    text_input = ' '.join(text_input)
    if len(player.room.mobs) > 0:
        for idx, mobs in player.room.mobs.items():
            for mob in mobs:
                monster_aoo = (f"The {mob.name} was still in the {player.room} while you were attempting to "
                               f"{text_input}. It gets a free attack against you.")
                monster_aoo_journal = (f"The {mob.name} was still in the {player.room} while you were attempting to"
                                       f" {text_input}. It got a free attack against you.")
                player.add_messages(monster_aoo)
                player.journal.add_entry(monster_aoo_journal)
                mob.attack_player(player)
                player.turn_counter += 1
