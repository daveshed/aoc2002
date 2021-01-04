import unittest

from linkedlist import CircularLinkedList

class LinkedListTestGroup(unittest.TestCase):
    EXPECTED = [3, 8, 9, 1, 2, 5, 4, 6, 7]

    def setUp(self):
        self.my_list = CircularLinkedList(self.EXPECTED)

    def test_ordering_respected_on_conversion_to_list(self):
        self.assertEqual(
            self.EXPECTED,
            self.my_list.to_list())
        self.assertEqual(len(self.EXPECTED), len(self.my_list))

    def test_sub_list_can_be_read(self):
        self.assertEqual(
            [1, 2, 5],
            self.my_list.to_list(location=1, length=3))

    def test_can_convert_to_list_starting_at_any_element(self):
        self.assertEqual(
            [1, 2, 5, 4, 6, 7, 3, 8, 9],
            self.my_list.to_list(location=1))

    def test_elements_appended_list_grows(self):
        self.my_list.append(20)
        self.assertEqual(
            [3, 8, 9, 1, 2, 5, 4, 6, 7, 20],
            self.my_list.to_list())
        self.assertEqual(10, len(self.my_list))

    def test_move_chunk_within_list_ordering_should_match(self):
        ([3, 2, 8, 9, 1, 5, 4, 6, 7], 2,),
        ([3, 2, 5, 4, 6, 7, 8, 9, 1], 5,),
        ([7, 2, 5, 8, 9, 1, 3, 4, 6], 8,),
        ([3, 2, 5, 8, 4, 6, 7, 9, 1], 4,),
        ([9, 2, 5, 8, 4, 1, 3, 6, 7], 1,),
        self.my_list.move(dst=2, src=8, length=3)
        self.assertEqual(
            CircularLinkedList([3, 2, 8, 9, 1, 5, 4, 6, 7]),
            self.my_list)
        self.my_list.move(dst=7, src=8, length=3)
        self.assertEqual(
            CircularLinkedList([3, 2, 5, 4, 6, 7, 8, 9, 1]),
            self.my_list)
        self.my_list.move(dst=3, src=4, length=3)
        self.assertEqual(
            CircularLinkedList([7, 2, 5, 8, 9, 1, 3, 4, 6]),
            self.my_list)
        self.my_list.move(dst=7, src=9, length=3)
        self.assertEqual(
            CircularLinkedList([3, 2, 5, 8, 4, 6, 7, 9, 1]),
            self.my_list)
        self.assertEqual(9, len(self.my_list))

    def test_move_chunk_already_in_position_nothing_changes(self):
        self.my_list.move(dst=7, src=3, length=2)
        self.assertEqual(
            [3, 8, 9, 1, 2, 5, 4, 6, 7],
            self.my_list.to_list())

    def test_clearing_list_removes_all_elements(self):
        self.my_list.clear()
        self.assertFalse(self.my_list)
        self.assertEqual(0, len(self.my_list))

    def test_element_is_member_should_return_true(self):
        self.assertTrue(9 in self.my_list)

    def test_is_iterable(self):
        for expected, actual in zip(self.EXPECTED, self.my_list):
            self.assertEqual(expected, actual)

    def test_element_is_not_member_should_return_false(self):
        self.assertTrue(9 in self.my_list)

    def test_calling_max_retrieves_largest_element(self):
        self.assertEqual(9, max(self.my_list))

    def test_get_next_element_should_get_adjacent(self):
        self.assertEqual(5, self.my_list.next(location=2))
        self.assertEqual(1, self.my_list.previous(location=2))

    def test_same_lists_compared_rotated_should_be_equal(self):
        rotated = self.EXPECTED[-2:] + self.EXPECTED[:-2]
        self.assertTrue(CircularLinkedList(rotated) == self.my_list)

    def test_different_compared_should_not_be_equal(self):
        rotated = self.EXPECTED + [19, 20,]
        self.assertFalse(CircularLinkedList(rotated) == self.my_list)
