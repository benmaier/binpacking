binpacking
==========

This package contains greedy algorithms to solve two typical bin packing
problems, (i) sorting items into a constant number of bins, (ii) sorting
items into a low number of bins of constant size. Here's a usage example

.. code:: python

    >>> import binpacking
    >>>
    >>> b = { 'a': 10, 'b': 10, 'c':11, 'd':1, 'e': 2,'f':7 }
    >>> bins = binpacking.to_constant_bin_number(b,4) # 4 being the number of bins
    >>> print("===== dict\n",b,"\n",bins)
    ===== dict
     {'a': 10, 'b': 10, 'c': 11, 'd': 1, 'e': 2, 'f': 7}
     [{'c': 11}, {'b': 10}, {'a': 10}, {'f': 7, 'e': 2, 'd': 1}]
    >>>
    >>> b = list(b.values())
    >>> bins = binpacking.to_constant_volume(b,11) # 11 being the bin volume
    >>> print("===== list\n",b,"\n",bins)
    ===== list
     [10, 10, 11, 1, 2, 7]
     [[11], [10], [10], [7, 2, 1]]

Consider you have a list of items, each carrying a weight *w\_i*.
Typical questions are

#. How can we distribute the items to a minimum number of bins *N* of
   equal volume *V*?
#. How can we distribute the items to exactly *N* bins where each
   carries items that sum up to approximately equal weight?

Problems like this can easily occur in modern computing. Assume you have
to run computations where a lot of files of different sizes have to be
loaded into the memory. However, you only have a machine with 8GB of
RAM. How should you bind the files such that you have to run your
program a minimum amount of times? This is equivalent to solving problem
1.

What about problem 2? Say you have to run a large number of
computations. For each of the jobs you know the time it will probably
take to finish. However, you only have a CPU with 4 cores. How should
you distribute the jobs to the 4 cores such that they will all finish at
approximately the same time?

The package provides the command line tool "binpacking" using which one
can easily bin pack csv-files containing a column that can be identified
with a weight. To see the usage enter

.. code:: bash

    $ binpacking -h
    Usage: binpacking [options]

    Options:
      -h, --help            show this help message and exit
      -f FILEPATH, --filepath=FILEPATH
                            path to the csv-file to be bin-packed
      -V V_MAX, --volume=V_MAX
                            maximum volume per bin (constant volume algorithm will
                            be used)
      -N N_BIN, --n-bin=N_BIN
                            number of bins (constant bin number algorithm will be
                            used)
      -c WEIGHT_COLUMN, --weight-column=WEIGHT_COLUMN
                            integer (or string) giving the column number (or
                        column name in header) where the weight is stored
      -H, --has-header      parse this option if there is a header in the csv-file
      -d DELIM, --delimiter=DELIM
                            delimiter in the csv-file (use "tab" for tabs)
      -q QUOTECHAR, --quotechar=QUOTECHAR
                            quotecharacter in the csv-file
      -l LOWER_BOUND, --lower-bound=LOWER_BOUND
                            weights below this bound will not be considered
      -u UPPER_BOUND, --upper-bound=UPPER_BOUND
                            weights exceeding this bound will not be considered

Install
-------

.. code:: bash

    pip install binpacking

Examples
--------

In the repository's directory

.. code:: bash

    cd examples/
    binpacking -f hamlet_word_count.csv -V 2000 -H -c count -l 10 -u 1000
    binpacking -f hamlet_word_count.csv -N 4 -H -c count 

or in Python

.. code:: python

    import binpacking

    b = { 'a': 10, 'b': 10, 'c':11, 'd':1, 'e': 2,'f':7 }
    bins = binpacking.to_constant_bin_number(b,4)
    print("===== dict\n",b,"\n",bins)

    b = list(b.values())
    bins = binpacking.to_constant_volume(b,11)
    print("===== list\n",b,"\n",bins)

