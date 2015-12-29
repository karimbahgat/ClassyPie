
from __future__ import division
from . import _breaks
import itertools
import math


##class MultiClassifier(object):
##
##    # NOTE: Maybe not the fastest to run find_class on each value
##    # maybe instead run split() for each classification and zip them
##    # yielding each value and its (fastly calculated) classnum for each
##    # iterate also to next classval at each new classnum
##    # maybe also cache results
##    # ...
##
##    def __init__(self, items):
##        self.items = items
##        self.classifications = dict()
##
##    def add_classification(self, id, breaks, fromval, toval, key=None, **kwargs):
##        if isinstance(breaks, bytes):
##            algo = breaks
##            breaks = None
##            
##        else:
##            algo = "custom"
##            breaks = breaks
##            
##        instruct = dict(algo=algo,
##                        breaks=breaks,
##                        fromval=fromval,
##                        toval=toval,
##                        key=key,
##                        kwargs=kwargs)
##        
##        self.classifications[id] = instruct
##
##    def classify(self, id):
##        # force update/calculate breaks and class values
##        # mostly used internally, though can be used to recalculate
##        instruct = self.classifications[id]
##        if instruct["algo"] != "custom":
##            instruct["breaks"] = breaks(items=self.items,
##                                        algorithm=instruct["algo"],
##                                        key=instruct["key"],
##                                        **instruct["kwargs"])
##            
##        instruct["classvalues"] = class_values(len(instruct["breaks"])-1, # -1 because break values include edgevalues so will be one more in length
##                                               instruct["fromval"],
##                                               instruct["toval"])
##
##    def __iter__(self):
##        # first process any noncalculated classifications
##        for id,instruct in self.classifications.items():
##            if "classvalues" not in instruct:
##                self.classify(id)
##
##        # loop and yield items along with their classnum and classvalue
##        for item in self.items:
##            info = dict()
##            for id,instruct in self.classifications.items():
##                if instruct["key"]:
##                    val = instruct["key"](item)
##                else:
##                    val = item
##                classnum,valrange = find_class(val, instruct["breaks"])
##                classval = instruct["classvalues"][classnum-1]
##                info[id] = classval
##            yield item,info


class Classifier(object):
    # probably replace instead of multiclassifier, one for each classification instead of multi
    # ALSO, maybe allow unique categorization and maybe membership too

    def __init__(self, items, breaks, valuestops, key=None, **kwargs):
        self.items = items
        
        if isinstance(breaks, bytes):
            algo = breaks
            breaks = None
            
        else:
            algo = "custom"
            breaks = breaks
            
        self.algo = algo
        self.breaks = breaks
        self.valuestops = valuestops
        self.key = key
        self.kwargs = kwargs
        self.classvalues = None

        self.update()

    def __repr__(self):
        import pprint
        metadict = dict(algo=self.algo,
                        breaks=self.breaks,
                        classvalues=self.classvalues)
        return "Classifier object:\n" + pprint.pformat(metadict, indent=4)

    def update(self):
        # force update/calculate breaks and class values
        # mostly used internally, though can be used to recalculate
        if self.algo == "unique":
            self.classvalues = self.valuestops

        else:
            if self.algo != "custom":
                self.breaks = breaks(items=self.items,
                                    algorithm=self.algo,
                                    key=self.key,
                                    **self.kwargs)
            self.classvalues = class_values(len(self.breaks)-1, # -1 because break values include edgevalues so will be one more in length
                                           self.valuestops)

    def __iter__(self):
        # loop and yield items along with their classnum and classvalue
        
        if self.algo == "unique":
            # create eternal iterator over classvalues
            def classvalgen ():
                while True:
                    for classval in self.classvalues:
                        yield classval
            classvalgen = classvalgen()
            for uid,subitems in unique(self.items, key=self.key):
                classval = next(classvalgen)
                for item in subitems:
                    yield item,classval

        else:
            for classnum,(valrange,subitems) in enumerate(split(self.items, self.breaks, key=self.key, **self.kwargs)):
                classval = self.classvalues[classnum]
                for item in subitems:
                    yield item,classval


################################
            

def find_class(value, breaks):
    """
    Given a set of breakpoints, calculate which two breakpoints an input
    value is located between, returning the class number (1 as the first class)
    and the two enclosing breakpoint values. The breakpoints must include the maximum
    and minimum possible value. 
    """
    
    prevbrk = breaks[0]
    classnum = 1
    for nextbrk in breaks[1:]:
        if value <= nextbrk:
            return classnum, (prevbrk,nextbrk)
        prevbrk = nextbrk
        classnum += 1
    else:
        raise Exception("Value was not within the range of the break points")

def class_values(classes, valuestops):
    """
    Return x number of class values linearly interpolated
    between a minimum and maximum value.

    - classes: Number of classes values to return. 
    - valuestops: can be either a single number or sequences of numbers
        where a classvalue will be interpolated for each sequence number,
        and so all sequences must be equally long. Thus, specifying the
        valuestops as rgb color tuples will create interpolated color gradients.
    """
    # special case
    if classes <= 1:
        raise Exception("Number of classes must be higher than 1")
    if len(valuestops) < 2:
        raise Exception("There must be at least two items in valuestops for interpolating between")

    def _lerp(val, oldfrom, oldto, newfrom, newto):
        oldrange = oldto - oldfrom
        relval = (val - oldfrom) / float(oldrange)
        newrange = newto - newfrom
        newval = newfrom + newrange * relval
        return newval

    # determine appropriate interp func for either sequenes or single values
    
    # ALMOST THERE, JUST SLIGHTLY FUNKY INTERPOLATION NEEDING FIXING
    # ...
    
    if all(hasattr(valstop, "__iter__") for valstop in valuestops):
        _len = len(valuestops[0])
        if any(len(valstop) != _len for valstop in valuestops):
            raise Exception("If valuestops are sequences they must all have the same length")
        def _interpfunc(val):
            relindex = _lerp(classnum, 0, classes-1, 0, len(valuestops)-1)
            fromval = valuestops[int(math.floor(relindex))]
            toval = valuestops[int(math.ceil(relindex))]
            classval = [_lerp(relindex, 0, len(valuestops)-1, ifromval, itoval)
                        for ifromval,itoval in zip(fromval,toval)]
            return classval
    else:
        def _interpfunc(classnum):
            relindex = _lerp(classnum, 0, classes-1, 0, len(valuestops)-1)
            fromval = valuestops[int(math.floor(relindex))]
            toval = valuestops[int(math.ceil(relindex))]
            classval = _lerp(relindex, 0, len(valuestops)-1, fromval, toval)
            return classval
    
    # perform
    classvalues = []
    for classnum in range(classes):
        classval = _interpfunc(classnum)
        classvalues.append(classval)

    return classvalues

def breaks(items, algorithm, key=None, **kwargs):
    """
    Only get the break points, including the start and endpoint.
    """
    # sort by key
    if key:
        items = sorted(items, key=key)
        values = [key(item) for item in items]
    else:
        values = items = sorted(items)
        
    # get breaks
    func = _breaks.__dict__[algorithm]
    breaks = func(values, **kwargs)
    
    return breaks

def split(items, breaks, key=None, **kwargs):
    """
    Splits a list of items into n non-overlapping classes based on the
    specified algorithm. Values are either the items themselves or
    a value extracted from the item using the key function. 

    Arguments:

    - **items**: The list of items or values to classify.
    - **breaks**: List of custom break values or the name of the algorithm to use.
        Valid names are:
        - histogram (alias for equal)
        - equal
        - quantile
        - pretty
        - stdev
        - natural
        - headtail
    - **key** (optional): Function used to extract value from each item, defaults to None. 
    - **classes** (optional): The number of classes to group the items into.
    - more...

    Returns:

    - All the input items reorganized into the groups/classes that they belong to,
    as a list of lists of items.
    """

    # sort and get key
    if key:
        items = sorted(items, key=key)
        values = [key(item) for item in items]
    else:
        key = lambda x: x
        values = items = sorted(items)

    # if not custom specified, get break values from algorithm name
    if isinstance(breaks, bytes):
        func = _breaks.__dict__[breaks]
        breaks = func(values, **kwargs)
    else:
        # custom specified breakpoints, ensure endpoints are included
        if breaks[0] != values[0]: breaks.insert(0, values[0])
        if breaks[-1] != values[-1]: breaks.append(values[-1])

    breaks_gen = (brk for brk in breaks)
    loopdict = dict()
    loopdict["prevbrk"] = next(breaks_gen)
    loopdict["nextbrk"] = next(breaks_gen)

    def find_class(item, loopdict=loopdict):
        val = key(item)
        if val > loopdict["nextbrk"]:
            loopdict["prevbrk"] = loopdict["nextbrk"]
            loopdict["nextbrk"] = next(breaks_gen)
        return loopdict["prevbrk"],loopdict["nextbrk"]

    groups = []
    for valrange,members in itertools.groupby(items, key=find_class):
        yield valrange, list(members)

def unique(items, key=None):
    """
    Bins all same values together, so all bins are unique.
    Only for ints or text values.
    """
    
    # sort and get key
    if key:
        items = sorted(items, key=key)
    else:
        key = lambda x: x
        items = sorted(items)

    for uniq,members in itertools.groupby(items, key=key):
        yield uniq, list(members)

    # maybe add remaining groups if none?
    # ... 

def membership(items, ranges, key=None):
    """
    Groups can be overlapping/nonexclusive and are based on custom ranges.
    """
    ###
    if not key:
        key = lambda x: x
    ###
    for _min,_max in ranges:
        valitems = ((key(item),item) for item in items)
        members = [item for val,item in valitems if val >= _min and val <= _max]
        yield (_min,_max), members

##def rescale(values, newmin, newmax):
##    oldmin, oldmax = max(values), min(values)
##    oldwidth = oldmax - oldmin
##    newwidth = newmax - newmin
##
##    # begin
##    newvalues = []
##    for val in values:
##        relval = (val - oldmin) / oldwidth
##        newval = newmin + newwidth * relval
##        newvalues.append(newval)
##
##    return newvalues
##
##def rescale_single(value, oldmin, oldmax, newmin, newmax):
##    oldwidth = oldmax - oldmin
##    newwidth = newmax - newmin
##
##    # begin
##    relval = (value - oldmin) / oldwidth
##    newval = newmin + newwidth * relval
##    return newval









