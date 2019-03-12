from AlphaBeta import Alphabeta
from Settings import VAMPIRES, WAREWOLVES
from TestBoard import TestBoard

if __name__ == "__main__":

    board = TestBoard(5, 6)

    game_map = [
         #(x, y,H ,V , W)
         (3, 0, 0, 0, 6),
         (0, 1, 0, 6, 0),
         (4, 4, 2, 0, 0),
     ]

    # game_map = [
    #     # (x, y, H ,V , W)
    #     (2, 2, 4, 0, 0),
    #     (9, 0, 2, 0, 0),
    #     (9, 2, 1, 0, 0),
    #     (9, 4, 2, 0, 0),
    #     (4, 1, 0, 0, 4),
    #     (4, 3, 0, 4, 0),
    # ]
    # game_map = [
    #     # (lign, col,H ,V , W)
    #     (0, 0, 0, 0, 6),
    #     (0, 1, 0, 58, 0),
    # ]
    board.update_board(game_map)
    board.print_pretty()

    alpha_vampire = Alphabeta(board, player=VAMPIRES)
    alpha_warewold = Alphabeta(board, player=WAREWOLVES)

    for i in range(10):
        print("\n Tour", i)

        alpha_warewold.board = board
        move_w = alpha_warewold.alphabeta()
        print("WAREWOLVES move", move_w)
        board.play_with_battle(move_w, WAREWOLVES)
        board.print_pretty()

        alpha_vampire.board = board
        move = alpha_vampire.alphabeta()
        print("VAMPIRES move", move)
        board.play_with_battle(move, VAMPIRES)
        board.print_pretty()


