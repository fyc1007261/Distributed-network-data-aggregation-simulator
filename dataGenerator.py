import random
mylist = []
for i in range(98):
    rd = random.random()
    rd *= 1000
    mylist.append(rd)
mylist.append(0)
mylist.append(1000)
f = open('data.txt', 'w')
f.write(str(mylist))
f.close()
