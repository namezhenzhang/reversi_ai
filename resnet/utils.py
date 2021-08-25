import torch
id2xy = lambda id: (id%8,id//8)
xy2id = lambda a: a[1]*8 + a[0]
xyadd = lambda a,b: (a[0]+b[0],a[1]+b[1])
notout = lambda x: (0<=x[0]<=7 and 0<=x[1]<=7)
def trans_chessbook_to_input(x):
    a = torch.Tensor(x).view(8,8)
    i_list = []
    for i in range(8):
        j_list = []
        for j in range(8):
            b = torch.cat([a[i,j].unsqueeze(0)]*28)
            c = torch.stack([b]*28,dim = 1)
            j_list.append(c)
        i_list.append(torch.cat(j_list,dim = 1))
    d = torch.cat(i_list,dim=0)
    # print(d.shape)
    input = torch.stack((d,d,d),dim = 0)
    return input
def convert_chessbook(player,board):
    convert_board = list(map(trans_id_for_model[player],board))
    return convert_board
def trans_id_for_model0(idx):
    if idx==0:
        return 1
    elif idx==2:
        return 0
    else:
        return -1
def trans_id_for_model1(idx):
    if idx==1:
        return 1
    elif idx==2:
        return 0
    else:
        return -1
trans_id_for_model = [trans_id_for_model0,trans_id_for_model1]
def get_next_step_board( board, player, id,for_model = False):
    '''
    棋盘推演
    落子后的棋盘
    '''
    next_board = board.copy()
    move = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
    enemy = 1 if player == 0 else 0
    changed = False
    for m in move:  
        reversi_list = []
        ptr_xy = xyadd(id2xy(id),m)
        while notout(ptr_xy):  
            ptr_id = xy2id(ptr_xy)
            chess = next_board[ptr_id]
            if chess == 2: 
                break
            if chess == enemy:
                reversi_list.append(ptr_id)
            if chess == player:  
                if len(reversi_list)>0:
                    changed = True
                for i in reversi_list: 
                    next_board[i] = player
                break
            ptr_xy = xyadd(ptr_xy,m)
    assert changed,"no chess reversed"
    next_board[id] = player
    if for_model:
        next_board = list(map(trans_id_for_model[player],next_board))
    else:  
        pass
    return next_board
def ask_next_pos(board, player,need_id = False):
    '''
    可落子位置
    '''
    move = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
    enemy = 1 if player == 0 else 0
    id_list = []
    for id in range(64):
        if board[id] != 2:
            continue
        is_pos = False
        for m in move:  
            reversi_list = False
            ptr_xy = xyadd(id2xy(id),m)
            while notout(ptr_xy):  
                ptr_id = xy2id(ptr_xy)
                chess = board[ptr_id]
                if chess == 2: 
                    break
                if chess == enemy:
                    reversi_list=True
                if chess == player:  
                    if reversi_list: 
                        is_pos = True
                    break
                ptr_xy = xyadd(ptr_xy,m)
            if is_pos: 
                id_list.append(id)
                break
    if need_id:
        return id_list
    ret = [0]*64
    for i in id_list:
        ret[i]=1
    return ret