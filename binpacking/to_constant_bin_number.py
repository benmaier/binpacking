from __future__ import print_function
from builtins import range

from binpacking.utilities import (
            load_csv,
            save_csvs,
            print_binsizes,
            get,
            argmin,
            revargsort,
        )

def csv_to_constant_bin_number(filepath,
                               weight_column,
                               N_bin,
                               has_header=False,
                               delim=',',
                               quotechar='"',
                               lower_bound=None,
                               upper_bound=None,
                              ):
    """
    Load a csv file, binpack the rows according to one of the columns
    to a constant number of bins.
    Write a new csv file for each bin, containing
    the corresponding rows.
    """

    data, weight_column, header = load_csv(filepath,
                                           weight_column,
                                           has_header=has_header,
                                           delim=delim,
                                           quotechar=quotechar,
                                           )

    bins = to_constant_bin_number(data,
                                  N_bin,
                                  weight_pos=weight_column,
                                  lower_bound=lower_bound,
                                  upper_bound=upper_bound,
                                  )
    print_binsizes(bins, weight_column)

    save_csvs(bins,
              filepath,
              header,
              delim=delim,
              quotechar=quotechar,
              )


def to_constant_bin_number(d,
                           N_bin,
                           weight_pos=None,
                           key=None,
                           lower_bound=None,
                           upper_bound=None,
                       ):
    """
    Distributes a list of weights, a dictionary of weights or a list of tuples containing weights
    to a fixed number of bins while trying to keep the weight distribution constant.

    Parameters
    ==========
    d : iterable
        list containing weights,
        OR dictionary where each (key,value)-pair carries the weight as value,
        OR list of tuples where one entry in the tuple is the weight. The position of
        this weight has to be given in optional variable weight_pos
    N_bin : int
        Number of bins to distribute items to.
    weight_pos : int, default = None
        if d is a list of tuples, this integer number gives the position of the weight in a tuple
    key : function, default = None
        if d is a list, this key functions grabs the weight for an item
    lower_bound : float, default = None
        weights under this bound are not considered
    upper_bound : float, default = None
        weights exceeding this bound are not considered

    Returns
    =======
    bins : list
        A list of length ``N_bin``. Each entry is a list of items or
        a dict of items, depending on the type of ``d``.
    """

    isdict = isinstance(d,dict)

    if not hasattr(d,'__len__'):
        raise TypeError("d must be iterable")

    # Handle empty input
    if len(d) == 0:
        if isdict:
            return [{} for _ in range(N_bin)]
        else:
            return [[] for _ in range(N_bin)]

    if not isdict and hasattr(d[0], '__len__'):
        if weight_pos is not None:
            key = lambda x: x[weight_pos]
        if key is None:
            raise ValueError("Must provide weight_pos or key for tuple list")

    if not isdict and key:
        new_dict = {i: val for i, val in enumerate(d)}
        d = {i: key(val) for i, val in enumerate(d)}
        isdict = True
        is_tuple_list = True
    else:
        is_tuple_list = False

    if isdict:

        #get keys and values (weights)
        keys_vals = d.items()
        keys = [ k for k, v in keys_vals ]
        vals = [ v for k, v in keys_vals ]

        #sort weights decreasingly
        ndcs = revargsort(vals)

        weights = get(vals, ndcs)
        keys = get(keys, ndcs)

        bins = [ {} for i in range(N_bin) ]
    else:
        weights = sorted(d,key=lambda x: -x)
        bins = [ [] for i in range(N_bin) ]

    #find the valid indices
    # First check for invalid bounds
    if lower_bound is not None and upper_bound is not None and lower_bound >= upper_bound:
        raise Exception("lower_bound is greater or equal to upper_bound")

    if lower_bound is not None and upper_bound is not None:
        valid_ndcs = filter(lambda i: lower_bound <= weights[i] <= upper_bound, range(len(weights)))
    elif lower_bound is not None:
        valid_ndcs = filter(lambda i: lower_bound <= weights[i], range(len(weights)))
    elif upper_bound is not None:
        valid_ndcs = filter(lambda i: weights[i] <= upper_bound, range(len(weights)))
    else:
        valid_ndcs = range(len(weights))

    valid_ndcs = list(valid_ndcs)

    weights = get(weights, valid_ndcs)

    if isdict:
        keys = get(keys, valid_ndcs)

    #the total volume is the sum of all weights
    V_total = sum(weights)

    #the first estimate of the maximum bin volume is 
    #the total volume divided to all bins
    V_bin_max = V_total / float(N_bin)

    #prepare array containing the current weight of the bins
    weight_sum = [0. for n in range(N_bin) ]

    #iterate through the weight list, starting with heaviest
    for item, weight in enumerate(weights):

        if isdict:
            key = keys[item]

        #put next value in bin with lowest weight sum
        b = argmin(weight_sum)

        #calculate new weight of this bin
        new_weight_sum = weight_sum[b] + weight

        found_bin = False
        while not found_bin:

            #if this weight fits in the bin
            if new_weight_sum <= V_bin_max:

                #...put it in 
                if isdict:
                    bins[b][key] = weight
                else:
                    bins[b].append(weight)

                #increase weight sum of the bin and continue with
                #next item 
                weight_sum[b] = new_weight_sum
                found_bin = True

            else:
                #if not, increase the max volume by the sum of
                #the rest of the bins per bin
                V_bin_max += sum(weights[item:]) / float(N_bin)

    if not is_tuple_list:
        return bins
    else:
        new_bins = []
        for b in range(N_bin):
            new_bins.append([])
            for key in bins[b]:
                new_bins[b].append(new_dict[key])
        return new_bins

if __name__=="__main__":
    import pylab as pl
    import numpy as np

    a = np.random.power(0.01,size=1000)
    N_bin = 9

    bins = to_constant_bin_number(a,N_bin)
    weight_sums = [np.sum(b) for b in bins]

    #show max values of a and weight sums of the bins
    print(np.sort(a)[-1:-11:-1],weight_sums)

    #plot distribution
    pl.plot(np.arange(N_bin),[np.sum(b) for b in bins])
    pl.ylim([0,max([np.sum(b) for b in bins])+0.1])

    b = { 'a': 10, 'b': 10, 'c':11, 'd':1, 'e': 2,'f':7 }
    bins = to_constant_bin_number(b,4)
    print("===== dict\n",b,"\n",bins)

    lower_bound = None
    upper_bound = None

    b = [ ('a', 10), ('b', 10), ('c',11), ('d',1), ('e', 2),('f',7,'foo') ]
    bins = to_constant_bin_number(b,4,weight_pos=1,lower_bound=lower_bound,upper_bound=upper_bound)
    print("===== list of tuples\n",b,"\n",bins)

    pl.show()

