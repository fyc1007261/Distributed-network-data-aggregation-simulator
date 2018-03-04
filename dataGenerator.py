
import numpy.random
dataset = numpy.random.normal(size=40)
f = open('data40.txt', 'w')
f.write(str(dataset.tolist()))
f.close()

