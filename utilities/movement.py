from errors import RoomDoesNotExist

movement_index = {
    "north": 1 << 1,
    "east": 1 << 2,
    "south": 1 << 3,
    "west": 1 << 4
}


def move_action(player, choice):
    if movement_index[choice] in player.room.active_doors:
        this_room_index = player.room.zone.room_index[player.room]
        # See if the player is leaving the Zone. If not, simply move them to the next room in the Zone array.
        if player.room.zone.check_zone_borders(this_room_index, choice):
            # Check to see if a Zone exists in the direction that the player is travelling.
            neighboring_zone = player.room.zone.query_neighbor(choice)
            if not neighboring_zone:
                # Create a new Zone if one doesn't exist.
                neighboring_zone = player.room.zone.world_map.create_random_zone(
                    travel_direction=choice, previous_zone=player.room.zone)
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
                try:
                    new_room = player.room.zone.room_array[this_room_index[0] - 1][this_room_index[1]]
                except IndexError:
                    raise RoomDoesNotExist
            elif choice == "east":
                try:
                    new_room = player.room.zone.room_array[this_room_index[0]][this_room_index[1] + 1]
                except IndexError:
                    raise RoomDoesNotExist
            elif choice == "south":
                try:
                    new_room = player.room.zone.room_array[this_room_index[0] + 1][this_room_index[1]]
                except IndexError:
                    raise RoomDoesNotExist
            elif choice == "west":
                try:
                    new_room = player.room.zone.room_array[this_room_index[0]][this_room_index[1] - 1]
                except IndexError:
                    raise RoomDoesNotExist
        player.assign_room(new_room)
        player.journal.travel_entry(player.room, new_room, choice)
    else:
        player.add_messages(f"You run into a wall.")
        player.journal.add_entry(f"(Round {player.turn_counter}): You ran into a wall in {player.room.name}")
