import sys
# Hard-coded for 5 * 5 board
# Each co-ord can be represented by tup of 2 3-bit numbers
# Bit pattern 0 reserved for a player co-ord of None
# Otherwise, board is just a bitmap, with 1 if a cell is occupied.

# Translate co-ords so that board rotations can be done about the centre
def create_xlate_fns(offset):
    # xlate all board co-ords up and to left
    up_left = lambda x:None if x is None else (x[0]-offset, x[1]-offset)
    # shift the co-ords back
    down_rt = lambda x:None if x is None else (x[0]+offset, x[1]+offset)
    return up_left, down_rt

up_left, down_rt = create_xlate_fns(5//2)

def coord_to_num(coord):
    return coord[0] * 5 + coord[1]

def num_to_coord(num):
    return (num // 5, num % 5)


def format_bitmap(bitmap):
    bit_str = bin(bitmap)[2:].zfill(35)
    return ' '.join((bit_str[:5], bit_str[5:10], bit_str[10:]))

def encode_player(coord):
    if coord is None:
        return 0
    return coord_to_num(coord) + 1

def decode_player(number):
    player = number & 0b11111
    if player == 0:
        return None
    return num_to_coord(player-1)

def coord_to_bitmap(coord):
    return 1 << (24-coord_to_num(coord))

def bitmap_to_coords(bitmap):
    for i in range(24, -1, -1):
        if bitmap & 1:
            yield num_to_coord(i)
        bitmap >>= 1

def coords_to_integer(coords, offset=lambda x:x):
    number = encode_player(offset(coords[0]))
    number = (number << 5) + encode_player(offset(coords[1]))
    number <<= 25
    for coord in coords[2:]:
        number |= coord_to_bitmap(offset(coord))
    return number

def integer_to_coords(number, offset=lambda x:x):
    coords = [offset(b) for b in bitmap_to_coords(number)]
    number >>= 25
    player2 = offset(decode_player(number))
    number >>= 5
    player1 = offset(decode_player(number))

    return [player1, player2] + sorted(coords)


debug = 1
if __name__ == '__main__':

    for r in range(5):
        for c in range(6):
            if c == 5:
                if r != 4: continue
                coord = None
            else:
                coord = (r, c)
            num = encode_player(coord)
            check = decode_player(num)
            match = coord == check
            if debug or not match:
                print(str(num).rjust(8), bin(num)[2:].zfill(5), coord, check, coord==check)
            assert match

    if debug: print()
    for r in range(5):
        for c in range(5):
            coord = (r, c)
            num = coord_to_bitmap(coord)
            check = [b for b in bitmap_to_coords(num)]
            match = len(check)==1 and check[0] == coord
            if debug or not match:
                print(str(num).rjust(8), format_bitmap(num), coord, check[0], coord==check[0])
            assert match

    if debug: print()
    enc_test = [(3, 2), None, (1, 2), (2, 4), (0, 1), (3, 0), (0, 0), (4, 2)]

    enc_test = enc_test[:2] + sorted(enc_test[2:])
    num = coords_to_integer(enc_test)
    check = integer_to_coords(num)
    match = check == enc_test
    if debug or not match:
        print(str(num).rjust(11), format_bitmap(num))
        print(check)
        print(enc_test)
    assert match

    if debug: print()
    all_coords = [None, None, (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                              (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                              ( 0, -2), ( 0, -1), ( 0, 0), ( 0, 1), ( 0, 2),
                              ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
                              ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2)]
    all_ones = (2**25)-1
    check = integer_to_coords(all_ones, up_left)
    match = check == all_coords
    if debug or not match:
        print(str(all_ones).rjust(11), format_bitmap(all_ones))
        print(check)
    assert match

    if debug: print()
    check = coords_to_integer(all_coords, down_rt)
    match = check == all_ones
    if debug or not match:
        print(str(all_ones).rjust(11), format_bitmap(all_ones))
        print(str(check).rjust(11), format_bitmap(check))
    assert match

    if debug: print()
    players = [None, (0, -1)]
    bitmap = ((2*5+1)+1)<<25
    check = integer_to_coords(bitmap, up_left)
    match = check == players
    if debug or not match:
        print(str(bitmap).rjust(11), format_bitmap(bitmap))
        print(check)
    assert match