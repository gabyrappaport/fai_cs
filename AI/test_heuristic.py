from AlphaBeta import Alphabeta
from Settings import VAMPIRES, WAREWOLVES
from TestBoard import TestBoard

from AI.Heuristic import Heuristic

if __name__ == "__main__":

    board = TestBoard(4, 4)
    game_map = [
        #(lign, col,H ,V , W)
        (0, 2, 0, 50, 0),
        (1, 1, 0, 0, 6),
        (1, 2, 3, 0, 0),
    ]
    board.update_board(game_map)
    board.print_pretty()
    h = Heuristic(board)
    print("score board", h.calculate(board))

    board = TestBoard(5, 5)
    game_map = [
        # (lign, col,H ,V , W)
        (1, 1, 0, 0, 6),
        (1, 1, 0, 25, 0),
        (1, 2, 3, 0, 0),
        (1, 2, 0, 25, 0),
    ]
    board.update_board(game_map)
    board.print_pretty()
    h = Heuristic(board)
    print("score board", h.calculate(board))

    board = TestBoard(5, 5)
    game_map = [
        # (lign, col,H ,V , W)
        (0, 3, 0, 50, 0),
        (1, 1, 0, 0, 6),
        (1, 2, 3, 0, 0),
    ]
    board.update_board(game_map)
    board.print_pretty()
    h = Heuristic(board)
    print("score board", h.calculate(board))

    #alpha_vampire = Alphabeta(board, player=VAMPIRES)

    # alpha_warewold = Alphabeta(board, player=WAREWOLVES)
    #
    # for i in range(10):
    #     print("\n Tour", i)
    #
    #     alpha_vampire.board = board
    #     move = alpha_vampire.alphabeta()
    #     board.play_with_battle(move, VAMPIRES)
    #     board.print_pretty()
    #
    #     alpha_warewold.board = board
    #     move_w = alpha_warewold.alphabeta()
    #     board.play_with_battle(move_w, WAREWOLVES)
    #     board.print_pretty()
