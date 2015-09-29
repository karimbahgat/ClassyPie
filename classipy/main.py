
from __future__ import division
from . import _breaks

def breaks(values, algorithm, **kwargs):
    """
    Only get the break points.
    """
    values = sorted(values)
    func = _breaks.__dict__[algorithm]
    breaks = func(values, **kwargs)
    return breaks

def split(values, breaks, **kwargs):
    """
    Splits a list of values into n non-overlapping classes based on the
    specified algorithm.

    Arguments:

    - **breaks**: List of custom break values or the name of the algorithm to use.
        Valid names are:
        - histogram (alias for equal)
        - equal
        - quantile
        - pretty
        - stdev
        - natural
    - **values**: The list of values to classify.
    - **classes**: The number of classes to group the values into.
    - more...

    Returns:

    - All the input values reorganized into the groups/classes that they belong to,
    as a list of lists of values.
    """
    values = sorted(values)

    # if not custom specified, get break values from algorithm name
    if isinstance(breaks, bytes):
        func = _breaks.__dict__[breaks]
        breaks = func(values, **kwargs)
    else:
        breaks.insert(0, min(values))
        breaks.append(max(values))
        
    # begin
    groups = []
    group = []
    prevbreak = breaks.pop(0)
    nextbreak = breaks[0]
    for val in values:
        if val <= nextbreak:
            group.append(val)
        else:
            groups.append( ((prevbreak,nextbreak), group) )
            if len(breaks) >= 2: # dont do for last break pair
                group = [val] # count towards next bin
                prevbreak = breaks.pop(0)
                nextbreak = breaks[0]
    # add last group
    groups.append( ((prevbreak,nextbreak), group) )
    # somehow add remaining breaks even if no values in (eg if specified custom start and end values)
    # ...
    return groups

def unique(values):
    """
    Bins all same values together, so all bins are unique.
    Only for ints or text values.
    """
    groups = []
    uniqs = sorted(set(values))
    for uniq in uniqs:
        group = [uniq for _ in range(values.count(uniq))]
        groups.append( (uniq, group) )
    return groups

def membership(values, ranges):
    """
    Groups can be overlapping/nonexclusive and are based on custom ranges.
    
    TODO: possibly also allow custom function...
    """
    groups = []
    for _min,_max in ranges:
        group = [val for val in values if val >= _min and val <= _max]
        groups.append( ((_min,_max), group) )
    return groups

def rescale(values, newmin, newmax):
    oldmin, oldmax = max(values), min(values)
    oldwidth = oldmax - oldmin
    newwidth = newmax - newmin

    # begin
    newvalues = []
    for val in values:
        relval = (val - oldmin) / oldwidth
        newval = newmin + newwidth * relval
        newvalues.append(newval)

    return newvalues









