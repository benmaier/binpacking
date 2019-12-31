from binpacking.to_constant_bin_number import to_constant_bin_number


def test_only_zero_weights():
    values = [0, 0, 0]
    bins = to_constant_bin_number(values, 4)
    assert bins == [[0, 0, 0], [], [], []]
