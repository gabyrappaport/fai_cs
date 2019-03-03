from Board import Board
from Settings import VAMPIRES, WAREWOLVES
from AlphaBeta import Alphabeta

if __name__ == "__main__":

    board = Board(5, 5)
    board.display()
    game_map = [
    	(0, 0, 0, 4, 0),
    	(0, 1, 1, 0, 0),
    	(2, 0, 0, 0, 6),
    	(1, 2, 3, 0, 0),
    	(3, 2, 0, 5, 0),
    	(1, 4, 0, 0, 3)
    ]
    board.update_board(game_map)
    board.display()

    alpha_vampire = Alphabeta(board, player=VAMPIRES)
    alpha_warewold = Alphabeta(board, player=WAREWOLVES)

    for i in range(10):

    	print("\n Tour", i)

    	alpha_vampire.board = board
    	move = alpha_vampire.alphabeta()
    	print("Move vampire", move)
    	board.play(move, VAMPIRES)

    	alpha_warewold.board = board
    	move_w = alpha_warewold.alphabeta()
    	print("Move warewolf", move_w)
    	board.play(move_w, WAREWOLVES)
