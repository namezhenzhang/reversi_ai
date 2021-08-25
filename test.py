from Othello import Othello
from utils import *
class logic_API:
    def ask_next_pos(self, board, player):
        a = [   1,1,0,0,0,0,0,0,
                1,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,1,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,1,0,0,0,0,
                0,0,0,0,0,0,0,0    ]            

        # a[2]=1
        return a
player = 1
enemy = 1
board = [   2,2,1,1,1,1,1,2,
            2,0,1,1,1,1,2,2,
            1,0,0,1,1,1,2,0,
            1,1,1,1,1,1,0,2,
            1,0,0,0,0,0,2,2,
            1,1,1,0,0,1,1,1,
            2,2,2,2,0,2,2,2,
            2,2,2,2,2,2,2,2]
logic = logic_API()
step = 2
O = Othello(board,player,player,logic,step,True,step,2)

print(O.get_next_step_id_by_alphabeta())
print(Othello.num,'|',Othello.eval_num)
print(ask_next_pos(board, player))
# print(O.get_next_step_id())