import csv
import os

def load_csv(filepath,weight_column,has_header=False,delim=',',quotechar='"'):

    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=delim, quotechar=quotechar)

        data = []
        row_count = 0
        header = None
        
        for row in reader:

            if row_count>0:
                data.extend(row)
            elif has_header:
                header = row

            row_count += 1

    if isinstance(weight_column,basestring):
        if has_header:
            if weight_column in header:
                weight_column = header.index(weight_column)
            else:
                raise Exception("weight key "+weight_key+" not found in header")
        else:
            raise Exception("weight key "+weight_key+" useless, since given csv has no header")

    return data,weight_column,header



def save_csvs(bins,filepath,header,delim=',',quotechar='"'):
    filename, file_extension = os.path.splitext(filepath)

    N_bins = len(bins)
    N_chars = len(str(N_bins))
    formatstr = "%0" + str(N_chars) + "d"

    for ib,b in enumerate(bins):
        current_path = filename + "_" + formatstr % ib + file_extension
        with open(current_path,"w") as csvfile:            
            writer = csv.writer(csvfile, delimiter=delim, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
            if header is not None:
                writer.writerow(header)
            for row in b:
                writer.writerow(row)
