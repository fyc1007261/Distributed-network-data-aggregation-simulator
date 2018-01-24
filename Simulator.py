from network import *
import random


def read_data(file_name):
    f = open(file_name, 'r')
    s = f.readline()
    return eval(s)


def main():
    size = 100
    net = Network(new_top=False, num=size, topo_file="topology.txt")
    data = read_data("data.txt")
    flags = []
    net.set_data(data)
    #print(net.id_based_pdf_aggregation())
    print(net.generic_pdf_consensus(sections=20, sim=True).T[0])
    #print(net.generic_pdf_consensus(sections=40, sim=True).T[0])
    #print(net.generic_pdf_consensus(sections=100, sim=True).T[0])
    # Network 2
    net2 = Network(new_top=False, num=size, topo_file="topology2.txt")
    net2.set_data(data)
    print(net2.generic_pdf_consensus(sections=20, sim=True).T[0])
    plt.show()

def test_diameter():
    net = Network(new_top=True, num=100 , s_area=100, s_dis=15)
    net.save_topology()
    net.find_neighbors()
    b=net.diameter()
    print(b)

test_diameter()
