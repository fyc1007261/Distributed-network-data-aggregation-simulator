from network import *
import random

def main():
    size = 66
    net = Network(size)
    data = []
    flags = []
    for i in range(size):
        data.append(random.randrange(1, 99))
        flags.append(1)
    data[3] = -999
    net.set_data(data)
    net.m_consensus(flags,"min")

main()