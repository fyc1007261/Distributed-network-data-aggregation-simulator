from network import *
import random


def main():
    size = 66
    net = Network(True, size)
    data = []
    flags = []
    for i in range(size):
        data.append(i)
    net.set_data(data)
    net.save_topology()
    print(net.pdf_aggregation())


main()
