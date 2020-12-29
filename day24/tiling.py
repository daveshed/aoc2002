"""
Represent the hexagonal grid with a basic offset layout ie. a tile has two
indices to represent the row and column as per...
https://gamedevelopment.tutsplus.com/tutorials/creating-hexagonal-minesweeper--cms-28655
"""
def read_input(filename: str):
    """Read the file and return a list of the lines"""
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

class Vector:
    """A hexagonal tile vector expressed in basic offset layout"""
    def __init__(self, row, col):
        self._row = row
        self._col = col

    def __add__(self, other):
        return Vector((self.row + other.row), (self.col + other.col))

    def __eq__(self, other):
        return (self.row == other.row) and (self.col == other.col)

    def __hash__(self):
        return hash((self.row, self.col,))

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def __repr__(self):
        return f"Vector({self.row}, {self.col}) " + super().__repr__()

    @classmethod
    def from_directions(cls, directions):
        """Get the target tile vector from the directions string"""
        # start at the reference tile
        return cls._consume(cls(0, 0), directions)

    @classmethod
    def _consume(cls, vector, directions):
        if not directions:
            # no more directions to consume
            return vector
        if directions.startswith('e'):
            vector += Vector(0, 1)
            return cls._consume(vector, directions[1:])
        if directions.startswith('se'):
            vector += Vector(1, 1)
            return cls._consume(vector, directions[2:])
        if directions.startswith('sw'):
            vector += Vector(1, 0)
            return cls._consume(vector, directions[2:])
        if directions.startswith('w'):
            vector += Vector(0, -1)
            return cls._consume(vector, directions[1:])
        if directions.startswith('nw'):
            vector += Vector(-1, -1)
            return cls._consume(vector, directions[2:])
        if directions.startswith('ne'):
            vector += Vector(-1, 0)
            return cls._consume(vector, directions[2:])
        raise AssertionError(f"wtf is '{directions}'?!")


class HexagonalTile:
    _UNIT_VECTORS = [
        Vector(0, 1),
        Vector(1, 1),
        Vector(1, 0),
        Vector(0, -1),
        Vector(-1, -1),
        Vector(-1, 0),
    ]

    def __init__(self, location, floor):
        self._location = location
        self._floor = floor

    def __eq__(self, other):
        return self.location == other.location

    def update(self):
        """Apply policies based on neighbours and determine if this tile should
        be flipped. If so, just mark it to be flipped when the floor is updated.
        Note that all tiles are flipped at the same time after the policies have
        been applied."""
        raise NotImplementedError

    def flip(self):
        raise NotImplementedError

    @property
    def is_black(self):
        raise NotImplementedError

    @property
    def location(self):
        return self._location

    @property
    def neighbours(self):
        for location in self.adjacent_locations:
            try:
                yield self._floor.tiles[location]
            except KeyError:
                pass

    @property
    def black_neighbours(self): # this is a horrible name!
        return len(list(filter(lambda x: x.is_black, self.neighbours)))

    @property
    def adjacent_locations(self):
        return ((self.location + vector) for vector in self._UNIT_VECTORS)


class BlackTile(HexagonalTile):

    @property
    def is_black(self):
        return True

    def update(self):
        if self.black_neighbours == 0 or self.black_neighbours > 2:
            self._floor.to_flip.append(self)

    def flip(self):
        assert self.location in self._floor.tiles, \
            f"black tile should already exist in the map at {self.location}"
        self._floor.tiles[self.location] = WhiteTile(self.location, self._floor)
        del self


class WhiteTile(HexagonalTile):

    @property
    def is_black(self):
        return False

    def update(self):
        if self.black_neighbours == 2:
            self._floor.to_flip.append(self)

    def flip(self):
        # 1. put a black tile in the space...
        tile = BlackTile(self.location, self._floor)
        self._floor.tiles[self.location] = tile
        # 2. any adjacent tiles that are not already in the map must also be
        #    created...
        for location in tile.adjacent_locations:
            if location in self._floor.tiles:
                # don't overwrite anything that's already there...
                continue
            self._floor.tiles[location] = WhiteTile(location, self._floor)
        del self


class Floor:
    """A container that holds a lookup table of all the tiles."""
    def __init__(self):
        # map of all tiles by location...
        self._tiles = {}
        # tiles that are due to be flipped...
        self._to_flip = []

    @property
    def tiles(self):
        return self._tiles

    @property
    def to_flip(self):
        return self._to_flip

    def flip_tile(self, location):
        """Used at startup only when creating the floor the first time from
        instructions. After this, tiles will be updated and change following
        their own local rules."""
        try:
            self.tiles[location].flip()
        except KeyError:
            self.tiles[location] = WhiteTile(location, self)
            self.tiles[location].flip()

    def count_black(self):
        return len(list(filter(lambda x: x.is_black, self.tiles.values())))

    def update(self):
        """Flip the tiles for today"""
        # 1. update all tiles and see if they need to be flipped based on local
        #    policies...
        for tile in self.tiles.values():
            tile.update()
        # 2. flip those that have been marked...
        for tile in self.to_flip:
            tile.flip()
        self.to_flip.clear()

    @classmethod
    def from_instructions(cls, instructions):
        """Factory method to create from a list of directions"""
        floor = cls()
        for directions in instructions:
            floor.flip_tile(Vector.from_directions(directions))
        return floor


if __name__ == "__main__":
    floor = Floor.from_instructions(read_input("puzzle-input.txt"))
    print(f"PART1...{floor.count_black()}")
    for i in range(1, 101):
        floor.update()
        print(f"Day {i:3d}: {floor.count_black():4d}")
