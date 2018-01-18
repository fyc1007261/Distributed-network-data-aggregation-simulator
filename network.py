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
    def __init__(self, new=True, num=40):
        # initialize an empty network of size num, while no nodes are connected.
        self.size = num  # size of the network
        self.value = mat((num * [0])[:])  # initial value held by nodes
        self.topology = []
        self.neighbors = [] # a list of sets. Neighbors of each node are in the sets.
        # generate the topology
        # generate an empty matrix
        for i in range(num):
            temp = []
            for j in range(num):
                temp.append(0)
            self.topology.append(temp)
        if new:
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

    def save_topology(self):
        file_name = "topology.txt"
        f = open(file_name, 'w')
        size = len(self.topology)
        for i in range(size):
            f.write(str(self.topology[i])+'\n')
        f.close()

    def load_topology(self):
        file_name = "topology.txt"
        f = open(file_name, 'r')
        i = 0
        while 1:
            s = f.readline()
            if s == "":
                break
            self.topology[i] = eval(s)
            i += 1
        f.close()

    def add_line(self, i, j):
        # add a line between node i and node j.
        self.topology[i][j] = 1
        self.topology[j][i] = 1

    def set_data(self, data):
        # set all data while "data" is a list of n data.(n is the size of the network)
        self.value = (mat(data[:]))

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

    def calculate_avg(self, value_m, max_iter=-1):
        # calculate the average of the network.
        value_m = value_m.T
        if max_iter == -1:
            max_iter = self.size
        for iter in range(max_iter):
            value_m = (self.weight_matrix * value_m)
        return value_m.T

    def m_consensus(self, flags, iter=0):
        max_values = copy.deepcopy(self.value)
        min_values = copy.deepcopy(self.value)
        # set number of iterations by default.
        if iter == 0:
            iter = self.size//2 -1
        # initialize IDs in nodes.
        max_id_value = []
        min_id_value = []
        for i in range(self.size):
            max_id_value.append(i)
            min_id_value.append(i)
        # start the iterations
        for i in range(iter):
            temp_max = copy.deepcopy(max_values)
            temp_min = copy.deepcopy(min_values)
            temp_max_id = copy.deepcopy(max_id_value)
            temp_min_id = copy.deepcopy(min_id_value)
            temp_flags = copy.deepcopy(flags)
            for node in range(self.size):
                neighbors = self.neighbors_of(node)
                for nei in neighbors:
                    # max consensus
                    if flags[nei][1] == 0:  # no max in this neighbor.
                        pass
                    elif temp_flags[node][1] == 0:  # info in node has been deleted.
                        if flags[nei][1] == 1:
                            temp_max[0, node] = max_values[0, nei]
                            temp_flags[node][1] = 1
                            temp_max_id[node] = max_id_value[nei]
                        else:
                            continue
                    elif max_values[0, nei] == temp_max[0, node]:  # values equal, compare ID
                        if max_id_value[nei] > temp_max_id[node]:
                            temp_max_id[node] = max_id_value[nei]
                    elif max_values[0, nei] > temp_max[0, node]:
                        temp_max[0, node] = max_values[0, nei]
                        temp_max_id[node] = max_id_value[nei]
                    # min consensus
                    if flags[nei][0] == 0:  # no max in this neighbor.
                        pass
                    elif temp_flags[node][0] == 0:  # info in node has been deleted.
                        if flags[nei][0] == 1:
                            temp_min[0, node] = min_values[0, nei]
                            temp_flags[node][0] = 1
                            temp_min_id[node] = min_id_value[nei]
                        else:
                            continue
                    elif min_values[0, nei] == temp_min[0, node]:  # values equal, compare ID
                        if min_id_value[nei] < temp_min_id[node]:
                            temp_min_id[node] = min_id_value[nei]
                    elif min_values[0, nei] < temp_min[0, node]:
                        temp_min[0, node] = min_values[0, nei]
                        temp_min_id[node] = min_id_value[nei]
            max_id_value = copy.deepcopy(temp_max_id)
            min_id_value = copy.deepcopy(temp_min_id)
            max_values = copy.deepcopy(temp_max)
            min_values = copy.deepcopy(temp_min)
        # delete the data in max(min) nodes.
        for i in range(self.size):
            if min_id_value[i] == i:
                flags[i][0] = 0
            if max_id_value[i] == i:
                flags[i][1] = 0
        return max_values, min_values, flags

    def check_flags(self, flags):
        # check whether data in all nodes are used.
        for i in range(self.size):
            if flags[i][0] == 1 and flags[i][1] == 1:
                return False
        else:
            return True

    def pdf_aggregation(self, sections=10, max_iter=-1):
        # initialize max_iter
        if max_iter == -1:
            max_iter = self.size-1
        # initialize pdf in each nodes.
        pdf = ([0] * sections)[:]
        # initialize flags
        flags = []
        for i in range(self.size):
            flags.append([1, 1])
        # start aggregating
        # do the 1st iteration to gain the max and min of the network in order to divide the sections.
        max_values, min_values, flags = self.m_consensus(flags)
        max_value = max_values[0, 0]
        min_value = min_values[0, 0]
        min_all = min_value
        pdf[0] += 1
        pdf[-1] += 1
        v_range = max_value - min_value
        ran = self.size//2 - 1
        for i in range(ran):
            max_values, min_values, flags = self.m_consensus(flags)
            max_value = max_values[0, 0]
            min_value = min_values[0, 0]
            max_pos = int((max_value - min_all) / (v_range / sections))
            min_pos = int((min_value - min_all) / (v_range / sections))
            if max_pos >= sections:
                max_pos = -1
            pdf[max_pos] += 1
            pdf[min_pos] += 1
        return multiply(pdf, 1/self.size)

    def pdf_aggregation_without_id(self, sections=10, max_iter=-1):
        # initialize max_iter
        if max_iter == -1:
            max_iter = self.size
        # initialize flags
        flags = []
        for i in range(self.size):
            flags.append([1, 1])
        # do the 1st iteration to gain the max and min of the network in order to divide the sections.
        max_values, min_values, flags = self.m_consensus(flags)
        max_value = max_values[0, 0]
        min_value = min_values[0, 0]
        v_range = max_value - min_value
        # initialize pdf in each nodes.
        pdf = []
        for i in range(self.size):
            temp = []
            position = int((self.value[0, i] - min_value) / (v_range / sections))
            if position >= sections:
                position = -1
            for j in range(sections):
                temp.append(0)
            temp[position] = 1
            pdf.append(temp)

         #start aggregation
        pdf = (mat(pdf)).T
        for iter in range(max_iter):
            pdf = self.calculate_avg(pdf)
        return pdf




