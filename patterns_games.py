from patterns_game import Patterns_Game

class Tic_tac_toe(Patterns_Game):
    def __init__(self,startpos,zobrist_file="zobrist_tik_tac_toe.pkl"):
        squares = 9
        winpatterns = [
            (1<<0)|(1<<1)|(1<<2),
            (1<<3)|(1<<4)|(1<<5),
            (1<<6)|(1<<7)|(1<<8),
            (1<<0)|(1<<3)|(1<<6),
            (1<<1)|(1<<4)|(1<<7),
            (1<<2)|(1<<5)|(1<<8),
            (1<<0)|(1<<4)|(1<<8),
            (1<<2)|(1<<4)|(1<<6)
        ]
        super().__init__(winpatterns,startpos,squares,zobrist_file)

class Qango6x6