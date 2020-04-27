from binpacking.to_constant_bin_number import to_constant_bin_number


def test_only_zero_weights():
    values = [0, 0, 0]
    bins = to_constant_bin_number(values, 4)
    assert bins == [[0, 0, 0], [], [], []]

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