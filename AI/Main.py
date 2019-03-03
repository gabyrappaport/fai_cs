from Board import Board
from Settings import VAMPIRES
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

    alpha = Alphabeta(board, player=VAMPIRES)
    move = alpha.alphabeta()
    print("Move", move)

    board.play(move, VAMPIRES)

    move = alpha.alphabeta()
    print("Move", move)
