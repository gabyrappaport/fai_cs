class Board:
    def __init__(self, row, column, us, nbr_us, nbr_enemies, nbr_humans):
        self.row = row
        self.column = column
        self.us = us
        self.nbr_us = nbr_us
        self.nbr_enemies = nbr_enemies
        self.nbr_humans = nbr_humans

    def update_board(self, changes):
        pass
