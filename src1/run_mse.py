from reversi_dataset import reservi_dataset
from torch.utils.data import DataLoader
from model import reversi_model
import torch
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import json
def train(model,dataloader,max_epochs):
    model.train()
    print("begin training")
    epochs = 0
    loss_plt_num = 0
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_list = []
    loss_list_tmp = []
    tmp_len = 240
    put_len = 10
    while (epochs < max_epochs):
        tr_loss = 0.0
        global_step = 0
        epochs += 1

        with tqdm(total=len(dataloader)) as t:
            for step, batch in enumerate(dataloader):
                t.set_description("Epoch {}".format(epochs))
                predict = model(batch['inputs'].cuda())
                label = batch['labels']
                a = [0]*predict.shape[1]
                a[int(label)] = 1
                a = torch.Tensor(a).cuda().unsqueeze(0)
                # print(predict)
                # print(label)
                loss = criterion(predict, a)
                t.set_postfix(loss=loss.item())
                t.update(1)

                # if args.gradient_accumulation_steps > 1:
                #     loss = loss / args.gradient_accumulation_steps
                optimizer.zero_grad()
                loss.backward()
                loss_list_tmp.append(loss.item())
                optimizer.step()
                if (len(loss_list_tmp)) % tmp_len == 0:
                    loss_list.append(np.mean(loss_list_tmp))
                    loss_list_tmp = []

                if (step+1)%(tmp_len*put_len) == 0:
                    loss_plt_num+=1
                    plt.plot(loss_list)
                    plt.savefig('pic/mse/loss{}.jpg'.format(loss_plt_num))

    loss_plt_num+=1
    plt.plot(loss_list)
    plt.savefig('pic/mse/loss{}.jpg'.format(loss_plt_num))

    with open('pic/loss.json','w') as file_obj:
        json.dump(loss_list,file_obj)

def test(model,dataloader):
    model.eval()
    print("begin testing")
    epochs = 0
    loss_plt_num = 0
    loss_list = []
    loss_list_tmp = []
    true = 0
    all = 0
    total_chose =  0
    tmp_len = 600
    put_len = 50
    criterion = torch.nn.CrossEntropyLoss()
    with torch.no_grad():
        with tqdm(total=len(dataloader)) as t:
            for step, batch in enumerate(dataloader):
                t.set_description("Epoch {}".format(epochs))
                predict = model(batch['inputs'].cuda())
                predict_label = predict[0].argmax() 
                label = batch['labels']
                if predict_label== label:
                    true+=1
                all +=1
                total_chose+=len(predict[0])
                # print(predict)
                # print(label)
                loss = criterion(predict, label)
                t.set_postfix(loss=loss.item())
                t.update(1)

                # if args.gradient_accumulation_steps > 1:
                #     loss = loss / args.gradient_accumulation_steps
                loss_list_tmp.append(loss.item())

                if (len(loss_list_tmp)) % tmp_len == 0:
                    loss_list.append(np.mean(loss_list_tmp))
                    loss_list_tmp = []

                if (step+1)%(tmp_len*put_len) == 0:
                    loss_plt_num+=1
                    plt.plot(loss_list)
                    plt.savefig('pic/test/loss{}.jpg'.format(loss_plt_num))

    print(true,all,total_chose,true/all)

batch_size = 1
max_epochs = 1
data_save_path = 'param/param128_2h_2layer_40636_mse.pth'
datafilename = 'rewth/2001-2015_dataset_board.json'


model = reversi_model()
model.load_state_dict(torch.load(data_save_path))
model.cuda()

dataset = reservi_dataset(datafilename)
dataset.cuda()
train_dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

train(model,train_dataloader,max_epochs=max_epochs)
torch.save(model.state_dict(),data_save_path)

test(model,test_dataloader)
 
print("end")