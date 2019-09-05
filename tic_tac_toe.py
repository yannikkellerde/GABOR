import math
from that_kind_of_game import Game
from util import getwinhash, test_game

class Tic_tac_toe(Game):
    def __init__(self):
        self.squares = 9
        self.winpatterns = [
            (2**0)|(2**1)|(2**2),
            (2**3)|(2**4)|(2**5),
            (2**6)|(2**7)|(2**8),
            (2**0)|(2**3)|(2**6),
            (2**1)|(2**4)|(2**7),
            (2**2)|(2**5)|(2**8),
            (2**0)|(2**4)|(2**8),
            (2**2)|(2**4)|(2**6)
        ]
        self.winhash = getwinhash(self.winpatterns, self.squares)
        self.reset()

    def __str__(self):
        return "tic_tac_toe"

if __name__ == "__main__":
    test_game(Tic_tac_toe())