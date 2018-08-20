def spawn_monster(player, monster):
    player.room._spawn_monster(monster.lower())


def kill_monster(player, monster):
    player.room.mobs[monster.title()][0].kill_monster()