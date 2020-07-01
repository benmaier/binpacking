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