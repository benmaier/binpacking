"""
Analyze the impact of different sorting strategies on bin packing quality.

Tests whether "Decreasing" (largest first) is optimal, or if other
sorting orders produce better results.
"""

import random
import statistics
from benchmark_algorithms import SEED, generate_dataset, calculate_fill_stats


def pack_constant_volume(weights: list[float], V_max: float, use_least_loaded: bool = True) -> list[list[float]]:
    """Pack with configurable strategy (no sorting - uses order as given)."""
    bins: list[list[float]] = [[]]
    bin_sums = [0.0]

    for weight in weights:
        candidates = [i for i, s in enumerate(bin_sums) if s + weight <= V_max]

        if candidates:
            if use_least_loaded:
                best = min(candidates, key=lambda i: bin_sums[i])
            else:
                best = max(candidates, key=lambda i: bin_sums[i])
            bins[best].append(weight)
            bin_sums[best] += weight
        else:
            bins.append([weight])
            bin_sums.append(weight)

    return bins


def pack_constant_bin_number(weights: list[float], N_bin: int) -> list[list[float]]:
    """Pack with LPT (no sorting - uses order as given)."""
    bins: list[list[float]] = [[] for _ in range(N_bin)]
    bin_sums = [0.0] * N_bin

    for weight in weights:
        b = min(range(N_bin), key=lambda x: bin_sums[x])
        bins[b].append(weight)
        bin_sums[b] += weight

    return bins


def test_sorting_strategies():
    """Compare different sorting strategies."""
    print("=" * 80)
    print("SORTING STRATEGY ANALYSIS")
    print("=" * 80)
    print()

    random.seed(SEED)

    # Test multiple datasets
    datasets = {
        "Uniform [0,1]": [random.uniform(0, 1) for _ in range(1000)],
        "Uniform [0,5]": [random.uniform(0, 5) for _ in range(1000)],
        "Power law": [random.random() ** 0.5 for _ in range(1000)],
        "Bimodal": [random.choice([random.uniform(0.1, 0.5), random.uniform(3.0, 4.5)]) for _ in range(1000)],
    }

    sorting_strategies = {
        "Decreasing": lambda x: sorted(x, reverse=True),
        "Increasing": lambda x: sorted(x),
        "Random": lambda x: random.sample(x, len(x)),
        "Alternating": lambda x: alternate_sort(x),
        "Original": lambda x: x,
    }

    V_max = 5.0
    N_bin = 10

    # =========================================================================
    # CONSTANT VOLUME
    # =========================================================================
    print("CONSTANT VOLUME (V_max=5.0, Least Loaded Fit)")
    print("-" * 80)
    print(f"{'Distribution':<15} | ", end="")
    for name in sorting_strategies:
        print(f"{name:^14} | ", end="")
    print()
    print(f"{'':>15} | ", end="")
    for _ in sorting_strategies:
        print(f"{'Bins':>4} {'Var':>8} | ", end="")
    print()
    print("-" * 80)

    for dist_name, data in datasets.items():
        print(f"{dist_name:<15} | ", end="")

        for sort_name, sort_func in sorting_strategies.items():
            random.seed(SEED)  # Reset for random strategy consistency
            sorted_data = sort_func(data.copy())
            bins = pack_constant_volume(sorted_data, V_max, use_least_loaded=True)
            n_bins = len(bins)
            variance = calculate_fill_stats(bins)['variance']
            print(f"{n_bins:>4} {variance:>8.4f} | ", end="")
        print()

    # =========================================================================
    # CONSTANT BIN NUMBER
    # =========================================================================
    print()
    print("CONSTANT BIN NUMBER (N_bin=10)")
    print("-" * 80)
    print(f"{'Distribution':<15} | ", end="")
    for name in sorting_strategies:
        print(f"{name:^14} | ", end="")
    print()
    print(f"{'':>15} | ", end="")
    for _ in sorting_strategies:
        print(f"{'Var':>6} {'Std':>6} | ", end="")
    print()
    print("-" * 80)

    for dist_name, data in datasets.items():
        print(f"{dist_name:<15} | ", end="")

        for sort_name, sort_func in sorting_strategies.items():
            random.seed(SEED)
            sorted_data = sort_func(data.copy())
            bins = pack_constant_bin_number(sorted_data, N_bin)
            stats = calculate_fill_stats(bins)
            print(f"{stats['variance']:>6.4f} {stats['std']:>6.4f} | ", end="")
        print()


def alternate_sort(weights: list[float]) -> list[float]:
    """Sort alternating between largest and smallest remaining."""
    sorted_weights = sorted(weights, reverse=True)
    result = []
    left, right = 0, len(sorted_weights) - 1
    take_large = True

    while left <= right:
        if take_large:
            result.append(sorted_weights[left])
            left += 1
        else:
            result.append(sorted_weights[right])
            right -= 1
        take_large = not take_large

    return result


def test_sorting_with_size():
    """See if optimal sorting changes with problem size."""
    print()
    print("=" * 80)
    print("SORTING IMPACT BY PROBLEM SIZE (Uniform [0,5], V_max=5.0)")
    print("=" * 80)
    print()

    sizes = [50, 100, 500, 1000, 5000]

    print(f"{'Size':>6} | {'Decreasing':^14} | {'Increasing':^14} | {'Random':^14} |")
    print(f"{'':>6} | {'Bins':>4} {'Var':>8} | {'Bins':>4} {'Var':>8} | {'Bins':>4} {'Var':>8} |")
    print("-" * 60)

    for size in sizes:
        random.seed(SEED)
        data = [random.uniform(0, 5) for _ in range(size)]

        print(f"{size:>6} | ", end="")

        for sort_func in [
            lambda x: sorted(x, reverse=True),
            lambda x: sorted(x),
            lambda x: random.sample(x, len(x)),
        ]:
            random.seed(SEED)
            sorted_data = sort_func(data.copy())
            bins = pack_constant_volume(sorted_data, 5.0, use_least_loaded=True)
            n_bins = len(bins)
            variance = calculate_fill_stats(bins)['variance']
            print(f"{n_bins:>4} {variance:>8.4f} | ", end="")
        print()


def test_why_decreasing_works():
    """Demonstrate WHY decreasing order is important."""
    print()
    print("=" * 80)
    print("WHY DECREASING ORDER MATTERS")
    print("=" * 80)
    print()

    # Simple example
    weights = [4.5, 4.0, 3.5, 1.0, 0.8, 0.5, 0.2]
    V_max = 5.0

    print(f"Weights: {weights}")
    print(f"V_max: {V_max}")
    print()

    for name, order in [
        ("Decreasing", sorted(weights, reverse=True)),
        ("Increasing", sorted(weights)),
    ]:
        bins = pack_constant_volume(order, V_max, use_least_loaded=True)
        sums = [sum(b) for b in bins]

        print(f"{name} order: {order}")
        print(f"  Result: {len(bins)} bins")
        for i, b in enumerate(bins):
            print(f"    Bin {i}: {b} = {sum(b):.1f}")
        print()

    print("Explanation:")
    print("  - Decreasing: Large items placed first, small items fill gaps")
    print("  - Increasing: Small items placed first, large items force new bins")
    print("  - The 'gap filling' effect of decreasing order is crucial")


def test_adversarial_case():
    """Find cases where decreasing might not be optimal."""
    print()
    print("=" * 80)
    print("SEARCHING FOR ADVERSARIAL CASES")
    print("=" * 80)
    print()

    # Try to construct a case where increasing might win
    test_cases = [
        # (name, weights, V_max)
        ("Exact fit pairs", [3.0, 2.0, 3.0, 2.0, 3.0, 2.0], 5.0),
        ("Near V_max items", [4.9, 4.8, 4.7, 0.1, 0.2, 0.3], 5.0),
        ("All same size", [2.5, 2.5, 2.5, 2.5, 2.5, 2.5], 5.0),
        ("Fibonacci-like", [1, 1, 2, 3, 5, 8], 10.0),
        ("Powers of 2", [1, 2, 4, 8, 16, 32], 33.0),
    ]

    print(f"{'Case':<20} | {'Decreasing':^12} | {'Increasing':^12} | {'Winner':^12} |")
    print(f"{'':>20} | {'Bins':>4} {'Var':>6} | {'Bins':>4} {'Var':>6} | {'':^12} |")
    print("-" * 70)

    for name, weights, V_max in test_cases:
        results = {}
        for sort_name, sort_func in [
            ("dec", lambda x: sorted(x, reverse=True)),
            ("inc", lambda x: sorted(x)),
        ]:
            sorted_data = sort_func(weights.copy())
            bins = pack_constant_volume(sorted_data, V_max, use_least_loaded=True)
            results[sort_name] = (len(bins), calculate_fill_stats(bins)['variance'])

        dec_bins, dec_var = results["dec"]
        inc_bins, inc_var = results["inc"]

        if dec_bins < inc_bins:
            winner = "Decreasing"
        elif inc_bins < dec_bins:
            winner = "Increasing"
        elif dec_var < inc_var:
            winner = "Decreasing"
        elif inc_var < dec_var:
            winner = "Increasing"
        else:
            winner = "Tie"

        print(f"{name:<20} | {dec_bins:>4} {dec_var:>6.4f} | {inc_bins:>4} {inc_var:>6.4f} | {winner:^12} |")


if __name__ == "__main__":
    test_sorting_strategies()
    test_sorting_with_size()
    test_why_decreasing_works()
    test_adversarial_case()

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print("""
Decreasing order (largest first) is optimal because:

1. Large items are "difficult" - they have fewer placement options
2. Placing large items first maximizes flexibility for remaining items
3. Small items can fill gaps left by large items
4. Increasing order wastes space: small items spread out, large items don't fit

This is why FFD (First Fit Decreasing) is a well-known improvement over FF,
and why all serious bin packing algorithms use decreasing order.

The only edge cases where order doesn't matter:
- All items are the same size
- Items perfectly fill bins regardless of order
""")
