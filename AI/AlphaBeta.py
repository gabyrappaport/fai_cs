import time
from copy import deepcopy

from Heuristic import Heuristic
from Settings import VAMPIRES, WAREWOLVES


class Alphabeta:
    def __init__(self, board, player=VAMPIRES, profondeur_max=20):
        self.board = board
        self.player = player
        self.enemy = VAMPIRES if (player != VAMPIRES) else WAREWOLVES
        self.heuristic_player = Heuristic(board, self.player)
        self.heuristic_enemies = Heuristic(board, self.enemy)
        self.profondeur_max = profondeur_max
        self.start_time = time.time()

    def alphabeta(self):
        board = deepcopy(self.board)

        def maxvalue(board, alpha, beta, hauteur):
            if hauteur >= self.profondeur_max or self.time_elapsed():
                return self.heuristic_player.calculate(board)
            v = -100000
            for action in board.get_possible_actions(self.player):
                boardcopy = deepcopy(board)
                boardcopy.play(action, self.player)
                v = max(v, minvalue(boardcopy, alpha, beta, hauteur + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def minvalue(board, alpha, beta, hauteur):
            if hauteur >= self.profondeur_max:
                return self.heuristic_enemies.calculate(board)
            v = 100000
            for action in board.get_possible_actions(self.enemy):
                boardcopy = deepcopy(board)
                boardcopy.play(action, self.enemy)
                v = min(v, maxvalue(boardcopy, alpha, beta, hauteur + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        meilleur_score = -100000
        beta = 100000
        coup = None
        for action in board.get_possible_actions(self.player):
            boardcopy = deepcopy(board)
            boardcopy.play(action, self.player)
            v = minvalue(boardcopy, meilleur_score, beta, 1)
            # print("\nScore", v)
            # print("Move:", action)
            if v > meilleur_score:
                meilleur_score = v
                coup = action

        return coup

    def time_elapsed(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 1:
            return True
        return False
