from game import Game
from player import Player
from board import Board

def main():
    player_1 = Player("Player 1", "white")
    player_2 = Player("Player 2", "black")
    players = [player_1, player_2]
    game = Game(players, 2, 8)

    print(game.board.grid)



if __name__ == '__main__':
    main()