import classypie as c
from random import randint

vals = [-500000+_**2 for _ in range(-100,1000)]

print("\nbreaks:")
for algo in ("equal","quantile","stdev","pretty","natural","headtail"):
  print(algo, c.breaks(vals, algo))

print("\nsplit:")
for algo in ("equal","quantile","stdev","pretty","natural","headtail"):
  print(algo)
  for valrang,members in c.split(vals, algo):
    print(valrang,len(members))

print("\nmembership:")
for valrang,members in c.membership(vals, [(-10000,100000),(-10000,0),(0,1000000)]):
  print(valrang,len(members))


fdsf


##import pyagg
##
##grph = pyagg.graph.Histogram(vals, 5)
##grph.draw(300,300,background="red").view()
##
##grph = pyagg.graph.BarChart()
##barlabels,bars = zip(*c.split(vals, "headtail"))
##bars = [len(vals) for vals in bars]
##barlabels = [str(rng) for rng in barlabels]
##grph.add_category("bleh", barlabels=barlabels, bars=bars)
##grph.draw(300,300,background="red").view()
##
##print c.breaks(vals, "headtail")
##
##import time
##t = time.clock()
##for each in c.split(vals, "headtail"): #[-77,-33,55]):
##  print each
##print time.clock()-t



