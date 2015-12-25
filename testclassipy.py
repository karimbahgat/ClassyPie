
import classipy as cp

items = [v**2 for v in range(100)]

##cfier = cp.MultiClassifier(items)
##cfier.add_classification("equaltest",
##                       breaks="equal",
##                       fromval=1,
##                       toval=10)
##cfier.add_classification("naturaltest",
##                       breaks="natural",
##                       fromval=1,
##                       toval=10)
##cfier.add_classification("headtailtest",
##                       breaks="headtail",
##                       fromval=1,
##                       toval=10)
##
##for item,info in cfier:
##    print item,info


cfier = cp.Classification(items,
                          breaks="pretty",
                          fromval=1,
                          toval=10)
print "hmm"
print cfier.algo
print cfier.breaks
print cfier.classvalues
for item,classval in cfier:
    print item,classval
