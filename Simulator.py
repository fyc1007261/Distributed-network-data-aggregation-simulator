from network import *
import random


def main():
    size = 66
    net = Network(size)
    data = []
    flags = []
    for i in range(size):
        data.append(i)
    net.set_data(data)
    print(net.pdf_aggregation())

main()