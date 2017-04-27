"""This file contains a collection of my Isolation scoring heuristics, for
comparison with the heuristic functions given in the sample project files.
"""

def weighted_moves_score(game, player):
    # See https://github.com/on2valhalla/Isola
    # (myMoves - 3*opMoves) * filledSpaces
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = len(game.get_blank_spaces())
    filled_spaces = (game.width * game.height) - blank_spaces

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float((own_moves - 3*opp_moves)*filled_spaces)


knight_offsets = [
              (-2, -1), (-2,  1),
    (-1, -2),                     (-1,  2),
    ( 1, -2),                     ( 1,  2),
              ( 2, -1), ( 2,  1)
]

adjacent_offsets = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]

def get_moves(game, move, directions):
    r, c = move
    valid_moves = [(r+dr,c+dc) for dr, dc in directions]
    valid_moves = filter(game.move_is_legal, valid_moves)
    return valid_moves


def find_connected(game, player, direction):
    # Return a list of all the cells 'connected' to the player's current move.
    # The definition of connected depends on the way the player is allowed to
    # move from the current position, which is defined by 'directions' - a list
    # of offsets from the player's current position.
    examined = set([])
    queue = set([game.get_player_location(player)])
    while queue:
        move = queue.pop()
        queue |= (set(get_moves(game, move, direction)) - examined)
        examined.add(move)
    return examined


def reachable(game, player):
    return find_connected(game, player, knight_offsets)


def adjacent(game, player):
    return find_connected(game, player, adjacent_offsets)


def reachable_score(game, player):
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    own_reachable = reachable(game, player)
    opp_reachable = reachable(game, game.get_opponent(player))
    return float(len(own_reachable) - len(opp_reachable))


def cut_off_reach_score(game, player):
    # Not just how many squares are potentially reachable from your position -
    # but also whether you and your opponent are likely to overlap. It is
    # possible to place players so their moves will never overlap. Also, if one
    # player has cut the other off, their positions will never overlap, and
    # neither player can block the other further.
    #
    # .x.xo.o.
    # x..ox..o
    # ..X..O..       Capital X, O: initial positions
    # x..ox..o       Lowercase letters: potential moves
    # .x.xo.o.
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    own_reachable = reachable(game, player)
    opp_reachable = reachable(game, game.get_opponent(player))
    common = own_reachable & opp_reachable

    own_score = own_reachable - common
    opp_score = opp_reachable - common
    score = len(own_score) - len(opp_score)
    cut_off_bonus = bool(not len(common)) * (game.width*game.height)
    cut_off_bonus *= (-1 if score < 0 else 1)

    return float(score + cut_off_bonus)