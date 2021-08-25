from src.utils import *
import json
from tqdm import tqdm
with open('rewth/2001-2015_dataset.json','r') as file_obj:
    data = json.load(file_obj)
init_board = [
            2,2,2,2,2,2,2,2,
            2,2,2,2,2,2,2,2,
            2,2,2,2,2,2,2,2,
            2,2,2,1,0,2,2,2,
            2,2,2,0,1,2,2,2,
            2,2,2,2,2,2,2,2,
            2,2,2,2,2,2,2,2,
            2,2,2,2,2,2,2,2
        ]  
dataset = {'board':[],'next_step_id':[],'turn':[],'black_chess_num':[]}
for idx,chessbook in enumerate(tqdm(data['moves'])):

    # chessbook = data['moves'][1000]
    black_chess_num = data['black_chess_num'][idx]
    turn = 0
    now_board = init_board
    for idx,step in enumerate(chessbook):
        # if step == 11:
        #     print(11)
        if step == 0:
            break
        x = step%10 -1
        y = step//10 -1
        id = xy2id((x,y))
        
        # n_step = chessbook[idx+1]
        # if n_step==0:
        #     break
        # n_x = n_step%10 -1
        # n_y = n_step//10 -1
        # n_id = xy2id((n_x,n_y))
        next_pos = ask_next_pos(now_board,turn,need_id = True)
        if len(next_pos) == 0:
            turn = 0 if turn==1 else 1
            next_pos = ask_next_pos(now_board,turn,need_id = True)
            assert len(next_pos) !=0 , 'turn wrong'
            
        dataset['board'].append(now_board.copy())
        dataset['next_step_id'].append(id)
        dataset['turn'].append(turn)
        dataset['black_chess_num'].append(black_chess_num) 
          
        next_board = get_next_step_board(now_board,turn,id)
        now_board = next_board.copy()
        # next_board = list(map(two2_,next_board))
        # print(next_board[0:8])
        # print(next_board[8:16])
        # print(next_board[16:24])
        # print(next_board[24:32])
        # print(next_board[32:40])
        # print(next_board[40:48])
        # print(next_board[48:56])
        # print(next_board[56:64])
        # print('\n')
        if len(next_pos) >0:
            turn = 0 if turn==1 else 1
with open('rewth/2001-2015_dataset_board.json','w') as file_obj:
    json.dump(dataset,file_obj)