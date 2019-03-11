import itertools
import math
#import numpy as np
import random

from Settings import VAMPIRES
from Settings import WAREWOLVES


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.vampires = {}  # key = (x,y) ; value = number of vampires
        self.warewolves = {}
        self.humans = {}

    def is_playing(self, player_type):
        if player_type == WAREWOLVES:
            self.player = Player(WAREWOLVES, self.warewolves)
            self.enemy = Player(VAMPIRES, self.vampires)
        else:
            self.player = Player(VAMPIRES, self.vampires)
            self.enemy = Player(WAREWOLVES, self.warewolves)

    def update_board(self, game_map):
        for (x, y, humans, vampires, warewolves) in game_map:
            self.humans[(x, y)] = humans
            self.vampires[(x, y)] = vampires
            self.warewolves[(x, y)] = warewolves
            if self.humans[(x, y)] == 0: del self.humans[(x, y)]
            if self.vampires[(x, y)] == 0: del self.vampires[(x, y)]
            if self.warewolves[(x, y)] == 0: del self.warewolves[(x, y)]

    def play_dep(self, action):
        for move in action:
            (start_x, start_y), (end_x, end_y), num = move
            self.player.dict[(start_x, start_y)] -= num
            if self.player.dict[(start_x, start_y)] == 0:
                del self.player.dict[(start_x, start_y)]
            val = num
            if (end_x, end_y) in self.player.dict:
                val += self.player.dict[(end_x, end_y)]
            self.player.dict[(end_x, end_y)] = val
        self.update_dict()

    def play(self, moves):
        for move in moves:
            (start_x, start_y), (end_x, end_y), num = move
            self.player.dict[(start_x, start_y)] -= num
            if self.player.dict[(start_x, start_y)] == 0:
                del self.player.dict[(start_x, start_y)]
            if (not (end_x, end_y) in self.enemy.dict) and (not (end_x, end_y) in self.humans):
                add = num
                if (end_x, end_y) in self.player.dict:
                    add += self.player.dict[(end_x, end_y)]
                self.player.dict[(end_x, end_y)] = add
                self.update_dict()
                return

                # Enemy battle
            if (end_x, end_y) in self.enemy.dict:
                enemies_num = self.enemy.dict[(end_x, end_y)]
                if enemies_num > 1.5 * num:
                    self.enemy.dict[(end_x, end_y)] += num
                    self.update_dict()
                    return
                if num > 1.5 * enemies_num:
                    del self.enemy.dict[(end_x, end_y)]
                    self.player.dict[(end_x, end_y)] = num + enemies_num
                    self.update_dict()
                    return
                p = 0.5
                if num > enemies_num:
                    p = num / enemies_num - 0.5
                if enemies_num > num:
                    p = 0.5 * num / enemies_num
                rand = random.random()
                if rand < p:
                    # Player wins
                    del self.enemy.dict[(end_x, end_y)]
                    self.player.dict[(end_x, end_y)] = math.floor(p * num)
                    self.update_dict()
                    return
                else:
                    self.enemy.dict[(end_x, end_y)] = math.floor((1 - p) * enemies_num)
                    self.update_dict()
                    return
            # Human battle
            if (end_x, end_y) in self.humans:
                humans_num = self.humans[(end_x, end_y)]
                if num > humans_num:
                    del self.humans[(end_x, end_y)]
                    self.player.dict[(end_x, end_y)] = num + humans_num
                    self.update_dict()
                    return
                p = 0.5
                if num > humans_num:
                    p = num / humans_num - 0.5
                if humans_num > num:
                    p = 0.5 * num / humans_num
                rand = random.random()
                if rand < p:
                    # Player wins
                    del self.humans[(end_x, end_y)]
                    self.player.dict[(end_x, end_y)] = math.floor(p * num) + math.floor(p * humans_num)
                    self.update_dict()
                    return

    def update_dict(self):
        if self.player.type == VAMPIRES:
            self.vampires = self.player.dict
            self.warewolves = self.enemy.dict
        else:
            self.warewolves = self.player.dict
            self.vampires = self.enemy.dict

    def get_possible_actions_dep(self):
        player_type = self.player.type
        actions = []  # [(depart = (x,y), arrivee=(x,y), nombre de personnes deplacees)
        player = self.vampires
        if player_type == WAREWOLVES:
            player = self.warewolves

        # v0, deplacements en groupe
        # todo: sort (.sort(key=lambda x:x[1]))
        groups = [self.get_possibilities_move_together(player_coords, val) for player_coords, val in
                  player.items()]
        # todo remove case where nobody moves
        result = [list(x) for x in itertools.product(*groups)]
        return result

    def get_possible_actions(self):
        actions = []
        for player_coords, val in self.player.dict.items():
            all_together = self.get_possibilities_move_together(player_coords, val)
            split = []
            if val > self.player.get_mean():
                split = self.actions_after_split_in_two(player_coords, val)
            actions.append(split + all_together)
        result = [self.flatten(list(x)) for x in itertools.product(*actions)]
        return list(filter(([]).__ne__, result))

    def flatten(self, l):
        result = []
        start = []
        end = []
        for item in l:
            if isinstance(item, list):
                for i in item:
                    if i != ():
                        start.append(i[0])
                        end.append(i[1])
                        result.append(i)
            else:
                if item != ():
                    start.append(item[0])
                    end.append(item[1])
                    result.append(item)
        intersection = set(start).intersection(end)
        if len(intersection) == 0:
            return result
        return []

    def get_possibilities_move_together(self, player_coords, val):
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

    def actions_after_split_in_two(self, player_coords, val):
        actions = []
        for i in range(val // 2, val // 2 + 1):
            actions_split = []
            actions_split += [self.get_possibilities_move_together(player_coords, i)]
            actions_split += [self.get_possibilities_move_together(player_coords, val - i)]
            for x in itertools.product(*actions_split):
                a, b = x
                if list(a)[1] != list(b)[1]:  # We remove the cases where each split moves to the same direction.
                    actions += [list(x)]
        return actions

    def still_in_grid(self, x, y):
        return 0 <= x <= self.rows - 1 and 0 <= y <= self.columns - 1

    # def print_pretty(self):
    #     M = [["__" for row in range(self.rows)] for col in range(self.columns)]
    #     for (x, y), nombre in self.vampires.items():
    #         M[x][y] += str(nombre) + "V"
    #
    #     for (x, y), nombre in self.humans.items():
    #         M[x][y] += str(nombre) + "H"
    #
    #     for (x, y), nombre in self.warewolves.items():
    #         M[x][y] += str(nombre) + "W"
    #
    #     print(np.matrix(M))


class Player:

    def __init__(self, type, dict):
        self.type = type
        self.dict = dict

    def get_count(self):
        return sum(self.dict.values())

    def get_mean(self):
        return sum(self.dict.values()) / len(self.dict.keys()) if self.dict else 0
