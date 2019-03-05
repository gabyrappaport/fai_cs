from AlphaBeta import Alphabeta
from Settings import VAMPIRES, WAREWOLVES
from TestBoard import TestBoard

from Heuristic import Heuristic

if __name__ == "__main__":

    # board = TestBoard(4, 4)
    # game_map = [
    #     #(lign, col,H ,V , W)
    #     (0, 2, 0, 50, 0),
    #     (1, 1, 0, 0, 6),
    #     (1, 2, 3, 0, 0),
    # ]
    # board.update_board(game_map)
    # board.print_pretty()

    # board.is_playing(VAMPIRES)
    # h = Heuristic(board)
    # print("score board", h.calculate(board))

    board = TestBoard(4, 4)
    game_map = [
        #(lign, col,H ,V , W)
        (0, 2, 0, 50, 0),
        (1, 1, 0, 0, 6),
        (1, 2, 3, 0, 0),
        (1, 3, 0, 5, 0),
    ]
    board.update_board(game_map)
    board.print_pretty()

    board.is_playing(VAMPIRES)
    h = Heuristic(board)
    print("score board", h.calculate(board))

    board = TestBoard(4, 4)
    game_map = [
        #(lign, col,H ,V , W)
        (1, 1, 0, 0, 6),
        (1, 1, 0, 25, 0),
        (1, 2, 3, 0, 0),
        (1, 2, 0, 25, 0),
        (1, 3, 0, 5, 0),
    ]
    board.update_board(game_map)
    board.print_pretty()

    board.is_playing(VAMPIRES)
    h = Heuristic(board)
    print("score board", h.calculate(board))

    board = TestBoard(4, 4)
    game_map = [
        #(lign, col,H ,V , W)
        (1, 1, 0, 0, 6),
        (0, 3, 0, 30, 0),
        (1, 2, 3, 0, 0),
        (0, 1, 0, 25, 0),
    ]
    board.update_board(game_map)
    board.print_pretty()

    board.is_playing(VAMPIRES)
    h = Heuristic(board)
    print("score board", h.calculate(board))
