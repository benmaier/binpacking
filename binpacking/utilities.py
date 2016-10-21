from __future__ import print_function

import csv
import os
from builtins import str
from past.builtins import basestring


def load_csv(filepath,weight_column,has_header=False,delim=',',quotechar='"'):

    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=delim, quotechar=quotechar)

        data = []
        row_count = 0
        header = None
        
        for row in reader:

            if row_count>0:
                row[weight_column] = float(row[weight_column])
                data.append(row)
            elif has_header:
                header = row
                if isinstance(weight_column,basestring):
                    if has_header:
                        if weight_column in header:
                            weight_column = header.index(weight_column)
                        else:
                            raise Exception("weight key "+weight_column+" not found in header")
            else:
                if isinstance(weight_column,basestring):
                    raise Exception("weight key "+weight_column+" useless, since given csv has no header")

            row_count += 1


    return data,weight_column,header


def print_binsizes(bins,weight_column):
    print("=== distributed items to bins with sizes ===")
    formatstr = "%0" + str(len(str(len(bins)-1))) + "d"
    for ib,b in enumerate(bins):
        print(formatstr % ib, sum([t[weight_column] for t in b]))
    

def save_csvs(bins,filepath,header,delim=',',quotechar='"'):
    filename, file_extension = os.path.splitext(filepath)

    formatstr = "%0" + str(len(str(len(bins)))) + "d"

    for ib,b in enumerate(bins):
        current_path = filename + "_" + formatstr % ib + file_extension
        with open(current_path,"w") as csvfile:            
            writer = csv.writer(csvfile, delimiter=delim, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
            if header is not None:
                writer.writerow(header)
            for row in b:
                writer.writerow(row)
