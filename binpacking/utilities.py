from __future__ import print_function

import csv
import os
from builtins import str
from past.builtins import basestring


def load_csv(filepath,weight_column,has_header=False,delim=',',quotechar='"'):

    weight_col_is_str = isinstance(weight_column,basestring)

    if weight_col_is_str and not has_header:
        raise Exception("weight key "+weight_column+" useless, since given csv has no header")

    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=delim, quotechar=quotechar)

        data = []
        row_count = 0
        header = None

        for row in reader:

            if has_header and row_count == 0:
                header = row
                if weight_column in header:
                    weight_column = header.index(weight_column)
                elif weight_col_is_str:
                    raise Exception("weight key "+weight_column+" not found in header")
            else:
                row[weight_column] = float(row[weight_column])
                data.append(row)

            row_count += 1


    return data, weight_column, header


def print_binsizes(bins,weight_column):
    print("=== distributed items to bins with sizes ===")
    formatstr = "%0" + str(len(str(len(bins)-1))) + "d"
    for ib,b in enumerate(bins):
        print(formatstr % ib, sum([t[weight_column] for t in b]))
        
def print_bin(bins):
    print("=== items distributed over bins ===")
    for i,bin in enumerate(bins):
        print(f"\n= bin {i} =")
        for entry in bin:
            print(f"{entry[0]};{entry[1]};{entry[2]};{entry[3]}")

    print(f"\ntotal count of bins: {len(bins)}")

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

def get(lst,ndx):
    return [lst[n] for n in ndx]

def argmin(lst):
    return min(range(len(lst)), key=lst.__getitem__)

def argmax(lst):
    return max(range(len(lst)), key=lst.__getitem__)

def argsort(lst):
    return sorted(range(len(lst)), key=lst.__getitem__)

def revargsort(lst):
    return sorted(range(len(lst)), key=lambda i: -lst[i])
