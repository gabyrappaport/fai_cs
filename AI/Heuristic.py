import math


def inverse(x):
    return 1/x if x!=0 else 100

def linear(x):
    return x


class Heuristic:

    def __init__(self, board, distance_lambda=inverse, enemy_lambda=linear,
                 distance_threshold=None):

        self.coef_humans = 100
        self.coef_enemy = 10
        self.distance_threshold = max(board.rows, board.columns) // 2 if not distance_threshold else distance_threshold
        self.distance_lambda = distance_lambda
        self.enemy_lambda = enemy_lambda

    def calculate(self, board):
        #print("compute heuristic")
        #print(board.player.type)
        #board.print_pretty()
        player_location = board.player.dict
        enemy_location = board.enemy.dict
        human_location = board.humans
        result = 0
        for player_pos, player_num in player_location.items():
            scores = []
            for enemy_pos, enemy_num in enemy_location.items():
                d = self.euclidian(player_pos, enemy_pos)
                #if d <= self.distance_threshold:
                #print("distance enemy", d)
                scores += [self.heuristic_enemy(player_pos, enemy_pos, player_num, enemy_num, board)]
            #print("scores enemy", scores)
            for human_pos, human_num in human_location.items():
                d = self.euclidian(player_pos, human_pos)
                #if d <= self.distance_threshold:
                #print("distance human", d)
                scores += [self.heuristic_human(player_pos, human_pos, player_num, human_num)]
            #print("scores total", scores)
            if len(scores) > 0:
                result += self.max_abs(scores)
        ##print("result", result)
        return result

    def max_abs(self, scores):
        max = 0
        for i in range(len(scores)):
            if abs(scores[i]) > abs(max):
                max = scores[i]
        return max

    def heuristic_enemy(self, player_pos, enemy_pos, player_num, enemy_num, board):
        #if enemy_pos in board.humans:
        #    enemy_num = self.player_left_against_human(enemy_num, board.humans[enemy_pos])
        #if player_pos in board.humans:
        #    player_num = self.player_left_against_human(player_num, board.humans[player_pos])
        player_left = self.player_left_against_enemy(player_num, enemy_num)
        ##print("player left", player_left)
        return self.coef_enemy * self.distance(player_pos, enemy_pos) * player_left

    def heuristic_human(self, start, end, player_num, human_num):
        #print("player left against human", self.player_left_against_human(player_num, human_num))
        #print("distance human", self.distance(start, end), "start", start, "end", end)
        #print('coef', self.coef_humans)
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

class HeuristicAllEnvironnement(Heuristic):

    def __init__(self, board):
        super().__init__(board)

    def calculate(self, board):
        player_location = board.player.dict
        enemy_location = board.enemy.dict
        human_location = board.humans
        # if board in self.score_mem: return self.score_mem[board]
        result = board.player.get_count()*100
        # Au lieu de tout sommer on peut prendre le score max par point
        for player_pos, player_num in player_location.items():
            scores = 0
            for enemy_pos, enemy_num in enemy_location.items():
                d = self.euclidian(player_pos, enemy_pos)
                if d <= self.distance_threshold:
                    scores += self.heuristic_enemy(player_pos, enemy_pos, player_num, enemy_num)
            for human_pos, human_num in human_location.items():
                d = self.euclidian(player_pos, human_pos)
                if d <= self.distance_threshold:
                    scores += self.heuristic_human(player_pos, human_pos, player_num, human_num)
        # #print("Got result", result, len(player_location.items()), len(enemy_location.items()))
        return result


class AttackingHumansHeuristic(Heuristic):

    def __init__(self, board):
        super(Heuristic, self).__init__(board)
