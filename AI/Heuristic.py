import math

from Settings import VAMPIRES, WAREWOLVES


def linear(x):
    return x


class Heuristic:

    def __init__(self, board, player_type=VAMPIRES, distance_lambda=linear, enemy_lambda=linear,
                 distance_threshold=None):
        self.player_type = player_type
        self.coef_humans = 10
        self.coef_enemy = 10
        self.distance_threshold = max(board.rows, board.columns) // 2 if not distance_threshold else distance_threshold
        self.distance_lambda = distance_lambda
        self.enemy_lambda = enemy_lambda

    def calculate(self, board):
        result = 0
        player_locations = board.vampires
        enemy_locations = board.warewolves
        human_locations = board.humans
        if self.player_type == WAREWOLVES:
            player_locations = board.warewolves
            enemy_locations = board.vampires
        for player_pos, player_num in player_locations.items():
            for enemy_pos, enemy_num in enemy_locations.items():
                if self.euclidian(player_pos, enemy_pos) < self.distance_threshold:
                    result += self.heuristic_enemy(player_pos, enemy_pos, player_num, enemy_num)
            for human_pos, human_num in human_locations.items():
                if self.euclidian(player_pos, human_pos) < self.distance_threshold:
                    result += self.heuristic_human(player_pos, human_pos, player_num, human_num)
        return result

    def heuristic_enemy(self, start, end, player_num, enemy_num):
        return self.coef_enemy * self.distance(start, end) * self.player_left(player_num, enemy_num, rapport_de_force_coef=1.5)

    def heuristic_human(self, start, end, player_num, enemy_num):
        return self.coef_enemy * self.distance(start, end) * self.player_left(player_num, enemy_num)

    def euclidian(self, start, end):
        (start_x, start_y) = start
        (end_x, end_y) = end
        return math.floor(math.sqrt(((start_x - end_x) ** 2) + ((start_y - end_y) ** 2)))

    # approximation of distance with diagonals
    def distance(self, start, end):
        return self.distance_lambda(self.euclidian(start, end))

    def player_left(self, player_num, enemy_num, rapport_de_force_coef=1):
        if player_num > rapport_de_force_coef * enemy_num:
            return self.enemy_lambda(player_num)
        if player_num * rapport_de_force_coef < enemy_num:
            return self.enemy_lambda(-player_num)
        p = 0.5
        if player_num > enemy_num:
            p = player_num / enemy_num - 0.5
        if player_num < enemy_num:
            p = 0.5 * player_num / enemy_num
        return self.enemy_lambda(self.player_left_after_random_battle(p) * player_num)

    def player_left_after_random_battle(self, p):
        return p * (2 * p - 1) - (1 - p)


class DefensiveHeuristic(Heuristic):

    def __init__(self, board):
        super(Heuristic, self).__init__(board)


class AttackingOpponentsHeuristic(Heuristic):

    def __init__(self, board):
        super(Heuristic, self).__init__(board)


class AttackingHumansHeuristic(Heuristic):

    def __init__(self, board):
        super(Heuristic, self).__init__(board)
