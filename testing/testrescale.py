
import classypie as cp

vals = range(16)

for old,new in cp.rescale(vals, 0, 100):
    print old,new

for old,new in cp.rescale(vals, 100, 0):
    print old,new

for old,new in cp.rescale(vals, (0,100,0), (100,0,100)):
    print old,new

for old,new in cp.rescale(vals, (100,0,100), (0,100,0)):
    print old,new
