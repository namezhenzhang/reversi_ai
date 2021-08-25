import torch
import torch.nn.functional as F

class reversi_model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.h = 128
        
        self.embeding = torch.nn.Parameter(torch.randn(self.h,65), requires_grad=True)
        self.w_k11 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q11 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v11 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k12 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q12 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v12 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        

        self.linear1 = torch.nn.Parameter(torch.randn(2*self.h,self.h), requires_grad=True)#将多头合并为一个hidden

        self.w_k21 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q21 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v21 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k22 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q22 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v22 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.linear2 = torch.nn.Parameter(torch.randn(2*self.h,self.h), requires_grad=True)
        
        self.linear3 = torch.nn.Parameter(torch.randn(self.h,self.h//2), requires_grad=True)

        self.linear4 = torch.nn.Parameter(torch.randn(self.h//2,1), requires_grad=True)
        
    def forward(self,inputs):
        inputs = inputs[0]
        outputs = []
        append_x = torch.Tensor([1]).cuda()
        for x_ in inputs:
            x = torch.cat((x_,append_x))
            y = self.embeding * x

            k11 = self.w_k11 @ y
            q11 = self.w_q11 @ y
            v11 = self.w_v11 @ y
            kq11 = k11.T @ q11
            kq_sm11 = F.softmax(kq11,dim = 1)
            att11 = kq_sm11 @ v11.T

            k12 = self.w_k12 @ y
            q12 = self.w_q12 @ y
            v12 = self.w_v12 @ y
            kq12 = k12.T @ q12
            kq_sm12 = F.softmax(kq12,dim = 1)
            att12 = kq_sm12 @ v12.T
            # print(att12.shape)
            y = torch.cat((att11,att12),dim = 1)
            y = torch.tanh(y @ self.linear1)

            y = y.T

            k21 = self.w_k21 @ y
            q21 = self.w_q21 @ y
            v21 = self.w_v21 @ y
            kq21 = k21.T @ q21
            kq_sm21 = F.softmax(kq21,dim = 1)
            att21 = kq_sm21 @ v21.T
            # print(att21.shape)
            k22 = self.w_k22 @ y
            q22 = self.w_q22 @ y
            v22 = self.w_v22 @ y
            kq22 = k22.T @ q22
            kq_sm22 = F.softmax(kq22,dim = 1)
            att22 = kq_sm22 @ v22.T

            y = torch.cat((att21,att22),dim = 1)
            # print(y.shape)
            y = torch.tanh(y @ self.linear2)[64] 
            y = torch.tanh(y @ self.linear3)
            score = y @ self.linear4

            # print(att.shape)
            # tag = att22[64]
            # score = F.relu((F.relu(tag @ self.linear1)) @ self.linear2) @ self.linear3
            # score = torch.sigmoid(score)
            outputs.append(score)

        outputs = torch.cat(outputs).unsqueeze(0)
        return outputs