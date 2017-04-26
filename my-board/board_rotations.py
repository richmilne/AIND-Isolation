import sys

r"""
General Rotation matrix, for     [cos θ  -sin θ]
θ° rotation anti-clockwise       [sin θ   cos θ]

For rotations which are multiples of 90°, the sin/cos terms end up being 0 or
±1. Here they're plotted, along with the rotation matrix:

    (-y,x)
 3 .  o  .  |  .  .  .             [ 0 -1][x] = [-y]      [ 1  0][x] = [ x]
 2 .  .  .  |  .  .  O (X,Y)       [ 1  0][y]   [ x]      [ 0  1][y]   [ y]
 1 .  .  .  |  .  .  .                Rotate 90°             Original point
 0-+--+--+--+--+--+--+-
-1 .  .  .  |  .  .  .             [-1  0][x] = [-x]      [ 0  1][x] = [ y]
-2 o (-x,-y)|  .  .  .             [ 0 -1][y]   [-y]      [-1  0][y]   [-x]
-3 .  .  .  |  .  o (y,-x)            Rotate 180°            Rotate 270°
  -3 -2 -1  0  1  2  3

We can also get a series of flips about the x and y axes:

 3 .  .  .  |  .  .  .             [-1  0][x] = [-x]
 2 o (-x,y) |  .  .  O (X,Y)       [ 0  1][y]   [ y]
 1 .  .  .  |  .  .  .             Flip about y-axis
 0-+--+--+--+--+--+--+-
-1 .  .  .  |  .  .  .             [-1  0][x] = [-x]      [ 1  0][x] = [ x]
-2 o (-x,-y)|  .  .  o (x,-y)      [ 0 -1][y]   [-y]      [ 0 -1][y]   [-y]
-3 .  .  .  |  .  .  .             Flip about x and       Flip about x-axis
  -3 -2 -1  0  1  2  3             y - same as rotate
                                   rotate 180°

And flips about the lines y = ±x

 3 .  .  .  |  .  o (y,x)          [ 0  1][x] = [ y]
 2 .  .  .  |  .  .  O (X,Y)       [ 1  0][y]   [ x]
 1 .  .  .  |  .  .  .             Flip about y=x
 0-+--+--+--+--+--+--+-
-1 .  .  .  |  .  .  .             [ 0 -1][x] = [-y]
-2 .  .  .  |  .  .  .             [-1  0][y]   [-x]
-3 .  o (-y,-x).  .  .             Flip about y=-x
  -3 -2 -1  0  1  2  3

All in all, we have the following transformed co-ordinates

0: ( x,  y)  Original              4: ( y,  x)  Flip about y=x
1: ( x, -y)  Flip about x-axis     5: (-y,  x)  Rotate 90°
2: (-x,  y)  Flip about y-axis     6: ( y, -x)  Rotate 270°
3: (-x, -y)  Rotate 180°           7: (-y, -x)  Flip about y=-x

So you can see there are 8 options above. To effect a transformation, we either
swap or leave the two points, and negate either, neither or both. These actions
can be represented by bit positions in a 3-bit number.
"""

def rotate(coords, flag, reverse=False):
    # Reverse for when you want to reverse, or undo, the effect of a previous
    # transformation

    if not flag:
        return coords

    swap =  (flag & 0b100) >> 2
    neg_x = (flag & 0b010) >> 1
    neg_y = (flag & 0b001)
    if reverse and swap:
        neg_x, neg_y = neg_y, neg_x
    # print('flags:', bin(flag)[2:].zfill(3), swap, neg_x, neg_y, reverse)
    signs = (1-2*neg_x, 1-2*neg_y)

    rotated = []
    for coord in coords:
        if coord is None:
            rotated.append(None)
        else:
            x, y = [s * c for s, c in zip(signs, coord)]
            new = (y, x) if swap else (x, y)
            rotated.append(new)
    return rotated


def enum_rotations(coords):
    all_rotations = [(0, coords)]
    for flag in range(1, 8):
        all_rotations.append((flag, rotate(coords, flag)))
    return all_rotations


if __name__ == '__main__':
    point = (3, 2)
    tests = {
        0: ( 3,  2),
        1: ( 3, -2),
        2: (-3,  2),
        3: (-3, -2),
        4: ( 2,  3),
        5: (-2,  3),
        6: ( 2, -3),
        7: (-2, -3)
    }
    for trans, check in tests.items():
        ans = rotate([point], trans, False)
        # print(trans, check, ans)
        assert ans[0] == check
        assert point == rotate(ans, trans, True)[0]

    test = [(3, 2), None, (-1, 2), (5, -4), (0, 1), (3, 0), (0, 0), (-2, -6)]
    print(test)
    for flag in range(8):
        print()
        print(flag, bin(flag)[2:].zfill(3))
        rot = rotate(test, flag)
        print(rot)
        check = rotate(rot, flag, True)
        print(check)
        assert(check==test)

    for flag, rotated in enum_rotations(test):
        print(bin(flag)[2:].zfill(3), rotated)