import time
from copy import deepcopy

from AI.Heuristic import Heuristic


class Alphabeta:
    def __init__(self, board, profondeur_max=4):
        self.board = board
        self.heuristic_us = Heuristic(board)
        self.heuristic_enemies = Heuristic(board)
        self.profondeur_max = profondeur_max
        self.start_time = time.time()

    def alphabeta(self):
        board = deepcopy(self.board)

        def maxvalue(board, alpha, beta, hauteur):
            if hauteur >= self.profondeurmax or self.time_elapsed():
                return self.heuristic_us.heuristic(board)
            v = -100000
            for action in board.getPossibleColumns():
                boardcopy = deepcopy(board)
                boardcopy.play(self.color, action)
                v = max(v, minvalue(boardcopy, alpha, beta, hauteur + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def minvalue(board, alpha, beta, hauteur):
            if hauteur >= self.profondeurmax:
                return self.heuristic_enemies.heuristic(board)
            v = 100000
            for action in board.getPossibleColumns():
                boardcopy = deepcopy(board)
                boardcopy.play(-self.color, action)
                v = min(v, maxvalue(boardcopy, alpha, beta, hauteur + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        meilleur_score = -100000
        beta = 100000
        coup = None
        for action in board.getPossibleColumns():
            boardcopy = deepcopy(board)
            boardcopy.play(self.color, action)
            v = minvalue(boardcopy, meilleur_score, beta, 1)
            if v > meilleur_score:
                meilleur_score = v
                coup = action

        return coup

    def time_elapsed(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 1:
            return True
        return False
