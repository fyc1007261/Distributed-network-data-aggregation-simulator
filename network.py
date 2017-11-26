
from numpy import *
import random

def mmax(a, b):
    if a > b:
        return a
    else:
        return b


class Network:
    def __init__(self, num=40):
        # initialize an empty network of size num, while no nodes are connected.
        self.size = num
        self.value = (num * [0])[:]
        self.topology = []
        for i in range(num):
            temp = []
            for j in range(num):
                temp.append(0)
            self.topology.append(temp)
        self.generate()

    def neighbors_of(self, i):
        # return a set that contains neighbors of node i.
        s = set()
        for j in range(self.size):
            if self.topology[i][j] == 1 and i != j:
                s.add(j)
        return s

    def num_of_neighbors(self, i):
        # calculate the number of neighbors of one node.
        neighbors = self.neighbors_of(i)
        return len(neighbors)

    def judge_connected(self):
        # judge whether the network is connected
        visited = set()
        visited.add(0) # add node 0 into the set.
        q = [0]
        while len(q) != 0:
            out = q.pop(0)
            nbs = self.neighbors_of(out)
            for node in nbs:
                if not (node in visited):
                    q.append(node)
                    visited.add(node)
        if len(visited) != self.size:
            return False
        else:
            return True

    def generate(self, area=100, dis=30):
        # In a square of area*area, if the distance between 2 nodes <= dis, then connect this 2 nodes.
        while (1):
            nodes = []
            for i in range(self.size):
                x = random.randrange(0, area)
                y = random.randrange(0, area)
                nodes.append([x, y])
            for i in range(self.size):
                for j in range(self.size):
                    if i == j:
                        continue
                    else:
                        distance = (nodes[i][0] - nodes[j][0])**2 + (nodes[i][1] - nodes[j][1])**2
                        if distance <= dis**2:
                            self.add_line(i, j)
            if self.judge_connected():
                return

    def add_line(self, i, j):
        # add a line between node i and node j.
        self.topology[i][j] = 1
        self.topology[j][i] = 1

    def set_data(self, data):
        # set all data while "data" is a list of n data.(n is the size of the network)
        self.value = data[:]

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
                self.topology[i][j] = temp
                self.topology[j][i] = temp

    def calculate_avg(self, max_iter=-1):
        # calculate the average of the network.
        if max_iter == -1:
            max_iter = self.size**2
        temp = self.value[:]
        new = temp[:] # store the value, because values should be update simultaneously.
        for iter in range(max_iter):
            print(temp)
            for i in range(self.size):
                count = 0
                num = 0
                for j in range(self.size):
                    if self.topology[i][j] == 1:
                        count += temp[j] * (1 / (1 + mmax(self.num_of_neighbors(i), self.num_of_neighbors(j))))
                        num += 1/(1+mmax(self.num_of_neighbors(i), self.num_of_neighbors(j)))
                new[i] = (count + temp[i] * (1 - num))
            temp[:] = new[:]
        self.value = temp[:]
