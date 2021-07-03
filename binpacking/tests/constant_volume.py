from binpacking.to_constant_volume import to_constant_volume, csv_to_constant_volume


def test_exact_fit():
    values = [1, 2, 1]
    bins = to_constant_volume(values, 2)
    assert len(bins) == 2

def test_weight_pos():
    values = [
        [1, 'x'],
        [2, 'y'],
        [1, 'z'],
    ]
    bins = to_constant_volume(values, 2, weight_pos=0)
    for bin_ in bins:
        for item in bin_:
            assert isinstance(item[0], int)
            assert isinstance(item[1], str)

def test_key_func():
    values = [
        {'x': 'a', 'y': 1},
        {'x': 'b', 'y': 5},
        {'x': 'b', 'y': 3},
    ]
    bins = to_constant_volume(values, 2, key=lambda x: x['y'])

    for bin_ in bins:
        for item in bin_:
            assert 'x' in item
            assert 'y' in item

def test_no_fit():
    values = [42, 24]
    bins = to_constant_volume(values, 20)
    assert bins == [[42], [24]]


def test_bounds_and_tuples():
    c = [ ('a', 10, 'foo'), ('b', 10, 'log'), ('c', 11), ('d', 1, 'bar'), ('e', 2, 'bommel'), ('f',7,'floggo') ]
    V_max = 11

    bins = to_constant_volume(c,V_max,weight_pos=1,upper_bound=11)
    bins = [ sorted(_bin, key=lambda x:x[0]) for _bin in bins ]
    assert bins == [
                        [('a', 10, 'foo'), ('d', 1, 'bar')],
                        [('b', 10, 'log')],
                        [
                            ('e', 2, 'bommel'),
                            ('f', 7, 'floggo'),
                        ],
                    ]

    bins = to_constant_volume(c,V_max,weight_pos=1,lower_bound=1)
    bins = [ sorted(_bin, key=lambda x:x[0]) for _bin in bins ]
    assert bins == [
                        [('c', 11,)],
                        [('a', 10, 'foo')],
                        [('b', 10, 'log')],
                        [
                            ('e', 2, 'bommel'),
                            ('f', 7, 'floggo'),
                        ],
                    ]

    bins = to_constant_volume(c,V_max,weight_pos=1,lower_bound=1,upper_bound=11)
    bins = [ sorted(_bin, key=lambda x:x[0]) for _bin in bins ]
    assert bins == [
                        [('a', 10, 'foo')],
                        [('b', 10, 'log')],
                        [
                            ('e', 2, 'bommel'),
                            ('f', 7, 'floggo'),
                        ],
                    ]



if __name__=="__main__":
    test_bounds_and_tuples()
