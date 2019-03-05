import sys
import time
from copy import deepcopy

from Heuristic import Heuristic
from Settings import VAMPIRES, WAREWOLVES


class Alphabeta:
    def __init__(self, board, player=VAMPIRES, profondeur_max=4):
        self.board = board
        self.player = player
        self.enemy = VAMPIRES if (player != VAMPIRES) else WAREWOLVES
        self.heuristic_player = Heuristic(board)
        self.heuristic_enemies = Heuristic(board)
        self.profondeur_max = profondeur_max

    def alphabeta(self):
        self.start_time = time.time()
        board = deepcopy(self.board)
        board.is_playing(self.player)

        def maxvalue(board, alpha, beta, hauteur):
            board.is_playing(self.player)
            if hauteur >= self.profondeur_max or self.time_elapsed():
               return self.heuristic_enemies.calculate(board)
            v = -sys.maxsize
            for action in board.get_possible_actions_dep():
                if action != []:
                    boardcopy = deepcopy(board)
                    boardcopy.play(action)
                    v = max(v, minvalue(boardcopy, alpha, beta, hauteur + 1))
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

        def minvalue(board, alpha, beta, hauteur):
            board.is_playing(self.enemy)
            if hauteur >= self.profondeur_max:
                return self.heuristic_player.calculate(board)
            v = sys.maxsize
            for action in board.get_possible_actions_dep():
                if action != []:
                    boardcopy = deepcopy(board)
                    boardcopy.play(action)
                    v = min(v, maxvalue(boardcopy, alpha, beta, hauteur + 1))
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v

        meilleur_score = -sys.maxsize
        beta = sys.maxsize
        coup = []
        for action in board.get_possible_actions_dep():
            boardcopy = deepcopy(board)
            boardcopy.play(action)
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
