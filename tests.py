from patterns_game import Patterns_Game,convert_into_patterns_game
from patterns_games import Tic_tac_toe, Qango6x6
from util import draw_board,board_to_pos
import time
import math

def test_aval_tic():
    p1 = """#####
            #X O#
            # O #
            #  X#
            #####"""
    true_pos = board_to_pos(p1)
    draw_board(true_pos,9)
    game = Tic_tac_toe(startpos=[true_pos,False])
    print(hash(game))
    p1 = """#####
            #X O#
            # O #
            # X #
            #####"""
    true_pos = board_to_pos(p1)
    draw_board(true_pos,9)
    game = Tic_tac_toe(startpos=[true_pos,False])
    print(hash(game))
    exit()
    print(game.aval_squares)
    game = Tic_tac_toe(startpos=[[0,0],True])
    game.make_move(1)
    game.make_move(64)
    game.make_move(16)
    game.make_move(32)
    draw_board(game.position,game.squares)
    print(game.aval_squares)
    print(hash(game))
    game.make_move(256)
    draw_board(game.position,game.squares)
    print(hash(game))

def test_patterns_qango():
    pos1 = [
      int("0b001000"
            "000000"
            "000000"
            "000000"
            "000100"
            "000000",2),
      int("0b100000"
            "001000"
            "000000"
            "000000"
            "000000"
            "000100",2),
    ]
    pos2 = [
      int("0b000000"
            "000000"
            "100000"
            "000010"
            "000000"
            "000000",2),
      int("0b000000"
            "000000"
            "010000"
            "000001"
            "000000"
            "100000",2),
    ]
    q1 = Qango6x6([pos1.copy(),True])
    q2 = Qango6x6([pos2.copy(),True])
    draw_board(q1.position,q1.squares)
    draw_board(q2.position,q2.squares)
    start = time.perf_counter()
    print(hash(q1)==hash(q2))
    print(time.perf_counter()-start)
def test_tic_tac_toe():
    pos = [
        int("0b000"
              "000"
              "000",2),
        int("0b000"
              "010"
              "000",2)
    ]
    t = Tic_tac_toe([pos.copy(),True])
    draw_board(t.position,t.squares)
    hash1 = hash(t)
    pos = [
        int("0b000"
              "000"
              "000",2),
        int("0b000"
              "000"
              "010",2)
    ]
    t = Tic_tac_toe([pos.copy(),True])
    draw_board(t.position,t.squares)
    hash2 = hash(t)
    print(hash1==hash2)

def test_get_actions():
    q = Qango6x6()
    pos1 = [
      int("0b000100"
            "000000"
            "000101"
            "000010"
            "001100"
            "000000",2),
      int("0b000000"
            "000011"
            "000010"
            "000100"
            "000000"
            "110100",2),
    ]
    pos2 = [
      int("0b000101"
            "010000"
            "001101"
            "010010"
            "000110"
            "010000",2),
      int("0b000010"
            "001111"
            "010010"
            "001101"
            "001000"
            "000100",2),
    ]
    q.set_state(pos2, False)
    print(sorted([int(round(math.log(x,2))) for x in q.get_actions()]))
    print(q.position)
def test_pg():
    q = Qango6x6()
    pos1 = [
      int("0b000001"
            "010010"
            "100000"
            "011110"
            "010000"
            "000010",2),
      int("0b000010"
            "000001"
            "010010"
            "100001"
            "010000"
            "100001",2),
    ]
    q.set_state(pos1, True)
    pg = convert_into_patterns_game(q)
    pg.sort_myself()
    print(pg)
def testfull():
    q=Qango6x6()
    pos1 = [
      int("0b100000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
      int("0b010000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
    ]
    pos2 = [
      int("0b111111"
            "111111"
            "111111"
            "000000"
            "000000"
            "000000",2),
      int("0b000000"
            "000000"
            "000000"
            "111111"
            "111111"
            "111111",2),
    ]
    q.set_state(pos2, True)
    assert q.check_full()==True
    q.set_state(pos1, True)
    assert q.check_full()==False

def teshash():
    q=Qango6x6()
    pos1 = [
      int("0b100000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
      int("0b010000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
    ]
    pos2 = [
      int("0b000001"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
      int("0b000010"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
    ]
    pos3 = [
      int("0b000001"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
      int("0b000000"
            "000001"
            "000000"
            "000000"
            "000000"
            "000000",2),
    ]
    pos4 = [
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000001",2),
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000001"
            "000000",2),
    ]
    pos5 = [
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000001",2),
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000010",2),
    ]
    pos6 = [
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000000"
            "100000",2),
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000000"
            "010000",2),
    ]
    pos7 = [
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000000"
            "100000",2),
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "100000"
            "000000",2),
    ]
    pos8 = [
      int("0b100000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
      int("0b000000"
            "100000"
            "000000"
            "000000"
            "000000"
            "000000",2),
    ]
    neq1 = [
      int("0b000000"
            "100000"
            "000000"
            "000000"
            "000000"
            "000000",2),
      int("0b100000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000000",2),
    ]
    neq2 = [
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000001"
            "000000",2),
      int("0b000000"
            "000000"
            "000000"
            "000000"
            "000000"
            "000001",2),
    ]
    poses = [pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,neq1,neq2]
    def dohash(p):
      q.position=p
      return q.hashpos()
    print([dohash(p) for p in poses])

if __name__=='__main__':
    test_aval_tic()