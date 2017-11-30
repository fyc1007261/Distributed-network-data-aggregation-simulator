from numpy import *
import matplotlib.pyplot as plt
import random
import copy


def mmax(a, b):
    if a > b:
        return a
    else:
        return b


def find_extreme(my_set, mode="max"):
    if mode != "max" and mode != "min":
        print("Wrong parameter in function find_extreme.")
    result = my_set[0]
    for item in my_set:
        if mode == "max":
            if result < item:
                result = item
        if mode == "min":
            if result > item:
                result = item
    return result


class Network:
    def __init__(self, num=40):
        # initialize an empty network of size num, while no nodes are connected.
        self.size = num  # size of the network
        self.value = mat((num * [0])[:])  # initial value held by nodes
        self.topology = []
        self.neighbors = [] # a list of sets. Neighbors of each node are in the sets.
        # generate the topology
        for i in range(num):
            temp = []
            for j in range(num):
                temp.append(0)
            self.topology.append(temp)
        self.generate()
        self.weight_matrix = mat(self.calculate_weight_matrix())

    def find_neighbors(self):
        self.neighbors = []
        for i in range(self.size):
            s = set()
            for j in range(self.size):
                if self.topology[i][j] == 1 and i != j:
                    s.add(j)
            self.neighbors.append(s)

    def neighbors_of(self, i):
        # return a set that contains neighbors of node i.
        return self.neighbors[i]

    def num_of_neighbors(self, i):
        # calculate the number of neighbors of one node.
        neighbors = self.neighbors_of(i)
        return len(neighbors)

    def judge_connected(self):
        # judge whether the network is connected
        visited = set()
        visited.add(0)  # add node 0 into the set.
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
        while 1:
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
            self.find_neighbors()
            if self.judge_connected():
                break

    def add_line(self, i, j):
        # add a line between node i and node j.
        self.topology[i][j] = 1
        self.topology[j][i] = 1

    def set_data(self, data):
        # set all data while "data" is a list of n data.(n is the size of the network)
        self.value = mat(data[:])

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

    def calculate_weight_matrix(self):
        result = []
        for i in range(self.size):
            temp = []
            for j in range(self.size):
                temp.append(0)
            result.append(temp)
        for i in range(self.size):
            num = 0
            for j in range(self.size):
                if self.topology[i][j] == 1:
                    result[i][j] = (1 / (1 + mmax(self.num_of_neighbors(i), self.num_of_neighbors(j))))
                    num += result[i][j]
            result[i][i] = 1 - num
        return result

    def calculate_avg(self, max_iter=-1):
        # calculate the average of the network.
        if max_iter == -1:
            max_iter = self.size
        temp = self.value[:]
        new = temp[:]  # store the value, because values should be update simultaneously.
        for iter in range(max_iter):
            self.value = self.value * self.weight_matrix

    def m_consensus(self, flags, mode="max", iter=0):
        values = self.value
        # error report.
        if mode != "max" and mode != "min":
            print("Invalid parameters!")
            return
        multi = 1
        if mode == "min":
            multi = -1
        # set number of iterations by default.
        if iter == 0:
            iter = self.size-1
        # initialize IDs in nodes.
        id_value = []
        for i in range(self.size):
            id_value.append(i)
        # start the iterations
        for i in range(iter):
            temp = copy.deepcopy(values)
            temp_id = copy.deepcopy(id_value)
            for node in range(self.size):
                neighbors = self.neighbors_of(node)
                for nei in neighbors:
                    if flags[nei] == 0:  # no data in this neighbor.
                        continue
                    if flags[node] == 0:  # info in node has been deleted.
                        if flags[nei] == 1:
                            temp[0, node] = values[0,nei]
                            flags[node] = 1
                            temp_id[node] = id_value[nei]
                        else:
                            continue
                    elif values[0, nei] == temp[0, node]:  # values equal, compare ID
                        if multi*id_value[nei] > multi*temp_id[node]:
                            temp_id[node] = id_value[nei]
                    elif multi*values[0, nei] > multi*temp[0, node]:
                        temp[0, node] = values[0, nei]
                        temp_id[node] = id_value[nei]
            id_value = copy.deepcopy(temp_id)
            values = copy.deepcopy(temp)
        self.value = values
        # delete the data in max(min) nodes.
        for i in range(self.size):
            if id_value[i] == i:
                flags[i] = 0
        return flags


