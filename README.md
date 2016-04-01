# Bin Packing
This package contains greedy algorithms to solve two typical bin packing problems. Consider you have a list of items, each carrying a weight *w_i*. Typical questions are

1. How can we distribute the items to a minimum number of bins *N* of equal volume *V*?
2. How can we distribute the items to exactly *N* bins where each carries items that sum up to approximately equal weight?

Problems like this can easily occur in modern computing. Assume you have to run computations where a lot of files of different sizes have to be loaded into the memory. However, you only have a machine with 8GB of RAM. How should you bind the files such that you have to run your program a minimum amount of times? This is equivalent to solving problem 1.

What about problem 2? Say you have to run a large number of computations. For each of the jobs you know the time it will probably take to finish. However, you only have a CPU with 4 cores. How should you distribute the jobs to the 4 cores such that they will all finish at approximately the same time?

The package provides the command line tool "binpacking" using which one can easily bin pack csv-files containing a column that can be identified with a weight. To see the usage enter 

    $ binpacking -h

## Install 

    $ sudo python setup.py install

## Examples

In the package's folder, do

```
cd examples/
binpacking -f hamlet_word_count.csv -V 2000 -H -c count -l 10 -u 1000
binpacking -f hamlet_word_count.csv -N 4 -H -c count 
```

or in python, do 

```python
import binpacking

b = { 'a': 10, 'b': 10, 'c':11, 'd':1, 'e': 2,'f':7 }
bins = binpacking.to_constant_bin_number(b,4)
print "===== dict\n",b,"\n",bins

b = b.values()
bins = binpacking.to_constant_volume(b,11)
print "===== list\n",b,"\n",bins

```
