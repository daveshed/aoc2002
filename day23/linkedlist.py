
class Node:

    def __init__(self, data):
        self._next = None
        self._previous = None
        self._data = data

    def __repr__(self):
        return f"Node(data={self.data})"

    @property
    def data(self):
        return self._data

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node
        node._previous = self

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, node):
        self._previous = node
        node._next = self


class CircularLinkedList:
    """A circular doubly linked list with fast hashtable lookup.

    The lookup is done on the value of each element added. Make sure that the
    values are hashable.
    """

    def __init__(self, data: iter=None):
        self._nodes = {}
        # remember the initial element that was inserted. It will serve as a
        # useful reference point for when the circle is converted to a list.
        self._origin = None
        if data is not None:
            for value in data:
                self.append(value)

    def __bool__(self):
        return bool(self._nodes)

    def __len__(self):
        return len(self._nodes)

    def __contains__(self, item):
        return item in self._nodes

    def __iter__(self):
        element = self._origin
        for _ in range(len(self)):
            yield element.data
            element = element.next

    def __eq__(self, other):
        # The lengths must match for equality...
        if len(self) != len(other):
            return False
        # They may be in the same order but rotated. We need to find the same
        # starting point...
        this = self._origin
        that = other._get_node(self._origin.data, 0)
        for _ in range(len(self)):
            if this.data != that.data:
                return False
            this = this.next
            that = that.next
        return True

    def __repr__(self):
        return '->'.join(str(data) for data in self)

    def next(self, location):
        """Get the next cup from the given location"""
        return self._get_node(location, 1).data

    def previous(self, location):
        """Get the next cup from the given location"""
        return self._get_node(location, -1).data

    def move(self, dst, src, length):
        """Move a portion of the list with the specified length from the src
        location to the dst location"""
        # early return if there is nothing to do...
        if self._nodes[dst].next == self._nodes[src]:
            return
        # get the ends of the chunk to be moved...
        head = self._get_node(src, 0)
        tail = self._get_node(src, length - 1)
        # store some refs temporarily...
        dst_next = self._nodes[dst].next
        head_previous = head.previous
        tail_next = tail.next
        # insert the chunk...
        self._nodes[dst].next = head
        tail.next = dst_next
        head_previous.next = tail_next

    def append(self, value):
        """Append the value to the tail of the linked list.

        Note that the value will be used as the hash for lookup so this value
        must be hashable.
        """
        node = Node(value)
        # 1. link the node...
        if not self._nodes:
            # first one edge case...node just points to itself...
            node.next = node
            self._origin = node
        else:
            tail = self._origin.previous
            tail.next = node
            node.next = self._origin
        # 2. store hash for fast lookup later...
        self._nodes[node.data] = node

    def to_list(self, location=None, length=None):
        """Convert to a python list starting at the location specified if one is
        provided. Only a sublist may be returned if length is supplied."""
        start_at = self._nodes[location] if location else self._origin
        count = length if length else len(self)
        element = start_at
        result = []
        for _ in range(count):
            result.append(element.data)
            element = element.next
        return result

    def clear(self):
        """Remove all elements"""
        self._nodes = {}
        self._initial = None
        self._last = None

    def _get_node(self, location, offset):
        """Get node given by the location plus offset"""
        node = self._nodes[location]
        if offset == 0:
            return node
        if offset > 0:
            return self._get_node(node.next.data, offset - 1)
        return self._get_node(node.previous.data, offset + 1)
