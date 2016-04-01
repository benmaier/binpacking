import numpy as np

def to_constant_volume(d,V_max,lower_bound=None,upper_bound=None):
    
    isdict = isinstance(d,dict)

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

    #the total volume is the sum of all weights
    V_total = weights.sum()

    #prepare array containing the current weight of the bins
    weight_sum = [ 0. ]

    #iterate through the weight list, starting with heaviest
    for item,weight in enumerate(weights):
        
        if isdict:
            key = keys[item]

        #put next value in bin with lowest weight sum
        b = np.argmin(weight_sum)

        #calculate new weight of this bin
        new_weight_sum = weight_sum[b] + weight

        #if this weight doesn't fit in the bin
        if new_weight_sum > V_max:
            b = len(weight_sum)
            #open new bin
            weight_sum.append(0.)
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

    return bins

         
if __name__=="__main__":

    a = np.random.power(0.01,size=10000)
    V_max = 1.

    bins = to_constant_volume(a,V_max)

    a = np.sort(a)[::-1]
    print(a[:10])
    print [ np.sum(b) for b in bins ]
    print a.sum(), sum([ np.sum(b) for b in bins ])

    w = [ np.sum(b) for b in bins ]

    import pylab as pl
    pl.plot(np.arange(len(w)),w)
    pl.show()


    b = { 'a': 10, 'b': 10, 'c':11, 'd':1, 'e': 2,'f':7 }
    V_max = max(b.values())

    bins = to_constant_volume(b,V_max)
    print bins


