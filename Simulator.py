from network import *
import random


def read_data(file_name):
    f = open(file_name, 'r')
    s = f.readline()
    return eval(s)


def size_differs():
    net = Network(new_top=True, num=100, s_dis=20)
    data = read_data("data100.txt")
    net.set_data(data)
    net.generic_pdf_consensus(sections=20, sim=True, max_iter=500, label="N=100")
    # Network 2
    data2 = read_data("data400.txt")
    net2 = Network(new_top=True, num=400, topo_file="topology2.txt",s_area=200 ,s_dis=20)
    net2.set_data(data2)
    net2.generic_pdf_consensus(sections=20, sim=True, max_iter=500, label="N=400")
    plt.xlabel("k")
    plt.ylabel(r"$\varepsilon$")
    plt.show()


def topology_differs():
    size = 100
    data = read_data("data100.txt")
    net = Network(new_top=True, num=size, s_dis=20)
    net.set_data(data)
    net.generic_pdf_consensus(sections=20, sim=True, max_iter=150, label=r"$l=20$")
    print(net.diameter(), net.average_degree())
    net2 = Network(new_top=True, num=size, s_dis=40)
    net2.set_data(data)
    net2.generic_pdf_consensus(sections=20, sim=True, max_iter=150, label=r"$l=40$")
    print(net2.diameter(), net2.average_degree())
    plt.xlabel("k")
    plt.ylabel(r"$\varepsilon$")
    plt.show()

def test_diameter():
    net = Network(new_top=True, num=100, s_area=100, s_dis=20)
    net.save_topology()
    net.find_neighbors()
    b = net.diameter()
    print(b)


size_differs()
topology_differs()
