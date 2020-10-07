from graph_games import Tic_tac_toe, Qango6x6
from graph_game import Graph_game

class Alpha_beta():
    def __init__(self, game:Graph_game):
        self.game = game
        self.maximizer = "b"
        self.ttable = {}

    def search(self,alpha,beta):
        if len(self.game.graph)==0:
            return 0
        try:
            return self.ttable[self.game.hash]
        except:
            pass
        if self.game.onturn == self.maximizer:
            value = -1
            moves = self.game.get_actions()
            if moves is None:
                value = 1
            else:
                for move in moves:
                    self.game.make_move(move)
                    value = max(self.search(alpha,beta),value)
                    self.game.revert_moves(1)
                    alpha = max(alpha,value)
                    if alpha>=beta:
                        break
        else:
            value = 1
            moves = self.game.get_actions()
            if moves is None:
                value = -1
            else:
                for move in moves:
                    self.game.make_move(move)
                    value = min(self.search(alpha,beta),value)
                    self.game.revert_moves(1)
                    beta = min(beta,value)
                    if beta<=alpha:
                        break
        self.ttable[self.game.hash] = value
        return value

if __name__ =="__main__":
    game = Tic_tac_toe()
    ab = Alpha_beta(game)
    print(ab.search(-1,1))
