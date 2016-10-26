from binpacking.to_constant_volume import to_constant_volume, csv_to_constant_volume


def test_exact_fit():
    values = [1, 2, 1]
    bins = to_constant_volume(values, 2)
    assert len(bins) == 2