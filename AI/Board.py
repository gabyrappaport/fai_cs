from Settings import HUMANS, VAMPIRES, WAREWOLVES

class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.vampires = {} # key = (x,y) ; value = number of vampires
        self.warewolves = {}
        self.humans = {}
        self.reinit_numb()

    def print(self):
        print("Vampires", self.vampires)
        print("Warewolves", self.warewolves)
        print("Humans", self.humans)

    def reinit_numb(self):
        self.nbr_vampires = 0
        self.nbr_warewolves = 0
        self.nbr_humans = 0

    def update_board(self, game_map):
        self.reinit_numb()
        for (x, y, humans, vampires, warewolves) in game_map:
            if humans > 0:
                self.humans[(x,y)] = humans
                self.nbr_humans += humans
            if vampires > 0:
                self.vampires[(x,y)] = vampires
                self.nbr_vampires += vampires
            if warewolves > 0:
                self.warewolves[(x,y)] = warewolves
                self.nbr_warewolves += warewolves

    def play(self, action, player_type):
        ((start_x, start_y), (end_x, end_y), num) = action
        if player_type == WAREWOLVES:
            self.warewolves[(start_x, start_y)] -= num
            self.warewolves[(end_x, end_y)] += num
            return
        self.vampires[(start_x, start_y)] -= num
        self.vampires[(end_x, end_y)] += num

    # todo: be smart about the actions order, une case peut pas etre depart et arrivee
    def get_possible_actions(self, player_type):
        actions = [] # [(depart = (x,y), arrivee=(x,y), nombre de personnes deplacees)
        player = self.vampires
        if player_type == WAREWOLVES:
            player = self.warewolves
        for (player_x, player_y), val in player.items():
            # x-1 still
            if self.still_in_grid(player_x-1, player_y):
                actions += [((player_x, player_y), (player_x-1, player_y), i) for i in range(val, 0, -1)]
            if self.still_in_grid(player_x-1, player_y+1):
                actions += [((player_x, player_y), (player_x-1, player_y+1), i) for i in range(val, 0, -1)]
            if self.still_in_grid(player_x-1, player_y-1):
                actions += [((player_x, player_y), (player_x-1, player_y-1), i) for i in range(val, 0, -1)]
            # x still
            if self.still_in_grid(player_x, player_y+1):
                actions += [((player_x, player_y), (player_x, player_y+1), i) for i in range(val, 0, -1)]
            if self.still_in_grid(player_x, player_y-1):
                actions += [((player_x, player_y), (player_x, player_y-1), i) for i in range(val, 0, -1)]
            # x+1 still
            if self.still_in_grid(player_x+1, player_y):
                actions += [((player_x, player_y), (player_x+1, player_y), i) for i in range(val, 0, -1)]
            if self.still_in_grid(player_x+1, player_y+1):
                actions += [((player_x, player_y), (player_x+1, player_y+1), i) for i in range(val, 0, -1)]
            if self.still_in_grid(player_x+1, player_y-1):
                actions += [((player_x, player_y), (player_x+1, player_y-1), i) for i in range(val, 0, -1)]
        return actions

    def still_in_grid(self, x, y):
        return x>0 and y>0 and x<self.rows-1 and y<self.columns-1

