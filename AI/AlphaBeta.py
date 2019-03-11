import sys
import time
from copy import deepcopy

from Heuristic import Heuristic, HeuristicAllEnvironnement
from Settings import VAMPIRES, WAREWOLVES


class Alphabeta:
    def __init__(self, board, player=VAMPIRES, profondeur_max=4, heuristic_player=Heuristic): # todo: prof pas > a la dim
        self.board = board
        self.player = player
        self.enemy = VAMPIRES if (player != VAMPIRES) else WAREWOLVES
        self.heuristic_player = heuristic_player(board)
        self.profondeur_max = profondeur_max

    def alphabeta(self):
        self.start_time = time.time()
        board = deepcopy(self.board)
        board.is_playing(self.player)

        def maxvalue(board, alpha, beta, hauteur):
            board.is_playing(self.player)
            if hauteur >= self.profondeur_max or self.time_elapsed():
                board.is_playing(self.player)
                return self.heuristic_player.calculate(board)
            v = -sys.maxsize
            for action in board.get_possible_actions():
                if action != []:
                    boardcopy = deepcopy(board)
                    boardcopy.play_test(action)
                    v = max(v, minvalue(boardcopy, alpha, beta, hauteur + 1))
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

        def minvalue(board, alpha, beta, hauteur):
            board.is_playing(self.enemy)
            if hauteur >= self.profondeur_max:
                board.is_playing(self.player)
                return self.heuristic_player.calculate(board)
            v = sys.maxsize
            for action in board.get_possible_actions():
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
        for action in board.get_possible_actions():
            boardcopy = deepcopy(board)
            boardcopy.play(action)
            v = minvalue(boardcopy, meilleur_score, beta, 1)
            print("Score", action, v)
            if v > meilleur_score:
                meilleur_score = v
                coup = action
        return coup

    def time_elapsed(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 1:
            return True
        return False
