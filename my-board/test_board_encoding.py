import sys
from board_encoding import create_encoding_class, no_offset

debug = 1
if __name__ == '__main__':

    dim = 5
    enc = create_encoding_class(5)()

    for r in range(5):
        for c in range(6):
            if c == 5:
                if r != 4: continue
                coord = None
            else:
                coord = (r, c)
            num = enc.encode_player(coord)
            check = enc.decode_player(num)
            match = coord == check
            if debug or not match:
                print(str(num).rjust(8), bin(num)[2:].zfill(5), coord, check, coord==check)
            assert match

    if debug: print()
    for r in range(5):
        for c in range(5):
            coord = (r, c)
            num = enc.coord_to_bitmap(coord)
            check = [b for b in enc.bitmap_to_coords(num)]
            match = len(check)==1 and check[0] == coord
            if debug or not match:
                print(str(num).rjust(8), enc.format_bitmap(num), coord, check[0], coord==check[0])
            assert match

    if debug: print()
    enc_test = [(3, 2), None, (1, 2), (2, 4), (0, 1), (3, 0), (0, 0), (4, 2)]

    enc_test = enc_test[:2] + sorted(enc_test[2:])
    num = enc.coords_to_integer(enc_test, no_offset)
    check = enc.integer_to_coords(num, no_offset)
    match = check == enc_test
    if debug or not match:
        print(str(num).rjust(11), enc.format_bitmap(num))
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
    check = enc.integer_to_coords(all_ones) # Using default up_left offset
    match = check == all_coords
    if debug or not match:
        print(str(all_ones).rjust(11), enc.format_bitmap(all_ones))
        print(check)
    assert match

    if debug: print()
    check = enc.coords_to_integer(all_coords) # Using default down_rt offset
    match = check == all_ones
    if debug or not match:
        print(str(all_ones).rjust(11), enc.format_bitmap(all_ones))
        print(str(check).rjust(11), enc.format_bitmap(check))
    assert match

    if debug: print()
    players = [None, (0, -1)]
    bitmap = ((2*5+1)+1)<<25
    check = enc.integer_to_coords(bitmap)#, up_left)
    match = check == players
    if debug or not match:
        print(str(bitmap).rjust(11), enc.format_bitmap(bitmap))
        print(check)
    assert match