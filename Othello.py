import sys
from typing import NamedTuple
from utils import *
#3f0c0f57cf4042e2869760c1fa9dfd03
#https://www.saiblo.net/match/2411719/
# id2xy = lambda id: (id%8,id//8)
# xy2id = lambda a: a[1]*8 + a[0]
# xyadd = lambda a,b: (a[0]+b[0],a[1]+b[1])
# notout = lambda x: (0<=x[0]<=7 and 0<=x[1]<=7)
class Othello:

    num = 0
    eval_num = 0

    def __init__(self, board, player, me, logic, step, is_root, search_steps,
                 remaining_steps,pased= False):
        Othello.num += 1
        self.board = board
        self.player = player
        self.me = me
        self.is_me = me == player
        self.enemy = 0 if player == 1 else 1
        self.logic = logic
        self.step = step
        self.score = None
        self.next_step_id_list = None
        self.minmax_ = None
        self.next_step_id_list = None
        self.true_board = None
        self.end = False
        self.is_root = is_root
        self.search_steps = search_steps
        self.remaining_steps = remaining_steps
        self.pased = pased
        # sys.stderr.write(f"{Othello.num}\n",flush=True)
        # print(Othello.num,file = sys.stderr,flush=True)

    def get_minmax_by_alphabeta(self, last_minmax):
        '''
        推演下一步
        '''
        if self.step == 0:
            self.score = self.eval(self.board, self.logic)
            self.minmax_ = self.score
            return self.minmax_

        self.next_step_id_list = []
        # next_list = self.logic.ask_next_pos(self.board, self.player)
        next_list = ask_next_pos(self.board, self.player)

        for id, b in enumerate(next_list):
            if b == 1:
                self.next_step_id_list.append(id)

        self.next_step_len = len(self.next_step_id_list)
        delta_for_pass = 0
        next_Othello = None
        if self.next_step_len==0:
            if self.pased:
                self.score = self.eval(self.board, self.logic)
                self.minmax_ = self.score
                return self.minmax_
            else: 
                self.next_step_id_list = [-1]
                delta_for_pass = 1
                self.pased = True

        self.next_Othello_list = []
        if self.is_me: 
            max = -float('inf')
            for id in self.next_step_id_list:
                if id != -1:
                    next_step_board = get_next_step_board(
                    self.board, self.player, id)
                    next_Othello = Othello(next_step_board, self.enemy, self.me,
                                       self.logic, self.step - 1, False,
                                       self.search_steps, self.remaining_steps)
                else: 
                    next_step_board = self.board.copy()
                    next_Othello = Othello(next_step_board, self.enemy, self.me,
                                       self.logic, self.step, False,
                                       self.search_steps, self.remaining_steps,pased = self.pased)
                if self.is_root:
                    self.next_Othello_list.append(next_Othello)
                minmax = next_Othello.get_minmax_by_alphabeta(max)
                if minmax > max:
                    max = minmax
                if max > last_minmax:
                    break
            self.minmax_ = max

        else:
            min = float('inf')
            for id in self.next_step_id_list:
                if id != -1:
                    next_step_board = get_next_step_board(
                    self.board, self.player, id)
                    next_Othello = Othello(next_step_board, self.enemy, self.me,
                                       self.logic, self.step - 1,
                                       False,self.search_steps, 
                                       self.remaining_steps)
                else: 
                    next_step_board = self.board.copy()
                    next_Othello = Othello(next_step_board, self.enemy, self.me,
                                       self.logic, self.step, False,
                                       self.search_steps, self.remaining_steps,pased = self.pased)
                if self.is_root:
                    self.next_Othello_list.append(next_Othello)
                minmax = next_Othello.get_minmax_by_alphabeta(min)
                if minmax < min:
                    min = minmax
                if min < last_minmax:
                    break
            self.minmax_ = min
        return self.minmax_

    # def get_next_step_board(self, board, player, id):
    #     '''
    #     棋盘推演
    #     '''
    #     next_board = board.copy()
    #     move = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
    #     enemy = 1 if player == 0 else 0
        
    #     for m in move:  
    #         reversi_list = []
    #         ptr_xy = xyadd(id2xy(id),m)
    #         while notout(ptr_xy):  
    #             ptr_id = xy2id(ptr_xy)
    #             chess = next_board[ptr_id]
    #             if chess == 2: 
    #                 break
    #             if chess == enemy:
    #                 reversi_list.append(ptr_id)
    #             if chess == player:  
    #                 for i in reversi_list: 
    #                     next_board[i] = player
    #                 break
    #             ptr_xy = xyadd(ptr_xy,m)
    #     next_board[id] = player
    #     return next_board

    # @property
    # def minmax(self):
    #     if not self.minmax_:
    #         if self.end:
    #             self.score = self.eval(self.board, self.logic)
    #             return self.score
    #         self.minmax_list = []
    #         for Othello_item in self.next_Othello_list:
    #             self.minmax_list.append(Othello_item.minmax)

    #         if self.player != self.me:
    #             self.minmax_ = min(self.minmax_list)
    #         else:
    #             self.minmax_ = max(self.minmax_list)
    #     return self.minmax_

    def get_next_step_id_by_alphabeta(self):

        max = self.get_minmax_by_alphabeta(float('inf'))
        minmax_list = []
        for i in self.next_Othello_list:
            minmax_list.append(i.minmax_)
        assert len(
            minmax_list
        ) == self.next_step_len, "minmax_list & next_step_len are not equal"
        idx = minmax_list.index(max)
        print(
            self.search_steps,'/',self.remaining_steps,"|",minmax_list,"|chose: ",idx,"|",
            file=sys.stderr,
            flush=True)
        return self.next_step_id_list[idx]

    def eval(self, board, logic):
        '''
        计算当前棋局分数
        '''
        Othello.eval_num += 1
        score = 0
        self.true_board = board.copy()
        for idx, i in enumerate(board):
            if i == self.me:
                self.true_board[idx] = 1
            elif i == 2:
                self.true_board[idx] = 0
            else:
                self.true_board[idx] = -1
        if self.true_board.count(1) == 0:
            return -float('inf')
        if self.true_board.count(-1) == 0:
            return float('inf')
        score_board = [
            0x1 << 24, 0x1, 0x1 << 20, 0x1 << 16, 0x1 << 16, 0x1 << 20, 0x1,
            0x1 << 24, 0x1, 0x1, 0x1 << 16, 0x1 << 4, 0x1 << 4, 0x1 << 16, 0x1,
            0x1, 0x1 << 20, 0x1 << 16, 0x1 << 12, 0x1 << 8, 0x1 << 8,
            0x1 << 12, 0x1 << 16, 0x1 << 20, 0x1 << 16, 0x1 << 4, 0x1 << 8, 0,
            0, 0x1 << 8, 0x1 << 4, 0x1 << 16, 0x1 << 16, 0x1 << 4, 0x1 << 8, 0,
            0, 0x1 << 8, 0x1 << 4, 0x1 << 16, 0x1 << 20, 0x1 << 16, 0x1 << 12,
            0x1 << 8, 0x1 << 8, 0x1 << 12, 0x1 << 16, 0x1 << 20, 0x1, 0x1,
            0x1 << 16, 0x1 << 4, 0x1 << 4, 0x1 << 16, 0x1, 0x1, 0x1 << 24, 0x1,
            0x1 << 20, 0x1 << 16, 0x1 << 16, 0x1 << 20, 0x1, 0x1 << 24
        ]
        if self.search_steps >= self.remaining_steps:
            score_board = [1] * 64
            # print("use 1",end=' ',file = sys.stderr,flush=True)

        for i in range(64):
            score += score_board[i] * self.true_board[i]

        return score
