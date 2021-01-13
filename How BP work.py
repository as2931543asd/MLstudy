import math
import random
# 垃圾网络 不过理解了bp是怎么做的了


def sigmoid(x):
    return 1/(1+math.exp(-x))


class FullCollectionNetwork:
    def __init__(self):
        self.w1, self.w2, self.w3, self.w4 = 1, 1, 1, 1
        self.w5, self.w6, self.w7, self.w8 = 1, 1, 1, 1
        self.net_h1, self.net_h2, self.net_h3, self.net_h4 = 0, 0, 0, 0
        self.out_h1, self.out_h2, self.out_h3, self.out_h4 = 0, 0, 0, 0
        self.b1, self.b2, self.b3, self.b4 = 0, 0, 0, 0
        self.output = 0
        self.input = 0
        self.lose = 0
        self.target = 0

    def loss(self):
        self.lose = (self.output-self.target)**2/2

    def forward(self):
        self.net_h1 = self.w1 * self.input + self.b1
        self.net_h2 = self.w2 * self.input + self.b2
        self.net_h3 = self.w3 * self.input + self.b3
        self.net_h4 = self.w4 * self.input + self.b4
        self.out_h1 = sigmoid(self.net_h1)
        self.out_h2 = sigmoid(self.net_h2)
        self.out_h3 = sigmoid(self.net_h3)
        self.out_h4 = sigmoid(self.net_h4)
        self.output = self.w5*self.out_h1+self.w6*self.out_h2+self.w7*self.out_h3+self.w8*self.out_h4

    def backward(self):
        lr = 0.01
        loss_output = self.output-self.target
        output_w5 = self.out_h1
        output_w6 = self.out_h2
        output_w7 = self.out_h3
        output_w8 = self.out_h4
        out_h1_net_h1 = self.net_h1 * (1 - self.net_h1)
        out_h2_net_h2 = self.net_h2 * (1 - self.net_h2)
        out_h3_net_h3 = self.net_h3 * (1 - self.net_h3)
        out_h4_net_h4 = self.net_h4 * (1 - self.net_h4)
        self.w5 = self.w5 - lr*output_w5 * loss_output
        self.w6 = self.w6 - lr*output_w6 * loss_output
        self.w7 = self.w7 - lr*output_w7 * loss_output
        self.w8 = self.w8 - lr*output_w8 * loss_output
        self.w1 = self.w1 - lr*loss_output * out_h1_net_h1 * self.input
        self.w2 = self.w2 - lr*loss_output * out_h2_net_h2 * self.input
        self.w3 = self.w3 - lr*loss_output * out_h3_net_h3 * self.input
        self.w4 = self.w4 - lr*loss_output * out_h4_net_h4 * self.input
        # print(loss_output)


if __name__ == '__main__':
    Network = FullCollectionNetwork()
    for i in range(10000):
        k = random.uniform(1, 5)
        Network.input = k
        Network.target = k**2
        Network.forward()
        Network.loss()
        print('input=', Network.input, 'output=', Network.output, 'Loss=', Network.lose)
        Network.backward()

