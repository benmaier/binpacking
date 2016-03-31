import numpy as np

def to_constant_bin_number(d,N_bin,lower_bound=None,upper_bound=None):
    
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

        bins = [ {} for i in xrange(N_bin) ]
    else:
        weights = np.sort(np.array(d))[::-1]
        bins = [ [] for i in xrange(N_bin) ]

    #the total volume is the sum of all weights
    V_total = weights.sum()

    #the first estimate of the maximum bin volume is 
    #the total volume divided to all bins
    V_bin_max = V_total / float(N_bin)
    
    #prepare array containing the current weight of the bins
    weight_sum = np.zeros(N_bin)

    #iterate through the weight list, starting with heaviest
    for item,weight in enumerate(weights):
        
        if isdict:
            key = keys[item]

        #put next value in bin with lowest weight sum
        b = np.argmin(weight_sum)

        #calculate new weight of this bin
        new_weight_sum = weight_sum[b] + weight

        found_bin = False
        while not found_bin:

            #if this weight fits in the bin
            if new_weight_sum < V_bin_max:

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
                V_bin_max += np.sum(weights[item:]) / float(N_bin)


    return bins

         
if __name__=="__main__":

    a = np.random.power(0.01,size=1000)
    N_bin = 9

    bins = to_constant_bin_number(a,N_bin)

    a = np.sort(a)[::-1]
    print(a[:10])
    print a.sum()/N_bin
    print [ np.sum(b) for b in bins ]
    print a.sum(), sum([ np.sum(b) for b in bins ])



