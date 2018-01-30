
import numpy.random
dataset = numpy.random.normal(size=400)
f = open('data400.txt', 'w')
f.write(str(dataset.tolist()))
f.close()
