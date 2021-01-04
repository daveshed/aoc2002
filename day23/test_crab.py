import unittest

import crab
from linkedlist import CircularLinkedList

class Part1TestGroup(unittest.TestCase):
    EXAMPLE_INPUT = "389125467"
    EXPECTED_OUTPUT = [
        ([3, 8, 9, 1, 2, 5, 4, 6, 7], 3,), # initial state
        ([3, 2, 8, 9, 1, 5, 4, 6, 7], 2,),
        ([3, 2, 5, 4, 6, 7, 8, 9, 1], 5,),
        ([7, 2, 5, 8, 9, 1, 3, 4, 6], 8,),
        ([3, 2, 5, 8, 4, 6, 7, 9, 1], 4,),
        ([9, 2, 5, 8, 4, 1, 3, 6, 7], 1,),
        ([7, 2, 5, 8, 4, 1, 9, 3, 6], 9,),
        ([8, 3, 6, 7, 4, 1, 9, 2, 5], 2,),
        ([7, 4, 1, 5, 8, 3, 9, 2, 6], 6,),
        ([5, 7, 4, 1, 8, 3, 9, 2, 6], 5,),
        ([5, 8, 3, 7, 4, 1, 9, 2, 6], 8,),
    ]

    def setUp(self):
        self.cups = crab.make_cups(self.EXAMPLE_INPUT)

    def test_example_part_1(self):
        _, actual_label = self.EXPECTED_OUTPUT[0]
        for i, (expected_order, expected_label,) in enumerate(self.EXPECTED_OUTPUT):
            self.assertEqual(
                expected_label,
                actual_label,
                msg=f"FAILED on move {i}")
            self.assertEqual(
                CircularLinkedList(expected_order),
                self.cups,
                msg=f"FAILED on move {i}")
            actual_label = crab.move_cups(expected_label, self.cups)

    def test_example_part_1(self):
        self.assertEqual(
            '92658374',
            crab.solution_part_1(labels=self.EXAMPLE_INPUT, moves=10))
        self.assertEqual(
            '67384529',
            crab.solution_part_1(labels=self.EXAMPLE_INPUT, moves=100))

    def test_example_part_2(self):
        self.assertEqual(
            '149245887792',
            crab.solution_part_2(labels=self.EXAMPLE_INPUT))
