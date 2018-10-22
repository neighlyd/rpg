from unittest import TestCase
from world_map.world_map import WorldMap
from world_map.zones import DungeonZone


class TestEmptyWorldMapGeneration(TestCase):
    def setUp(self):
        self.world = WorldMap()

    def test_empty_zone_index(self):
        expected = {}
        self.assertEqual(expected, self.world.zone_index)

    def test_empty_zone_array(self):
        expected = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.assertEqual(expected, self.world.zone_array)


class TestZoneExploration(TestCase):

    def setUp(self):
        self.world = WorldMap()
        self.starting_zone = DungeonZone(self.world)

    def test_initial_zone_index(self):
        expected_zone_index = {self.starting_zone: [1, 1]}
        self.assertEqual(expected_zone_index, self.world.zone_index)

    def test_add_initial_dungeon(self):
        expected_zone_array = [
            [None, None, None],
            [None, self.starting_zone, None],
            [None, None, None]
        ]
        self.assertEqual(expected_zone_array, self.world.zone_array)

    def test_query_non_existent_neighbor_zone(self, direction=None, flag=False):
        if direction and flag:
            query_direction = self.starting_zone.query_neighbor(direction)
            self.assertTrue(query_direction)
        elif direction and not flag:
            query_direction = self.starting_zone.query_neighbor(direction)
            self.assertFalse(query_direction)
        elif not direction and not flag:
            print('Querying non-existent neighbor to the North...')
            query_north = self.starting_zone.query_neighbor('north')
            print(query_north)
            self.assertFalse(query_north)

            print('Querying non-existent neighbor to the East...')
            query_east = self.starting_zone.query_neighbor('east')
            print(query_east)
            self.assertFalse(query_east)

            print('Querying non-existent neighbor to the South...')
            query_south = self.starting_zone.query_neighbor('south')
            print(query_south)
            self.assertFalse(query_south)

            print('Querying non-existent neighbor to the West...')
            query_west= self.starting_zone.query_neighbor('west')
            print(query_west)
            self.assertFalse(query_west)

    def test_room_index_length(self):
        """
            There should be 9 rooms in the room index.
        """
        self.assertEqual(9, len(self.starting_zone.room_index))

    def test_room_array_and_index(self):
        """
            Check to see if a zone's `room_array` and `room_index` match up. Do this by creating a new `room_list` out
            of the `room_array`. Then use `all()` to compare that with the keys in `room_index`.
        :return:
        """
        room_list = []
        for row in self.starting_zone.room_array:
            for room in row:
                room_list.append(room)
        self.assertTrue(all(room in room_list for room in self.starting_zone.room_index))

    def test_create_new_zone(self):
        self.world.create_random_zone('north', self.starting_zone)
        self.test_query_non_existent_neighbor_zone('north', True)

    def test_fill_map_with_zones(self):
        self.world.create_random_zone('north', self.starting_zone)
        self.world.create_random_zone('east', self.starting_zone)
        self.world.create_random_zone('south', self.starting_zone)
        self.world.create_random_zone('west', self.starting_zone)
        self.test_query_non_existent_neighbor_zone(flag=True)
