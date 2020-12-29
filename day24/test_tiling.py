import unittest

import tiling

EXAMPLE_INPUT = tiling.read_input(filename="example-input.txt")


class TilingTestGroup(unittest.TestCase):
    def setUp(self):
        self.floor = tiling.Floor.from_instructions(EXAMPLE_INPUT)

    def test_nwwswee_flips_reference_tile_itself(self):
        self.assertEqual(
            tiling.Vector(0, 0), tiling.Vector.from_directions("nwwswee"))

    def test_esew_flips_adjacent_tile_to_reference(self):
        self.assertEqual(
            tiling.Vector(1, 1), tiling.Vector.from_directions("esew"))

    def test_example_has_10_black_tiles(self):
        self.assertEqual(10, self.floor.count_black())

    def test_isolated_black_tile_is_flipped_back_to_white(self):
        floor = tiling.Floor()
        floor.flip_tile(tiling.Vector(0,0))
        # should have a black tile...
        self.assertEqual(1, floor.count_black())
        floor.update()
        # the single tile should have been flipped back to white...
        self.assertFalse(floor.count_black())

    def test_three_adjacent_black_tiles_two_more_black_tiles_flipped_each_side(self):
        floor = tiling.Floor()
        floor.flip_tile(tiling.Vector(0, 0))
        floor.flip_tile(tiling.Vector(0, 1))
        floor.flip_tile(tiling.Vector(0, -1))
        self.assertEqual(3, floor.count_black())
        floor.update()
        self.assertEqual(7, floor.count_black())

    def test_white_tile_with_two_black_neighbours_flipped_to_black(self):
        floor = tiling.Floor()
        # make the reference tile white with two black neighbours...
        floor.flip_tile(tiling.Vector(0, 1))
        floor.flip_tile(tiling.Vector(0, -1))
        self.assertEqual(2, floor.count_black())
        # updating should flip the tile in the middle but the neighbours will
        # flip back to white because they were isolated black tiles...
        floor.update()
        self.assertEqual(1, floor.count_black())

    def test_flip_tiles_each_day_matches_example(self):
        tile_count = [
            15,
            12,
            25,
            14,
            23,
            28,
            41,
            37,
            49,
            37,
        ]
        for count in tile_count:
            self.floor.update()
            self.assertEqual(count, self.floor.count_black())