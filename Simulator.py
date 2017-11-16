import random
from numpy import *


def mmax(a, b):
    if a > b:
        return a
    else:
        return b


class Network:
    def __init__(self, num):
        #initialize an empty network of size num, while no nodes are connected.
        self.size = num
        self.info = (num * [0])[:]
        self.nodes = []
        for i in range(num):
            temp = []
            for j in range(num):
                temp.append(0)
            self.nodes.append(temp)

    def add_line(self, i, j):
        #add a line between node i and node j.
        self.nodes[i][j] = 1
        self.nodes[j][i] = 1

    def set(self, data):
        #set all data while "data" is a list of n data.(n is the size of the network)
        self.info = data[:]

    def rd(self):
        # generate a random topology of the network.
        # it CANNOT make sure that every node is connected.
        for i in range(self.size):
            for j in range(i + 1, self.size):
                temp = random.random()
                if temp > 0.5:
                    temp = 1
                else:
                    temp = 0
                self.nodes[i][j] = temp
                self.nodes[j][i] = temp

    def calculateAvg(self):
        #calculate the average of the network.
        temp = self.info[:]
        for i in range(self.size):
            count = 0
            num = 0
            for j in range(self.size):
                if self.nodes[i][j] == 1:
                    count += self.info[j] * (1/(1+mmax(self.num_of_neighbors(i), self.num_of_neighbors(j))))
                    num += 1/(1+mmax(self.num_of_neighbors(i), self.num_of_neighbors(j)))
            temp[i] = (count + self.info[i] * (1 - num))
        self.info = temp[:]

    def num_of_neighbors(self, i):
        #calculate the number of neighbors of one node.
        count = 0
        for j in range(self.size):
            if self.nodes[i][j] == 1 and i != j:
                count += 1
        return count

    def output(self):
        # print(self.nodes)
        print(self.info)


# def main():
#     graph = Network(5)
#     graph.set([12132, 2123123, 321415, 44, 5555])
#     graph.add_line(0, 1)
#     graph.add_line(1, 2)
#     graph.add_line(1, 3)
#     graph.add_line(0, 4)
#     for i in range(100):
#         graph.output()
#         #graph.rd()
#         graph.calculateAvg()
#
#
# main()