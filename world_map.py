"""
    Rooms will be stored in a 2-dimensional array. The room_index var will be a key-index pair linking a room's ID with
    its location within this array for quick lookup. When the Room Array is updated with a new row or column, the
    room_index will also be updated to reflect changes to existing room's indices.
"""


class WorldMap:

    def __init__(self):
        self.room_index = dict()
        self.room_array = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def update_room_index(self, direction):
        # adding rooms to the north or west increases the array indices by 1
        # (either main list for North or sublist for West).
        # We need to iterate through our room_index and increment existing values to reflect these changes.
        if direction == "north":
            for key, value in self.room_index.items():
                value[0] = value[0] + 1
        if direction == "west":
            for key, value in self.room_index.items():
                value[1] = value[1] + 1
        print(self.room_index)

    def _show_map(self):
        known_map = (f"\n")
        for row in self.room_array:
            known_map = known_map + f"{row}\n"
        return known_map

    def expand_dungeon(self, direction):
        # get current E/W width of dungeon.
        # add new row to North (i.e. index 0 of main list).
        if direction == "north":
            width = len(self.room_array[0])
            self.room_array.insert(0, [None for x in range(width)])
            # because the indices of the array items changed, update room_index dict.
            self.update_room_index(direction)
        # add a new column to the East (i.e. the very last index of all sublists)
        if direction == "east":
            for row in self.room_array:
                row.append(None)
        # add new row to South (i.e. the very last index of main list).
        if direction == "south":
            width = len(self.room_array[0])
            self.room_array.append([None for x in range(width)])
        # add a new column to the West (i.e. index 0 of all sublists)
        if direction == "west":
            for row in self.room_array:
                row.insert(0, None)
            # because the indices of the array items changed, update room_index dict.
            self.update_room_index(direction)
