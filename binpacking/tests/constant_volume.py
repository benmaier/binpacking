from binpacking.to_constant_volume import to_constant_volume, csv_to_constant_volume


def test_exact_fit():
    values = [1, 2, 1]
    bins = to_constant_volume(values, 2)
    assert len(bins) == 2

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