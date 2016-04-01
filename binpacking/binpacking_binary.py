from binpacking import *
from optparse import OptionParser
import sys


def main():

    parser = OptionParser()
    parser.add_option("-f", "--filepath", dest="filepath", default=None,
                      help="path to the csv-file to be bin-packed"
                      )
    parser.add_option("-V", "--volume", dest="V_max", type="float", default=None,
                      help="maximum volume per bin (constant volume algorithm will be used)"
                      )
    parser.add_option("-N", "--n-bin", dest="N_bin", type="int", default=None,
                      help="number of bins (constant bin number algorithm will be used)"
                      )
    parser.add_option("-c", "--weight-column", dest="weight_column", default=None,
                      help="integer (or string) giving the column number (or column name in header) where the weight is stored"
                      )
    parser.add_option("-H", "--has-header", action="store_true", dest="has_header", default=False,
                      help="parse this option if there is a header in the csv-file"
                      )
    parser.add_option("-d", "--delimiter", dest="delim", default=',',
                      help='delimiter in the csv-file (use "tab" for tabs)'
                      )
    parser.add_option("-q", "--quotechar", dest="quotechar", default='"',
                      help="quotecharacter in the csv-file"
                      )
    parser.add_option("-l", "--lower-bound", dest="lower_bound", type="float", default=None,
                      help="weights below this bound will not be considered"
                      )
    parser.add_option("-u", "--upper-bound", dest="upper_bound", type="float", default=None,
                      help="weights exceeding this bound will not be considered"
                      )

    (options, args) = parser.parse_args()
    opt = vars(options)

    if opt["weight_column"] is None:
        raise Exception("No weight column identifier given")
        sys.exit(1)
    else:
        #if weight column is given try to convert it to a number
        try:
            opt["weight_column"] = int(opt["weight_column"])            
        except:
            pass

    if opt["delim"] == "tab" or opt["delim"] == '"tab"':
        opt["delim"] = '\t'
    
    if opt["V_max"] is None and opt["N_bin"] is None:
        print "Neither V_max nor N_bin are given. No algorithm can be used."
        sys.exit(1)
    elif opt["V_max"] is not None and opt["N_bin"] is not None:
        print "Both V_max and N_bin are given. It's unclear which algorithm is to be used."
        sys.exit(1)
    elif opt["V_max"] is not None and opt["N_bin"] is None:
        opt.pop("N_bin",None)
        csv_to_constant_volume(**opt)
    elif opt["V_max"] is None and opt["N_bin"] is not None:
        opt.pop("V_max",None)
        csv_to_constant_bin_number(**opt)
