
from torch.utils.data import Dataset
import torch
import json
from tqdm import tqdm
from utils import *
class reservi_dataset(Dataset):
    def __init__(self,filename):
        self.datasetname = "reservi_dataset"
        self.tensor = None
        print("reading data")
        with open(filename,'r') as file_obj:
            self.tensor = json.load(file_obj)
        self.dataset = {'inputs':[],'labels':[]}
        print("loading dataset")
        for idx in tqdm(list(range(len(self.tensor['board'])))[0:40636]):
            # if idx == 51:
            #     print(51)
            who_win = 0 if self.tensor['black_chess_num'][idx]>=32 else 1
            if self.tensor['turn'][idx] != who_win:
                continue
            if self.tensor['turn'][idx]!=0:
                continue
            next_pos_id = ask_next_pos(self.tensor['board'][idx],self.tensor['turn'][idx],need_id=True)
            
            assert self.tensor['next_step_id'][idx] in next_pos_id,"id not in list"
            label = next_pos_id.index(self.tensor['next_step_id'][idx])
            next_chessbook = []
            for id in next_pos_id:
                next_chessbook.append(get_next_step_board(self.tensor['board'][idx],self.tensor['turn'][idx],id,True))
            next_chessbook = torch.Tensor(next_chessbook)#.long()
            
            self.dataset['inputs'].append(next_chessbook)
            self.dataset['labels'].append(label)
        self.dataset['labels'] = torch.Tensor(self.dataset['labels']).long()
        self.len = len(self.dataset['labels'])

    def __len__(self):
        return self.len

    def __getitem__(self,index):
        return {key: data[index] for key, data in self.dataset.items()}

    def cuda(self):
        self.dataset['labels'] = self.dataset['labels'].cuda()
        for idx,i in enumerate(self.dataset['inputs']):
            self.dataset['inputs'][idx] = i.cuda()

