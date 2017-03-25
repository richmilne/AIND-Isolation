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

( x,  y)  Original                 ( y,  x)  Flip about y=x
( x, -y)  Flip about x-axis        ( y, -x)  Rotate 270°
(-x,  y)  Flip about y-axis        (-y,  x)  Rotate 90°
(-x, -y)  Rotate 180°              (-y, -x)  Flip about y=-x

So you can see there are 8 options above. To effect a transformation, we either
swap or leave the two points, and negate either, neither or both. These actions
can be represented by bit positions in a 3-bit number.
"""

def board_to_coords(game):

    # Add an offset so centre of board always (0, 0)?
    # And then you'd have to add the offset back to your numeric encoding.

    coords = [game.__last_player_move[game.__player_1__],
              game.__last_player_move[game.__player_2__]]

    for r, row in enumerate(self.__board_state__):
        for c, col in enumerate(row):
            if col != BLANK:
                coords.append((r, c))

    return coords

def rotate(co_ords, flag, reverse=False):

    if not flag:
        return co_ords

    swap =  (flag & 0b100) >> 2
    neg_x = (flag & 0b010) >> 1
    neg_y = (flag & 0b001)
    if reverse and swap:
        neg_x, neg_y = neg_y, neg_x

    rotated = []
    for co_ord in co_ords:
        if co_ord is None:
            rotated.append(None)
        else:
            x, y = co_ord
            new = ((1 - 2*neg_x) * (y if swap else x),
                   (1 - 2*neg_y) * (x if swap else y))
            rotated.append(new)
    return rotated

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


def enum_rotations(co_ords):
    all_rotations = [co_ords]
    for flag in range(8):
        all_rotations.append(rotate(co_ords, flag))


        swap =  (i & 0b100) >> 2
        neg_x = (i & 0b010) >> 1
        neg_y = (i & 0b001)
        print(swap, neg_x, neg_y)
        new = [(1-2*neg_x)*(y if swap else x),
               (1-2*neg_y)*(x if swap else y), i]
        rotations.append(new)
    for r in rotations:
        print(r)

# enum_rotations(test)



