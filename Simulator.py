from network import *
import random


def read_data(name):
    f = open(name, 'r')
    s = f.readline()
    return eval(s)


def main():
    size = 100
    net = Network(True, size)
    data = read_data("data.txt")
    flags = []
    net.set_data(data)
    net.save_topology()
    print(net.pdf_aggregation())


main()
