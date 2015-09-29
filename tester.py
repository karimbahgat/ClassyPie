import classipy as c
from random import randint
import pyagg

vals = [randint(-111,111) for _ in range(1000)]
grph = pyagg.graph.Histogram(vals, 5)
#grph.draw(300,300,background="red").view()

import time
t = time.clock()
for each in c.split(vals, [-77,-33,55]):
  print each
print time.clock()-t



