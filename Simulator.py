from network import *
import random


def main():
    size = 166
    net = Network(size)
    data = []
    flags = []
    for i in range(size):
        data.append(i)
    net.set_data(data)
    print(net.calculate_avg(net.value))
    #print(net.pdf_aggregation())
    print(multiply(net.pdf_aggregation_without_id(10)[:,0], size))

main()