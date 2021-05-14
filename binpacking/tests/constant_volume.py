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
