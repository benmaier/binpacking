from __future__ import print_function
from builtins import range

from binpacking.utilities import load_csv, save_csvs, print_binsizes

import numpy as np

def csv_to_constant_volume(filepath,weight_column,V_max,has_header=False,delim=',',quotechar='"',lower_bound=None,upper_bound=None):

    data, weight_column, header = load_csv(filepath,weight_column,has_header=has_header,delim=',',quotechar='"')

    bins = to_constant_volume(data,V_max,weight_pos=weight_column,lower_bound=lower_bound,upper_bound=upper_bound)
    print_binsizes(bins,weight_column)

    save_csvs(bins,filepath,header,delim=delim,quotechar=quotechar)


def to_constant_volume(d,V_max,weight_pos=None,key=None,lower_bound=None,upper_bound=None):
    '''
    Distributes a list of weights, a dictionary of weights or a list of tuples containing weights
    to a minimal number of bins which have a fixed volume.
    INPUT:
    --- d: list containing weights, 
           OR dictionary where each (key,value)-pair carries the weight as value,
           OR list of tuples where one entry in the tuple is the weight. The position of 
              this weight has to be given in optional variable weight_pos
         
    optional:
    ~~~ weight_pos: int -- if d is a list of tuples, this integer number gives the position of the weight in a tuple
    ~~~ key: function -- if d is a list, this key functions grabs the weight for an item
    ~~~ lower_bound: weights under this bound are not considered
    ~~~ upper_bound: weights exceeding this bound are not considered
    '''

    #define functions for the applying the bounds
    if lower_bound is not None and upper_bound is not None and lower_bound<upper_bound:
        get_valid_weight_ndcs = lambda a: np.nonzero(np.logical_and(a>lower_bound,a<upper_bound))[0]
    elif lower_bound is not None:
        get_valid_weight_ndcs = lambda a: np.nonzero(a>lower_bound)[0]
    elif upper_bound is not None:
        get_valid_weight_ndcs = lambda a: np.nonzero(a<upper_bound)[0]
    elif lower_bound is None and upper_bound is None:
        get_valid_weight_ndcs = lambda a: np.arange(len(a),dtype=int)
    elif lower_bound>=upper_bound:
        raise Exception("lower_bound is greater or equal to upper_bound")

    isdict = isinstance(d,dict)

    if isinstance(d, list) and hasattr(d[0], '__len__'):
        if weight_pos is not None:
            key = lambda x: x[weight_pos]
        if key is None:
            raise ValueError("Must provide weight_pos or key for tuple list")
    
    if isinstance(d, list) and key:
        new_dict = {i: val for i, val in enumerate(d)}
        print(new_dict)
        d = {i: key(val) for i, val in enumerate(d)}
        isdict = True
        is_tuple_list = True
    else:
        is_tuple_list = False

    if isdict:

        #get keys and values (weights)
        keys_vals = d.items()
        keys = np.array([ k for k,v in keys_vals ])
        vals = np.array([ v for k,v in keys_vals ])

        #sort weights decreasingly
        ndcs = np.argsort(vals)[::-1]

        weights = vals[ndcs]
        keys = keys[ndcs]

        bins = [ {} ]
    else:
        weights = np.sort(np.array(d))[::-1]
        bins = [ [] ]

    #find the valid indices
    valid_ndcs = get_valid_weight_ndcs(weights)
    weights = weights[valid_ndcs]

    if isdict:
        keys = keys[valid_ndcs]

    #the total volume is the sum of all weights
    V_total = weights.sum()

    #prepare array containing the current weight of the bins
    weight_sum = np.array([ 0. ])

    #iterate through the weight list, starting with heaviest
    for item,weight in enumerate(weights):
        
        if isdict:
            key = keys[item]

        #find candidate bins where the weight might fit
        candidate_bins = np.where(weight_sum+weight <= V_max)[0]

        # if there are candidates where it fits
        if len(candidate_bins)>0:

            # find the fullest bin where this item fits and assign it
            candidate_index = np.argmax(weight_sum[candidate_bins])
            b = candidate_bins[candidate_index]

        #if this weight doesn't fit in any existent bin
        else:
            # open a new bin
            b = len(weight_sum)
            weight_sum = np.append(weight_sum, 0.)
            if isdict:
                bins.append({})
            else:
                bins.append([])

        #put it in 
        if isdict:
            bins[b][key] = weight
        else:
            bins[b].append(weight)

        #increase weight sum of the bin and continue with
        #next item 
        weight_sum[b] += weight

    if not is_tuple_list:
        return bins
    else:
        new_bins = []
        for b in range(len(bins)):
            new_bins.append([])
            for key in bins[b]:
                new_bins[b].append(new_dict[key])
        return new_bins

         
if __name__=="__main__":

    a = np.random.power(0.01,size=10000)
    V_max = 1.

    bins = to_constant_volume(a,V_max)

    a = np.sort(a)[::-1]
    print(a[:10])
    print([ np.sum(b) for b in bins ])
    print(a.sum(), sum([ np.sum(b) for b in bins ]))

    w = [ np.sum(b) for b in bins ]

    import matplotlib.pyplot as pl
    pl.plot(np.arange(len(w)),w)
    pl.show()


    b = { 'a': 10, 'b': 10, 'c':11, 'd':1, 'e': 2,'f':7 }
    V_max = max(b.values())

    bins = to_constant_volume(b,V_max)
    print(bins)


