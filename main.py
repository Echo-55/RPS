import pygame
from src.game.rps_game import RPSGame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

def main():
    game = RPSGame()
    game.init()
    game.show()

    game.quit()

if __name__ == "__main__":
    main()

