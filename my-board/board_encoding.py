import sys
# Each co-ord can be represented by tup of 2 3-bit numbers
# Bit pattern 0 reserved for a player co-ord of None
# Otherwise, board is just a bitmap, with 1 if a cell is occupied.

no_offset = lambda x:x

def create_encoding_class(dim):
    # Board is a square, with dim x dim cells on the board.
    # Rows down, columns across. (0,0) top left. Max row/col = (dim - 1)
    # The position (row, col) is encoded as (row * dim + col).

    # Co-ord of bottom right would be (dim-1, dim-1).
    # This encodes to an integer pos of (dim-1)*dim + dim -1 = dim ** 2 - 1
    # Whether a cell on the board is free or blocked is encoded as a bit map,
    # with the status of the cell at an integer position 'pos' encoded by the
    # bit at bit position 1 << pos.
    # For a player's current position, however, 0 is used to encode no
    # position - in other words, that the player hasn't yet made a move. So we
    # add 1 to the encoding of the player's actual position to avoid collision
    # with this case. So, if a player occupied the cell at lower right of
    # board, the encoding of this position would be
    # (dim ** 2 - 1) + 1 = dim ** 2

    assert dim % 2 != 0
    offset = dim // 2

    MAX_COORD = (2**dim)-1
    assert dim**2 <= MAX_COORD
    # Which will always be the case, unless dim = 4.257464804
    NUM_CELLS = dim * dim

    BIT_STRING_LEN = dim + dim + NUM_CELLS

    # Translate co-ords so that board rotations can be done about the centre
    # xlate all board co-ords up and to left
    up_left = lambda x:None if x is None else (x[0]-offset, x[1]-offset)
    # shift the co-ords back
    down_rt = lambda x:None if x is None else (x[0]+offset, x[1]+offset)

    class BoardEncoder(object):

        def coord_to_num(self, coord):
            return coord[0] * dim + coord[1]

        def num_to_coord(self, num):
            return (num // dim, num % dim)

        def format_bitmap(self, bitmap):
            bit_str = bin(bitmap)[2:].zfill(BIT_STRING_LEN)
            components = (bit_str[:dim], bit_str[dim:2*dim], bit_str[2*dim:])
            return ' '.join(components)

        def encode_player(self, coord):
            if coord is None:
                return 0
            return self.coord_to_num(coord) + 1

        def decode_player(self, number):
            player = number & MAX_COORD
            if player == 0:
                return None
            return self.num_to_coord(player-1)

        def coord_to_bitmap(self, coord):
            return 1 << (NUM_CELLS-1 - self.coord_to_num(coord))

        def bitmap_to_coords(self, bitmap):
            for i in range(NUM_CELLS-1, -1, -1):
                if bitmap & 1:
                    yield self.num_to_coord(i)
                bitmap >>= 1

        def coords_to_integer(self, coords, offset=down_rt):
            number = self.encode_player(offset(coords[0]))
            number = (number << dim) + self.encode_player(offset(coords[1]))
            number <<= NUM_CELLS
            for coord in coords[2:]:
                number |= self.coord_to_bitmap(offset(coord))
            return number

        def integer_to_coords(self, number, offset=up_left):
            coords = [offset(b) for b in self.bitmap_to_coords(number)]
            number >>= NUM_CELLS
            player2 = offset(self.decode_player(number))
            number >>= dim
            player1 = offset(self.decode_player(number))

            return [player1, player2] + sorted(coords)

    return BoardEncoder