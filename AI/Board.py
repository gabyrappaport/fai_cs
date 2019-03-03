import itertools
import numpy as np
from Settings import WAREWOLVES


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.vampires = {}  # key = (x,y) ; value = number of vampires
        self.warewolves = {}
        self.humans = {}
        self.reinit_numb()

    def reinit_numb(self):
        self.nbr_vampires = 0
        self.nbr_warewolves = 0
        self.nbr_humans = 0

    def update_board(self, game_map):
        self.reinit_numb()
        for (x, y, humans, vampires, warewolves) in game_map:
            if humans > 0:
                self.humans[(x, y)] = humans
                self.nbr_humans += humans
            if vampires > 0:
                self.vampires[(x, y)] = vampires
                self.nbr_vampires += vampires
            if warewolves > 0:
                self.warewolves[(x, y)] = warewolves
                self.nbr_warewolves += warewolves

    def play(self, action, player_type):
        for move in action:
            (start_x, start_y), (end_x, end_y), num = move
            if player_type == WAREWOLVES:
                self.warewolves[(start_x, start_y)] -= num
                if self.warewolves[(start_x, start_y)] == 0:
                    del self.warewolves[(start_x, start_y)]
                val = num
                if (end_x, end_y) in self.warewolves:
                    val += self.warewolves[(end_x, end_y)]
                self.warewolves[(end_x, end_y)] = val
                return
            self.vampires[(start_x, start_y)] -= num
            if self.vampires[(start_x, start_y)] == 0:
                del self.vampires[(start_x, start_y)]
            val = num
            if (end_x, end_y) in self.vampires:
                val += self.vampires[(end_x, end_y)]
            self.vampires[(end_x, end_y)] = val

    # todo: be smart about the actions order, une case peut pas etre depart et arrivee
    # split the groups to go into different directions
    def get_possible_actions(self, player_type):
        actions = []  # [(depart = (x,y), arrivee=(x,y), nombre de personnes deplacees)
        player = self.vampires
        if player_type == WAREWOLVES:
            player = self.warewolves

        # v0, deplacements en groupe
        # todo: sort (.sort(key=lambda x:x[1]))
        groups = [self.get_possibilities(player_coords, val) for player_coords, val in player.items()]
        # todo remove case where nobody moves
        return [list(x) for x in itertools.product(*groups)]

    def get_possibilities(self, player_coords, val):
        player_x, player_y = player_coords
        actions = []  # the case where that specific group does not move, # ((player_x, player_y), (player_x, player_y), val)
        if self.still_in_grid(player_x - 1, player_y):
            actions += [((player_x, player_y), (player_x - 1, player_y), val)]
        if self.still_in_grid(player_x - 1, player_y + 1):
            actions += [((player_x, player_y), (player_x - 1, player_y + 1), val)]
        if self.still_in_grid(player_x - 1, player_y - 1):
            actions += [((player_x, player_y), (player_x - 1, player_y - 1), val)]
        # x still
        if self.still_in_grid(player_x, player_y + 1):
            actions += [((player_x, player_y), (player_x, player_y + 1), val)]
        if self.still_in_grid(player_x, player_y - 1):
            actions += [((player_x, player_y), (player_x, player_y - 1), val)]
        # x+1 still
        if self.still_in_grid(player_x + 1, player_y):
            actions += [((player_x, player_y), (player_x + 1, player_y), val)]
        if self.still_in_grid(player_x + 1, player_y + 1):
            actions += [((player_x, player_y), (player_x + 1, player_y + 1), val)]
        if self.still_in_grid(player_x + 1, player_y - 1):
            actions += [((player_x, player_y), (player_x + 1, player_y - 1), val)]
        return actions

    def still_in_grid(self, x, y):
        return 0 <= x <= self.rows - 1 and 0 <= y <= self.columns - 1

    def print_pretty(self):
        M = [["_" for row in range(self.rows)] for col in range(self.columns)]
        for (x, y), nombre in self.vampires.items():
            M[x][y] = str(nombre) + "V"

        for (x, y), nombre in self.humans.items():
            M[x][y] = str(nombre) + "H"

        for (x, y), nombre in self.warewolves.items():
            M[x][y] = str(nombre) + "W"

        print(np.matrix(M))
