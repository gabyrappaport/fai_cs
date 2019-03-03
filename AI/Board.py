class Board:
    def __init__(self, row, column, us, them, humans):
        self.row = row
        self.column = column
        self.us = us
        self.them = them
        self.humans = humans

    def update_board_us(self, changes):
        pass

    def update_board_them(self, changes):
        pass
