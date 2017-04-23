
import classypie as cp

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


cfier = cp.Classifier(items,
                      breaks="pretty",
                      valuestops=[1,30],
                      #start=0,
                      #end=10000
                      )
print "hmm"
print cfier
for item,classval in cfier:
    print item,classval
