import sys
from board_encoding import create_encoding_class
from board_rotations import enum_rotations, rotate

KNIGHT_OFFSETS = [
              (-2, -1), (-2,  1),
    (-1, -2),                     (-1,  2),
                     ####
    ( 1, -2),                     ( 1,  2),
              ( 2, -1), ( 2,  1)
]


def board_to_coords(game):
    # Convert representation of AIND Isolation board to ours

    # Add an offset so centre of board always (0, 0)?
    # And then you'd have to add the offset back to your numeric encoding.
    coords = [game.__last_player_move[game.__player_1__],
              game.__last_player_move[game.__player_2__]]

    for r, row in enumerate(self.__board_state__):
        for c, col in enumerate(row):
            if col != BLANK:
                coords.append((r, c))

    return coords


class MyBoard(object):
    def __init__(self, dim=None, board_encoding=None):
        if dim is None:
            return

        assert dim % 2 != 0
        self.dim = dim

        self.enc = create_encoding_class(dim)()

        offset = dim // 2
        # empty = [[(r, c) for c in range(dim)] for r in range(dim)]
        empty = [(r-offset, c-offset) for c in range(dim) for r in range(dim)]
        empty = set(empty)

        self.offset = offset

        if board_encoding is None:
            self.current = [None, None]
        else:
            coords = self.enc.integer_to_coords(board_encoding)
            for i, coord in enumerate(coords):
                assert coord in empty
                if i >= 2:
                    empty.remove(coord)
            self.current = coords

        self.empty = empty

    def __hash__(self):
        return self.enc.coords_to_integer(self.current)

    def normalise(self):
        # Enumerate all the rotations and flips of this board, and return the
        # one which has the lowest encoding integer.
        lowest = None
        for flag, rotated in enum_rotations(self.current):
            encoding = self.enc.coords_to_integer(rotated)
            # print(flag, encoding)
            if lowest is None or encoding < lowest[0]:
                lowest = (encoding, flag, rotated)

        encoding, flag, rotated = lowest
        if not flag:
            return
        self.current = rotated
        self.empty = rotate(self.empty, flag)
        # print('Lowest xform:', bin(flag)[2:].zfill(3))

    def copy(self):
        new_board = MyBoard()
        new_board.dim = self.dim
        new_board.offset = self.offset
        new_board.empty = self.empty.copy()
        new_board.current = self.current[:]
        return new_board

    def valid_moves(self, player):
        assert player in [1, 2]

        pos = self.current[player-1]
        if pos is None:
            return self.empty

        r, c = pos

        valid_moves = [(r+dr,c+dc) for dr, dc in KNIGHT_OFFSETS]
        valid_moves = [v for v in valid_moves if v in self.empty]

        return valid_moves

    def apply_move(self, move, player):
        assert move is not None
        assert player in [1, 2]
        player -= 1

        pos = self.current[player]
        assert move != pos
        assert move != self.current[1-player]
        assert move in self.empty
        self.empty.remove(move)
        self.current[player] = move

        if pos is not None:
            assert pos not in self.empty
            # assert pos not in self.current[2:]
            self.current.append(pos)

    def display(self, p1_char='X', p2_char='O'):
        offset = self.offset
        pad = max(len(str(0 - offset)), len(p1_char), len(p2_char))
        # print('pad:', pad)

        board = []
        col_header = [' '*pad]
        for r in range(self.dim):
            row = r - offset
            line = [str(row).rjust(pad)]
            for c in range(self.dim):
                col = c-offset
                if not r:
                    col_header.append(str(col).rjust(pad))
                char = '.' if (row, col) in self.empty else '#'
                line.append(char.rjust(pad))
            board.append(line)

        for pos, char in zip(self.current[:2], [p1_char, p2_char]):
            if pos is None: continue
            r, c = pos
            board[r+offset][c+offset+1] = char.rjust(pad)

        print(' '.join(col_header))
        for line in board:
            print(' '.join(line))

if __name__ == '__main__':
    board = MyBoard(5)
    board.apply_move((0, 0), 1)
    board.apply_move((-1, 2), 1)
    board.apply_move((-2, 0), 2)
    board.apply_move((0, -1), 2)
    board.display()
    print(hash(board))

    print()
    next = MyBoard(5, 10036973568)
    next.display()
    next.normalise()
    print()
    next.display()
    print(hash(next))