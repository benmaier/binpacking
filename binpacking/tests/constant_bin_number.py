from binpacking.to_constant_bin_number import to_constant_bin_number


def test_only_zero_weights():
    values = [0, 0, 0]
    bins = to_constant_bin_number(values, 4)
    assert bins == [[0, 0, 0], [], [], []]

def test_weight_pos():
    values = [
        [1, 'x'],
        [2, 'y'],
        [1, 'z'],
    ]
    bins = to_constant_bin_number(values, 2, weight_pos=0)
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
    bins = to_constant_bin_number(values, 2, key=lambda x: x['y'])

    for bin_ in bins:
        for item in bin_:
            assert 'x' in item
            assert 'y' in item

def test_bounds_and_tuples():
    c = [ ('a', 10, 'foo'), ('b', 10, 'log'), ('c', 11), ('d', 1, 'bar'), ('e', 2, 'bommel'), ('f',7,'floggo') ]
    N_bin = 4

    bins = to_constant_bin_number(c,N_bin,weight_pos=1,upper_bound=11)
    assert bins == [
                        [('a', 10, 'foo')],
                        [('b', 10, 'log')],
                        [('f', 7, 'floggo')],
                        [('e', 2, 'bommel'), ('d', 1, 'bar')]
                    ]

    bins = to_constant_bin_number(c,N_bin,weight_pos=1,lower_bound=1)
    assert bins == [
                        [('c', 11,)],
                        [('a', 10, 'foo')],
                        [('b', 10, 'log')],
                        [('f', 7, 'floggo'), ('e', 2, 'bommel')],
                    ]

    bins = to_constant_bin_number(c,N_bin,weight_pos=1,lower_bound=1,upper_bound=11)
    assert bins == [
                        [('a', 10, 'foo')],
                        [('b', 10, 'log')],
                        [('f', 7, 'floggo')],
                        [('e', 2, 'bommel')],
                    ]

if __name__=="__main__":
    test_bounds_and_tuples()
