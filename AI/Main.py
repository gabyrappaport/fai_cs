from AI.Board import Board
from AI.Settings import VAMPIRES

if __name__ == "__main__":
    board = Board(10, 10)
    board.print()
    game_map = [(0, 0, 0, 10, 0), (5, 5, 0, 0, 5)]
    board.update_board(game_map)
    board.print()

    actions = board.get_possible_actions(VAMPIRES)
    print("Actions", actions)