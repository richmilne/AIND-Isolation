"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import itertools
import random

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError
from sample_players import improved_score as custom_score


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

        self.fn = self.minimax if method == 'minimax' else self.alphabeta

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        if not legal_moves:
            return (-1, -1)

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        best = (-1, -1)
        if self.iterative:
            depths = itertools.count(1)
        else:
            depths = (self.search_depth,)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            for depth in depths:
                _, best = self.fn(game, depth, maximizing_player=True)
                if self.time_left() < 13 * self.TIMER_THRESHOLD:
                    break

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best

    def cut_off_test(self, game, depth):
        utility = game.utility(self)
        if bool(utility):
            return (True, utility, (-1, -1))
        if not depth:
            return (True, self.score(game, self), (-1, -1))
        return (False, None, (-1, -1))

    def _minimax_alphabeta(self, game, depth, maximise, alphabeta,
                           alpha=None, beta=None):

        cut_off, score, move = self.cut_off_test(game, depth)
        if cut_off: return score, move

        best = None
        deeper = depth-1
        max_or_min = not maximise
        v = float('-inf') if maximise else float('inf')

        for move in game.get_legal_moves():
            args = (game.forecast_move(move), deeper, max_or_min, alphabeta)
            if alphabeta:
                args += (alpha, beta)
            score, _ = self._minimax_alphabeta(*args)

            cmp = score > v if maximise else score < v
            if cmp:
                v, best = score, move

            if alphabeta:
                cmp = v >= beta if maximise else v <= alpha
                if cmp: break
                alpha, beta = ((max(alpha, v), beta) if maximise else
                               (alpha,  min(beta, v)))
            # if self.time_left() < self.TIMER_THRESHOLD: break
        return v, best

    def __max_value(self, game, depth):

        cut_off, score, move = self.cut_off_test(game, depth)
        if cut_off: return score, move

        v = float('-inf')
        best = None
        for move in game.get_legal_moves():
            score, _ = self.__min_value(game.forecast_move(move), depth-1)
            if score > v:
                v, best = score, move
        return v, best

    def __min_value(self, game, depth):

        cut_off, score, move = self.cut_off_test(game, depth)
        if cut_off: return score, move

        v = float('inf')
        best = None
        for move in game.get_legal_moves():
            score, _ = self.__max_value(game.forecast_move(move), depth-1)
            if score < v:
                v, best = score, move
        return v, best

    def __alphabeta_max_value(self, game, alpha, beta, depth):

        cut_off, score, move = self.cut_off_test(game, depth)
        if cut_off: return score, move

        v = float('-inf')
        best = None
        for move in game.get_legal_moves(self):
            args = (game.forecast_move(move), alpha, beta, depth-1)
            score, _ = self.__alphabeta_min_value(*args)
            if score > v:
                v, best = score, move
            if v >= beta:
                break
            alpha = max(alpha, v)
        return v, best

    def __alphabeta_min_value(self, game, alpha, beta, depth):

        cut_off, score, move = self.cut_off_test(game, depth)
        if cut_off: return score, move

        v = float('inf')
        best = None
        for move in game.get_legal_moves():
            args = (game.forecast_move(move), alpha, beta, depth-1)
            score, _ = self.__alphabeta_max_value(*args)
            if score < v:
                v, best = score, move
            if v <= alpha:
                break
            beta = min(beta, v)
        return v, best

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        return self._minimax_alphabeta(game, depth, maximizing_player,
                                       alphabeta=False)

        fn = self.__max_value if maximizing_player else self.__min_value
        return fn(game, depth)


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        return self._minimax_alphabeta(game, depth, maximizing_player, True,
                                       float('-inf'), float('inf'))

        fn = (self.__alphabeta_max_value if maximizing_player else 
              self.__alphabeta_min_value)
        return fn(game, float('-inf'), float('inf'), depth)