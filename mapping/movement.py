from .mapping import check_borders, Zone
from errors import RoomDoesNotExist, EndGameDied

movement_index = {
    "north": 1 << 1,
    "east": 1 << 2,
    "south": 1 << 3,
    "west": 1 << 4
}


def move_action(player, choice, world_map):
    # Check if there is a monster in the room. Currently, only one monster will be assigned per room. I'll change
    # this later. If the player attempts to leave while there is still a monster in the room, the monster will get a
    # free attack.
    if len(player.room.mobs) > 0:
        for idx, mobs in player.room.mobs.items():
            for mob in mobs:
                player.add_messages(f"The {mob.name} was still in the room while you were attempting to flee. "
                                    f"It gets a free attack against you.")
                player.journal.add_entry(f"You tried to leave {player.room.name} before killing the {mob.name}. "
                                         f"In your haste, it got a free attack on you.")
        # TODO: Add monster attack.
                if player.current_hp <= 0:
                    raise EndGameDied(f"You were killed by the {mob.name}.")
    if movement_index[choice] in player.room.active_doors:
        this_room_index = player.room.zone.room_index[id(player.room)]
        zone_width = len(player.room.zone.room_array) - 1
        zone_height = len(player.room.zone.room_array) - 1
        # See if the player is leaving the Zone. If not, simply move them to the next room in the Zone array.
        if check_borders(this_room_index, zone_width, zone_height, choice):
            # Check to see if a Zone exists in the direction that the player is travelling.
            neighboring_zone = player.room.zone.query_neighbor(choice)
            if not neighboring_zone:
                # Create a new Zone if one doesn't exist.
                neighboring_zone = Zone(world_map, choice, player.room.zone)
            # Move player to new Room in new Zone.
            if choice == "north":
                new_room = neighboring_zone.room_array[len(neighboring_zone.room_array) - 1][this_room_index[1]]
            if choice == "east":
                new_room = neighboring_zone.room_array[this_room_index[0]][0]
            if choice == "south":
                new_room = neighboring_zone.room_array[0][this_room_index[1]]
            if choice == "west":
                new_room = neighboring_zone.room_array[this_room_index[0]][len(neighboring_zone.room_array[0]) - 1]
        # If player is staying in the same Zone, assign to room as needed.
        else:
            if choice == "north":
                if player.room.zone.room_array[this_room_index[0] - 1][this_room_index[1]]:
                    new_room = player.room.zone.room_array[this_room_index[0] - 1][this_room_index[1]]
                else:
                    raise RoomDoesNotExist
            elif choice == "east":
                if player.room.zone.room_array[this_room_index[0]][this_room_index[1] + 1]:
                    new_room = player.room.zone.room_array[this_room_index[0]][this_room_index[1] + 1]
                else:
                    raise RoomDoesNotExist
            elif choice == "south":
                if player.room.zone.room_array[this_room_index[0] + 1][this_room_index[1]]:
                    new_room = player.room.zone.room_array[this_room_index[0] + 1][this_room_index[1]]
                else:
                    raise RoomDoesNotExist
            elif choice == "west":
                if player.room.zone.room_array[this_room_index[0]][this_room_index[1] - 1]:
                    new_room = player.room.zone.room_array[this_room_index[0]][this_room_index[1] - 1]
                else:
                    raise RoomDoesNotExist
        player.journal.travel_entry(player.room, new_room, choice)
        player.assign_room(new_room)
    else:
        player.add_messages(f"You run into a wall.")
        player.journal.add_entry(f"You ran into a wall in {player.room.name}")
