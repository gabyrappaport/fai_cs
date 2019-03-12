import math
import sys


def inverse(x):
    return 1/x if x!=0 else 100

def linear(x):
    return x


class Heuristic:

    def __init__(self, board, distance_lambda=inverse, enemy_lambda=linear,
                 distance_threshold=None):

        self.coef_humans = 100
        self.coef_enemy = 10
        self.coef_presence = 10
        self.distance_threshold = max(board.rows, board.columns) // 2 if not distance_threshold else distance_threshold
        self.distance_lambda = distance_lambda
        self.enemy_lambda = enemy_lambda

    def calculate(self, board):
        player_location = board.player.dict
        enemy_location = board.enemy.dict
        human_location = board.humans
        #print("Compute heuristique")
        #board.print_pretty()
        if board.player.get_count() == 0:
            return -sys.maxsize
        if board.enemy.get_count() == 0:
            return sys.maxsize
        result = self.coef_presence * (board.player.get_count() - board.enemy.get_count())
        #print("initial result", result)
        for player_pos, player_num in player_location.items():
            scores = []
            for enemy_pos, enemy_num in enemy_location.items():
                d = self.euclidian(player_pos, enemy_pos)
                #if d <= self.distance_threshold:
                scores += [self.heuristic_enemy(player_pos, enemy_pos, player_num, enemy_num, board)]
                #print('scores enemy', scores)
            for human_pos, human_num in human_location.items():
                d = self.euclidian(player_pos, human_pos)
                #if d <= self.distance_threshold:
                scores += [self.heuristic_human(player_pos, human_pos, player_num, human_num)]
                #print("scores", scores)
            if len(scores) > 0:
                result += self.max_abs(scores)
        #print("heuristic", result)
        return result

    def max_abs(self, scores):
        max = 0
        for i in range(len(scores)):
            if abs(scores[i]) > abs(max):
                max = scores[i]
        return max

    def heuristic_enemy(self, player_pos, enemy_pos, player_num, enemy_num, board):
        player_left = self.player_left_against_enemy(player_num, enemy_num)
        return self.coef_enemy * self.distance(player_pos, enemy_pos) * player_left

    def heuristic_human(self, start, end, player_num, human_num):
        #print("Heuristic humans")
        #print("start", start)
        #print("end", end)
        #print('distance', self.euclidian(start, end), "used distance", self.distance(start, end))
        #print("player left", self.player_left_against_human(player_num, human_num))
        return self.coef_humans * self.distance(start, end) * self.player_left_against_human(player_num, human_num)

    def euclidian(self, start, end):
        (start_x, start_y) = start
        (end_x, end_y) = end
        return math.floor(math.sqrt(((start_x - end_x) ** 2) + ((start_y - end_y) ** 2)))

    # approximation of distance with diagonals
    def distance(self, start, end):
        return self.distance_lambda(self.euclidian(start, end))

    def player_left_against_enemy(self, player_num, enemy_num):
        if player_num > 1.5 * enemy_num:
            return self.enemy_lambda(player_num)
        if player_num * 1.5 < enemy_num:
            return -self.enemy_lambda(player_num)
        p = 0.5
        if player_num > enemy_num:
            p = player_num / enemy_num - 0.5
        if player_num < enemy_num:
            p = 0.5 * player_num / enemy_num
        return self.enemy_lambda(player_num*p*p - enemy_num*(1-p)*(1-p))

    def player_left_against_human(self, player_num, human_num):
        if player_num > human_num:
            return self.enemy_lambda(player_num+human_num)
        if player_num < human_num:
            return -self.enemy_lambda(player_num)
        p = 0.5
        if player_num > human_num:
            p = player_num / human_num - 0.5
        if player_num < human_num:
            p = 0.5 * player_num / human_num
        return self.enemy_lambda((player_num+human_num)*p*p)
