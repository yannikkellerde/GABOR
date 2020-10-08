from graph_games import Tic_tac_toe, Qango6x6
from graph_game import Graph_game
import pickle

class Alpha_beta():
    def __init__(self, game:Graph_game):
        self.game = game
        self.maximizer = "b"
        self.ttable = {}

    def search(self,alpha,beta,depth):
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
                    value = max(self.search(alpha,beta,depth+1),value)
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
                    value = min(self.search(alpha,beta,depth+1),value)
                    self.game.revert_moves(1)
                    beta = min(beta,value)
                    if beta<=alpha:
                        break
        if len(self.ttable)%1000==0:
            if len(self.ttable)%100000 == 0:
                with open("alpha_beta.pkl", "wb") as f:
                    pickle.dump(self.ttable, f)
            print(len(self.ttable))
        self.ttable[self.game.hash] = value
        return value

if __name__ =="__main__":
    game = Qango6x6()
    ab = Alpha_beta(game)
    print(ab.search(-1,1,0))
    with open("alpha_beta.pkl", "wb") as f:
        pickle.dump(ab.ttable, f)
