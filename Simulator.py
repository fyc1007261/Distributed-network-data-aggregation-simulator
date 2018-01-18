from network import *
import random


def read_data(name):
    f = open(name, 'r')
    s = f.readline()
    return eval(s)


def main():
    size = 166
    net = Network(size)
    data = []
    size = 100
    net = Network(True, size)
    data = read_data("data.txt")
    flags = []
    net.set_data(data)
    print(net.calculate_avg(net.value))
    #print(net.pdf_aggregation())
    print(multiply(net.pdf_aggregation_without_id(10)[:,0], size))
    net.save_topology()
    print(net.pdf_aggregation())


main()
