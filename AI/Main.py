from AI.Board import Board
from AI.Settings import VAMPIRES
from AI.AlphaBeta import Alphabeta

if __name__ == "__main__":

    board = Board(10, 10)
    board.print()
    game_map = [(0, 0, 0, 10, 0), (5, 5, 0, 0, 5)]
    board.update_board(game_map)
    board.print()

    alpha = Alphabeta(board)
