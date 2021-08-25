
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
        for idx in tqdm(list(range(len(self.tensor['board'])))[0:20000]):
            # if idx == 51:
            #     print(51)
            who_win = 0 if self.tensor['black_chess_num'][idx]>=32 else 1
            if self.tensor['turn'][idx] != who_win:
                continue
            next_pos_id = ask_next_pos(self.tensor['board'][idx],self.tensor['turn'][idx],need_id=True)
            assert self.tensor['next_step_id'][idx] in next_pos_id,"id not in list"
            chessbook = convert_chessbook(self.tensor['turn'][idx],self.tensor['board'][idx])
            chessbook = trans_chessbook_to_input(chessbook)
            label = [0]*64
            
            for i in next_pos_id:
                label[i]=0.5

            label[self.tensor['next_step_id'][idx]] = 1
            # label = torch.Tensor(label)

            
        

            self.dataset['inputs'].append(chessbook)
            self.dataset['labels'].append(label)

        self.dataset['labels'] = torch.Tensor(self.dataset['labels'])
        self.dataset['inputs'] = torch.stack(self.dataset['inputs'],dim = 0)
        self.len = len(self.dataset['labels'])

    def __len__(self):
        return self.len

    def __getitem__(self,index):
        return {key: data[index] for key, data in self.dataset.items()}

    def cuda(self):
        self.dataset['labels'] = self.dataset['labels'].cuda()
        # for idx,i in enumerate(self.dataset['inputs']):
        #     self.dataset['inputs'][idx] = i.cuda()
        self.dataset['inputs'] = self.dataset['inputs'].cuda()

