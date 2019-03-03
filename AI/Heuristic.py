class Heuristic:

    def __init__(self, board):
        self.board = board

    def heuristic(self):
        heuristic = 0
        return heuristic

    def compute_distance(self):
        pass

    def coef_against_humans(self):
        pass

    def coef_against_ennemis(self):
        pass


class DefensiveHeuristic(Heuristic):

    def __init__(self, board):
        super(Heuristic, self).__init__(board)


class AttackingOpponentsHeuristic(Heuristic):

    def __init__(self, board):
        super(Heuristic, self).__init__(board)


class AttackingHumansHeuristic(Heuristic):

    def __init__(self, board):
        super(Heuristic, self).__init__(board)
