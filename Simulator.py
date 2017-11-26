from network import *


def main():
    size = 10
    net = Network(size)
    data = []
    for i in range(size):
        data.append(i)
    net.set_data(data)
    net.calculate_avg()
    print(net.value)
    print(net.topology)

main()