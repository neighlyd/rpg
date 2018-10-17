from unittest import TestCase
from world_map.world_map import WorldMap
from world_map.zones import DungeonZone


class TestWorldMap(TestCase):
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

    def test_add_initial_dungeon(self):
        from world_map.zones import DungeonZone
        starting_zone = DungeonZone(self.world)
        expected_zone_index = {id(starting_zone): [1, 1]}
        self.assertEqual(expected_zone_index, self.world.zone_index)
