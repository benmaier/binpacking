"""
Analyze how algorithm quality varies with problem size.

Tests across multiple sizes to see if the "best" algorithm changes.
"""

import statistics
from benchmark_algorithms import (
    SEED,
    generate_dataset,
    cv_best_fit_decreasing,
    cv_least_loaded_fit,
    cbn_adaptive_lpt,
    cbn_pure_lpt,
    cbn_lpt_rebalance,
    benchmark_algorithm,
    calculate_fill_stats,
)


def analyze_constant_volume_by_size():
    """Compare CV algorithms across different problem sizes."""
    print("=" * 80)
    print("CONSTANT VOLUME: Quality vs Problem Size")
    print("=" * 80)
    print()

    sizes = [50, 100, 250, 500, 1000, 2500, 5000, 10000]
    V_max = 5.0

    algorithms = [
        ("Best Fit (current)", cv_best_fit_decreasing),
        ("Least Loaded", cv_least_loaded_fit),
    ]

    # Header
    print(f"{'Size':>7} | ", end="")
    for name, _ in algorithms:
        print(f"{name:^30} | ", end="")
    print()

    print(f"{'':>7} | ", end="")
    for _ in algorithms:
        print(f"{'Bins':>6} {'Var':>8} {'Min%':>6} {'Max%':>6} | ", end="")
    print()

    print("-" * 80)

    for size in sizes:
        data = generate_dataset(size)

        print(f"{size:>7} | ", end="")

        for name, algo in algorithms:
            bins, _ = benchmark_algorithm(algo, data, V_max, runs=3)
            stats = calculate_fill_stats(bins, V_max)
            n_bins = len(bins)
            variance = stats['variance']
            min_pct = stats['min'] / V_max * 100
            max_pct = stats['max'] / V_max * 100

            print(f"{n_bins:>6} {variance:>8.4f} {min_pct:>5.0f}% {max_pct:>5.0f}% | ", end="")

        print()

    print()
    print("Observations:")
    print("  - Bins: Same for both (algorithms don't affect bin count)")
    print("  - Var: Variance of bin fill levels")
    print("  - Min%/Max%: Range of fill percentages")


def analyze_constant_bin_number_by_size():
    """Compare CBN algorithms across different problem sizes."""
    print()
    print("=" * 80)
    print("CONSTANT BIN NUMBER: Quality vs Problem Size")
    print("=" * 80)
    print()

    sizes = [50, 100, 250, 500, 1000, 2500, 5000, 10000]
    N_bin = 10

    algorithms = [
        ("Adaptive LPT", cbn_adaptive_lpt),
        ("Pure LPT", cbn_pure_lpt),
        ("LPT+Rebal", cbn_lpt_rebalance),
    ]

    # Header
    print(f"{'Size':>7} | ", end="")
    for name, _ in algorithms:
        print(f"{name:^20} | ", end="")
    print()

    print(f"{'':>7} | ", end="")
    for _ in algorithms:
        print(f"{'Variance':>9} {'StdDev':>8} | ", end="")
    print()

    print("-" * 80)

    for size in sizes:
        data = generate_dataset(size)

        print(f"{size:>7} | ", end="")

        for name, algo in algorithms:
            bins, _ = benchmark_algorithm(algo, data, N_bin, runs=3)
            stats = calculate_fill_stats(bins)

            print(f"{stats['variance']:>9.6f} {stats['std']:>8.4f} | ", end="")

        print()


def analyze_varying_n_bins():
    """See how algorithms compare with different numbers of bins."""
    print()
    print("=" * 80)
    print("CONSTANT BIN NUMBER: Quality vs N_bin (fixed size=1000)")
    print("=" * 80)
    print()

    data = generate_dataset(1000)
    n_bins_list = [2, 3, 4, 5, 8, 10, 15, 20, 50, 100]

    algorithms = [
        ("Adaptive LPT", cbn_adaptive_lpt),
        ("Pure LPT", cbn_pure_lpt),
        ("LPT+Rebal", cbn_lpt_rebalance),
    ]

    print(f"{'N_bin':>6} | ", end="")
    for name, _ in algorithms:
        print(f"{name:^20} | ", end="")
    print()

    print(f"{'':>6} | ", end="")
    for _ in algorithms:
        print(f"{'Variance':>9} {'StdDev':>8} | ", end="")
    print()

    print("-" * 80)

    for N_bin in n_bins_list:
        print(f"{N_bin:>6} | ", end="")

        for name, algo in algorithms:
            bins = algo(data.copy(), N_bin)
            stats = calculate_fill_stats(bins)

            print(f"{stats['variance']:>9.4f} {stats['std']:>8.4f} | ", end="")

        print()


def analyze_varying_v_max():
    """See how CV algorithms compare with different V_max values."""
    print()
    print("=" * 80)
    print("CONSTANT VOLUME: Quality vs V_max (fixed size=1000)")
    print("=" * 80)
    print()

    data = generate_dataset(1000)
    total = sum(data)
    v_max_list = [2.0, 3.0, 5.0, 8.0, 10.0, 15.0, 20.0]

    algorithms = [
        ("Best Fit", cv_best_fit_decreasing),
        ("Least Loaded", cv_least_loaded_fit),
    ]

    print(f"{'V_max':>6} | ", end="")
    for name, _ in algorithms:
        print(f"{name:^24} | ", end="")
    print()

    print(f"{'':>6} | ", end="")
    for _ in algorithms:
        print(f"{'Bins':>5} {'Var':>8} {'Min%':>5} {'Max%':>5} | ", end="")
    print()

    print("-" * 75)

    for V_max in v_max_list:
        print(f"{V_max:>6.1f} | ", end="")

        for name, algo in algorithms:
            bins = algo(data.copy(), V_max)
            stats = calculate_fill_stats(bins, V_max)
            n_bins = len(bins)
            variance = stats['variance']
            min_pct = stats['min'] / V_max * 100
            max_pct = stats['max'] / V_max * 100

            print(f"{n_bins:>5} {variance:>8.4f} {min_pct:>4.0f}% {max_pct:>4.0f}% | ", end="")

        print()


def generate_power_law(n: int, alpha: float, x_min: float = 1.0, rng=None) -> list[float]:
    """
    Generate samples from a power-law distribution P(x) ∝ x^(-alpha).

    Uses inverse transform sampling:
        x = x_min * u^(-1/(alpha-1))
    where u ~ Uniform(0,1).

    For alpha > 2: finite mean
    For alpha > 3: finite variance
    """
    if rng is None:
        import random
        rng = random
    return [x_min * rng.random() ** (-1.0 / (alpha - 1)) for _ in range(n)]


def analyze_different_distributions():
    """Test with different weight distributions."""
    print()
    print("=" * 80)
    print("EFFECT OF WEIGHT DISTRIBUTION (size=1000, V_max=5.0)")
    print("=" * 80)
    print()

    import random
    random.seed(SEED)

    # Power-law with exponent -3.1: heavy tail but finite variance
    power_law_31 = generate_power_law(1000, alpha=3.1, x_min=0.1, rng=random)

    distributions = {
        "Uniform [0,1]": [random.uniform(0, 1) for _ in range(1000)],
        "Uniform [0,5]": [random.uniform(0, 5) for _ in range(1000)],
        "Power law (α=0.1)": [random.random() ** 0.1 for _ in range(1000)],
        "Power law (α=0.5)": [random.random() ** 0.5 for _ in range(1000)],
        "Power law (α=2.0)": [random.random() ** 2.0 for _ in range(1000)],
        "Power law (exp=-3.1)": power_law_31,
        "Bimodal": [random.choice([random.uniform(0.1, 0.5), random.uniform(3.0, 4.5)]) for _ in range(1000)],
    }

    V_max = 5.0

    algorithms = [
        ("Best Fit", cv_best_fit_decreasing),
        ("Least Loaded", cv_least_loaded_fit),
    ]

    print(f"{'Distribution':<20} | ", end="")
    for name, _ in algorithms:
        print(f"{name:^24} | ", end="")
    print()

    print(f"{'':>20} | ", end="")
    for _ in algorithms:
        print(f"{'Bins':>5} {'Var':>8} {'Min%':>5} {'Max%':>5} | ", end="")
    print()

    print("-" * 80)

    for dist_name, data in distributions.items():
        print(f"{dist_name:<20} | ", end="")

        for name, algo in algorithms:
            bins = algo(data.copy(), V_max)
            stats = calculate_fill_stats(bins, V_max)
            n_bins = len(bins)
            variance = stats['variance']
            min_pct = stats['min'] / V_max * 100
            max_pct = stats['max'] / V_max * 100

            print(f"{n_bins:>5} {variance:>8.4f} {min_pct:>4.0f}% {max_pct:>4.0f}% | ", end="")

        print()

    # Also test constant bin number
    print()
    print("Same distributions, Constant Bin Number (N_bin=10):")
    print()

    cbn_algorithms = [
        ("Adaptive LPT", cbn_adaptive_lpt),
        ("Pure LPT", cbn_pure_lpt),
    ]

    print(f"{'Distribution':<20} | ", end="")
    for name, _ in cbn_algorithms:
        print(f"{name:^15} | ", end="")
    print()

    print(f"{'':>20} | ", end="")
    for _ in cbn_algorithms:
        print(f"{'Variance':>8} {'Std':>5} | ", end="")
    print()

    print("-" * 60)

    for dist_name, data in distributions.items():
        print(f"{dist_name:<20} | ", end="")

        for name, algo in cbn_algorithms:
            bins = algo(data.copy(), 10)
            stats = calculate_fill_stats(bins)

            print(f"{stats['variance']:>8.4f} {stats['std']:>5.2f} | ", end="")

        print()


def analyze_power_law_31():
    """
    Deep dive into power-law distribution with exponent -3.1.

    This is a realistic heavy-tailed distribution with:
    - Finite mean (α > 2)
    - Finite variance (α > 3)
    - But still heavy-tailed (occasional large values)
    """
    print()
    print("=" * 80)
    print("DEEP DIVE: Power-Law Distribution (exponent = -3.1)")
    print("=" * 80)
    print()

    import random
    random.seed(SEED)

    # Generate data
    data = generate_power_law(1000, alpha=3.1, x_min=0.1, rng=random)

    # Show distribution stats
    print("Distribution characteristics:")
    print(f"  n = {len(data)}")
    print(f"  min = {min(data):.4f}")
    print(f"  max = {max(data):.4f}")
    print(f"  mean = {sum(data)/len(data):.4f}")
    print(f"  median = {sorted(data)[len(data)//2]:.4f}")
    print(f"  total = {sum(data):.2f}")

    # Show percentiles
    sorted_data = sorted(data)
    percentiles = [50, 75, 90, 95, 99]
    print("  Percentiles:")
    for p in percentiles:
        idx = int(len(data) * p / 100)
        print(f"    {p}th: {sorted_data[idx]:.4f}")

    print()

    # Test constant volume at different V_max values
    print("Constant Volume (varying V_max):")
    print("-" * 75)
    print(f"{'V_max':>8} | {'Best Fit':^28} | {'Least Loaded':^28} |")
    print(f"{'':>8} | {'Bins':>5} {'Var':>8} {'Min%':>6} {'Max%':>6} | {'Bins':>5} {'Var':>8} {'Min%':>6} {'Max%':>6} |")
    print("-" * 75)

    for V_max in [0.5, 1.0, 2.0, 5.0, 10.0]:
        print(f"{V_max:>8.1f} | ", end="")

        for algo in [cv_best_fit_decreasing, cv_least_loaded_fit]:
            bins = algo(data.copy(), V_max)
            stats = calculate_fill_stats(bins, V_max)
            n_bins = len(bins)
            variance = stats['variance']
            min_pct = stats['min'] / V_max * 100
            max_pct = stats['max'] / V_max * 100
            print(f"{n_bins:>5} {variance:>8.4f} {min_pct:>5.0f}% {max_pct:>5.0f}% | ", end="")
        print()

    print()

    # Test constant bin number at different N_bin values
    print("Constant Bin Number (varying N_bin):")
    print("-" * 60)
    print(f"{'N_bin':>6} | {'Adaptive LPT':^16} | {'Pure LPT':^16} | {'LPT+Rebal':^16} |")
    print(f"{'':>6} | {'Var':>7} {'Std':>7} | {'Var':>7} {'Std':>7} | {'Var':>7} {'Std':>7} |")
    print("-" * 60)

    for N_bin in [3, 5, 10, 20, 50]:
        print(f"{N_bin:>6} | ", end="")

        for algo in [cbn_adaptive_lpt, cbn_pure_lpt, cbn_lpt_rebalance]:
            bins = algo(data.copy(), N_bin)
            stats = calculate_fill_stats(bins)
            print(f"{stats['variance']:>7.4f} {stats['std']:>7.4f} | ", end="")
        print()

    print()

    # Show example bin contents for N_bin=5
    print("Example: N_bin=5 with Pure LPT")
    bins = cbn_pure_lpt(data.copy(), 5)
    total = sum(data)
    ideal = total / 5

    print(f"  Ideal per bin: {ideal:.2f}")
    print()
    for i, b in enumerate(bins):
        b_sum = sum(b)
        deviation = (b_sum - ideal) / ideal * 100
        n_items = len(b)
        max_item = max(b) if b else 0
        print(f"  Bin {i}: sum={b_sum:>7.2f} ({deviation:>+5.1f}%), items={n_items:>3}, max_item={max_item:.2f}")


def analyze_power_law_scaling():
    """See how power-law -3.1 behaves at different problem sizes."""
    print()
    print("=" * 80)
    print("POWER-LAW (-3.1): Scaling with Problem Size")
    print("=" * 80)
    print()

    import random

    sizes = [100, 500, 1000, 5000, 10000]
    V_max = 5.0
    N_bin = 10

    print("Constant Volume (V_max=5.0):")
    print("-" * 70)
    print(f"{'Size':>7} | {'Best Fit':^28} | {'Least Loaded':^28} |")
    print(f"{'':>7} | {'Bins':>5} {'Var':>8} {'Min%':>6} {'Max%':>6} | {'Bins':>5} {'Var':>8} {'Min%':>6} {'Max%':>6} |")
    print("-" * 70)

    for size in sizes:
        random.seed(SEED)
        data = generate_power_law(size, alpha=3.1, x_min=0.1, rng=random)

        print(f"{size:>7} | ", end="")

        for algo in [cv_best_fit_decreasing, cv_least_loaded_fit]:
            bins = algo(data.copy(), V_max)
            stats = calculate_fill_stats(bins, V_max)
            n_bins = len(bins)
            variance = stats['variance']
            min_pct = stats['min'] / V_max * 100
            max_pct = stats['max'] / V_max * 100
            print(f"{n_bins:>5} {variance:>8.4f} {min_pct:>5.0f}% {max_pct:>5.0f}% | ", end="")
        print()

    print()
    print("Constant Bin Number (N_bin=10):")
    print("-" * 50)
    print(f"{'Size':>7} | {'Adaptive LPT':^18} | {'Pure LPT':^18} |")
    print(f"{'':>7} | {'Variance':>8} {'StdDev':>8} | {'Variance':>8} {'StdDev':>8} |")
    print("-" * 50)

    for size in sizes:
        random.seed(SEED)
        data = generate_power_law(size, alpha=3.1, x_min=0.1, rng=random)

        print(f"{size:>7} | ", end="")

        for algo in [cbn_adaptive_lpt, cbn_pure_lpt]:
            bins = algo(data.copy(), N_bin)
            stats = calculate_fill_stats(bins)
            print(f"{stats['variance']:>8.4f} {stats['std']:>8.4f} | ", end="")
        print()


if __name__ == "__main__":
    analyze_constant_volume_by_size()
    analyze_constant_bin_number_by_size()
    analyze_varying_n_bins()
    analyze_varying_v_max()
    analyze_different_distributions()
    analyze_power_law_31()
    analyze_power_law_scaling()

    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
