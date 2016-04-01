# Bin Packing
This package contains greedy algorithms to solve two typical bin packing problems. Consider you have a list of items, each carrying a weight *w_i*. Typical questions are

1. How can we distribute the items to a minimum number of bins *N* of equal volume *V*?
2. How can we distribute the items to exactly *N* bins where each carries items that sum up to approximately equal weight?

The package provides the command line tool "binpacking" using which one can easily bin pack csv-files. To see the usage enter 

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
