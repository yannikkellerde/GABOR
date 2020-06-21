import math

class Game():
    """Abstract Game class. Do not instantiate"""
    startpos:list
    squares:int
    fullness:int
    position:list
    winpatterns:set
    winhash:dict

    def reset(self):
        self.position, self.onturn = self.startpos
    
    def set_state(self, position, onturn):
        self.position = list(position)
        self.onturn = onturn

    def get_actions(self):
        actions = []
        whatsfree = ~(self.position[0]|self.position[1])
        for i in range(self.squares):
            val = (1<<i)&whatsfree
            if val:
                actions.append(val)
        return actions

    def check_full(self):
        return not ((self.position[0]|self.position[1])^self.fullness)

    def check_win(self, action):
        for p in self.winhash[action]:
            if not (p^self.position[not self.onturn])&p:
                return True
        return False
    
    def check_any_win(self):
        for p in self.winpatterns:
            if not (p^self.position[True])&p:
                return True
            elif not (p^self.position[False])&p:
                return False
        return None

    def make_move(self, action):
        self.position[self.onturn] |= action
        self.onturn = not self.onturn

    def convert_human_readable(self, move):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        rows = math.sqrt(self.squares)
        small_move = math.log2(move)
        return alphabet[int(small_move % rows)]+str(int(small_move//rows))