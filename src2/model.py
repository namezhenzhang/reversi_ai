import torch
import torch.nn.functional as F

class reversi_model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.h = 512

        self.dropout = torch.nn.Dropout(p=0.1)

        self.embeding = torch.nn.Parameter(torch.randn(self.h,65), requires_grad=True)
        self.w_k11 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q11 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v11 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k12 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q12 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v12 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k13 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q13 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v13 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        

        self.linear1 = torch.nn.Parameter(torch.randn(3*self.h,self.h), requires_grad=True)#将多头合并为一个hidden

        self.w_k21 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q21 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v21 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k22 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q22 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v22 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k23 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q23 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v23 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.linear2 = torch.nn.Parameter(torch.randn(3*self.h,self.h), requires_grad=True)#将多头合并为一个hidden

        self.w_k31 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q31 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v31 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k32 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q32 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v32 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)

        self.w_k33 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_q33 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)
        self.w_v33 = torch.nn.Parameter(torch.randn(self.h,self.h), requires_grad=True)


        self.linear3 = torch.nn.Parameter(torch.randn(3*self.h,2*self.h), requires_grad=True)
        
        self.linear4 = torch.nn.Parameter(torch.randn(2*self.h,self.h), requires_grad=True)

        self.linear5 = torch.nn.Parameter(torch.randn(self.h,64), requires_grad=True)
        
    def forward(self,inputs):
        inputs = inputs[0]
        outputs = []
        append_x = torch.Tensor([1]).cuda()
        # for x_ in [inputs]:
        x_ = inputs
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

        k13 = self.w_k13 @ y
        q13 = self.w_q13 @ y
        v13 = self.w_v13 @ y
        kq13 = k13.T @ q13
        kq_sm13 = F.softmax(kq13,dim = 1)
        att13 = kq_sm13 @ v13.T
        # print(att12.shape)
        y = torch.cat((att11,att12,att13),dim = 1)
        y = torch.relu(y @ self.linear1)

        y = y.T

        k21 = self.w_k21 @ y
        q21 = self.w_q21 @ y
        v21 = self.w_v21 @ y
        kq21 = k21.T @ q21
        kq_sm21 = F.softmax(kq21,dim = 1)
        att21 = kq_sm21 @ v21.T

        k22 = self.w_k22 @ y
        q22 = self.w_q22 @ y
        v22 = self.w_v22 @ y
        kq22 = k22.T @ q22
        kq_sm22 = F.softmax(kq22,dim = 1)
        att22 = kq_sm22 @ v22.T

        k23 = self.w_k23 @ y
        q23 = self.w_q23 @ y
        v23 = self.w_v23 @ y
        kq23 = k23.T @ q23
        kq_sm23 = F.softmax(kq23,dim = 1)
        att23 = kq_sm23 @ v23.T
        # print(att12.shape)
        y = torch.cat((att11,att12,att23),dim = 1)
        y = torch.relu(y @ self.linear2)

        y = y.T

        k31 = self.w_k31 @ y
        q31 = self.w_q31 @ y
        v31 = self.w_v31 @ y
        kq31 = k31.T @ q31
        kq_sm31 = F.softmax(kq31,dim = 1)
        att31 = kq_sm31 @ v31.T

        k32 = self.w_k32 @ y
        q32 = self.w_q32 @ y
        v32 = self.w_v32 @ y
        kq32 = k32.T @ q32
        kq_sm32 = F.softmax(kq32,dim = 1)
        att32 = kq_sm32 @ v32.T

        k33 = self.w_k33 @ y
        q33 = self.w_q33 @ y
        v33 = self.w_v33 @ y
        kq33 = k33.T @ q33
        kq_sm33 = F.softmax(kq33,dim = 1)
        att33 = kq_sm33 @ v33.T
        # print(att12.shape)
        y = torch.cat((att11,att12,att33),dim = 1)
        y = torch.relu(y @ self.linear3)[64]
        y = self.dropout(y)
        y = torch.tanh(y @ self.linear4)
        score = y @ self.linear5
        return score.unsqueeze(0)


            # print(att.shape)
            # tag = att22[64]
            # score = F.relu((F.relu(tag @ self.linear1)) @ self.linear2) @ self.linear3
            # score = torch.sigmoid(score)
            # outputs.append(score)

        outputs = torch.cat(outputs).unsqueeze(0)
        return outputs