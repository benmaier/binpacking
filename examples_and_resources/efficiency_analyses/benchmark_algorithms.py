"""
Benchmark different bin packing algorithms.

Compares:
- to_constant_volume variants: Best Fit Decreasing, Least Loaded Fit, Target Fill
- to_constant_bin_number variants: Current (Adaptive LPT), Pure LPT, LPT + Rebalance

Metrics:
- Speed (execution time)
- Number of bins (for constant-volume)
- Variance of bin fill levels
"""

import random
import time
import statistics
from typing import Callable

# Seed for reproducibility
SEED = 68334

# =============================================================================
# CONSTANT VOLUME ALGORITHMS
# =============================================================================


def cv_best_fit_decreasing(weights: list[float], V_max: float) -> list[list[float]]:
    """Current algorithm: Best Fit Decreasing (place in fullest bin that fits)."""
    weights = sorted(weights, reverse=True)
    bins: list[list[float]] = [[]]
    bin_sums = [0.0]

    for weight in weights:
        # Find bins where item fits
        candidates = [i for i, s in enumerate(bin_sums) if s + weight <= V_max]

        if candidates:
            # Pick fullest bin that fits
            best = max(candidates, key=lambda i: bin_sums[i])
            bins[best].append(weight)
            bin_sums[best] += weight
        else:
            # Open new bin
            bins.append([weight])
            bin_sums.append(weight)

    return bins


def cv_least_loaded_fit(weights: list[float], V_max: float) -> list[list[float]]:
    """Least Loaded Fit: place in emptiest bin that fits."""
    weights = sorted(weights, reverse=True)
    bins: list[list[float]] = [[]]
    bin_sums = [0.0]

    for weight in weights:
        # Find bins where item fits
        candidates = [i for i, s in enumerate(bin_sums) if s + weight <= V_max]

        if candidates:
            # Pick emptiest bin that fits
            best = min(candidates, key=lambda i: bin_sums[i])
            bins[best].append(weight)
            bin_sums[best] += weight
        else:
            # Open new bin
            bins.append([weight])
            bin_sums.append(weight)

    return bins


def cv_target_fill(weights: list[float], V_max: float, target_pct: float = 0.85) -> list[list[float]]:
    """Target Fill: prefer bins closest to target fill level."""
    weights = sorted(weights, reverse=True)
    bins: list[list[float]] = [[]]
    bin_sums = [0.0]
    target = target_pct * V_max

    for weight in weights:
        # Find bins where item fits
        candidates = [i for i, s in enumerate(bin_sums) if s + weight <= V_max]

        if candidates:
            # Pick bin whose new sum is closest to target
            best = min(candidates, key=lambda i: abs(bin_sums[i] + weight - target))
            bins[best].append(weight)
            bin_sums[best] += weight
        else:
            # Open new bin
            bins.append([weight])
            bin_sums.append(weight)

    return bins


def cv_first_fit_decreasing(weights: list[float], V_max: float) -> list[list[float]]:
    """First Fit Decreasing: place in first bin that fits."""
    weights = sorted(weights, reverse=True)
    bins: list[list[float]] = [[]]
    bin_sums = [0.0]

    for weight in weights:
        placed = False
        for i, s in enumerate(bin_sums):
            if s + weight <= V_max:
                bins[i].append(weight)
                bin_sums[i] += weight
                placed = True
                break

        if not placed:
            bins.append([weight])
            bin_sums.append(weight)

    return bins


# =============================================================================
# CONSTANT BIN NUMBER ALGORITHMS
# =============================================================================


def cbn_adaptive_lpt(weights: list[float], N_bin: int) -> list[list[float]]:
    """Current algorithm: Adaptive LPT with V_bin_max ceiling."""
    weights = sorted(weights, reverse=True)
    bins: list[list[float]] = [[] for _ in range(N_bin)]
    bin_sums = [0.0] * N_bin

    V_total = sum(weights)
    V_bin_max = V_total / N_bin

    for i, weight in enumerate(weights):
        b = min(range(N_bin), key=lambda x: bin_sums[x])
        new_sum = bin_sums[b] + weight

        while new_sum > V_bin_max:
            remaining = sum(weights[i:])
            V_bin_max += remaining / N_bin

        bins[b].append(weight)
        bin_sums[b] = new_sum

    return bins


def cbn_pure_lpt(weights: list[float], N_bin: int) -> list[list[float]]:
    """Pure LPT: always place in lightest bin, no ceiling."""
    weights = sorted(weights, reverse=True)
    bins: list[list[float]] = [[] for _ in range(N_bin)]
    bin_sums = [0.0] * N_bin

    for weight in weights:
        b = min(range(N_bin), key=lambda x: bin_sums[x])
        bins[b].append(weight)
        bin_sums[b] += weight

    return bins


def cbn_lpt_rebalance(weights: list[float], N_bin: int) -> list[list[float]]:
    """LPT with post-processing rebalancing."""
    # Start with pure LPT
    bins = cbn_pure_lpt(weights, N_bin)

    # Rebalance: try moving items from heaviest to lightest bin
    improved = True
    max_iterations = 100
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        bin_sums = [sum(b) for b in bins]
        max_idx = max(range(N_bin), key=lambda x: bin_sums[x])
        min_idx = min(range(N_bin), key=lambda x: bin_sums[x])

        if max_idx == min_idx:
            break

        current_diff = bin_sums[max_idx] - bin_sums[min_idx]

        # Try moving each item from heaviest to lightest
        for item in sorted(bins[max_idx], reverse=True):
            new_max = bin_sums[max_idx] - item
            new_min = bin_sums[min_idx] + item
            new_diff = abs(new_max - new_min)

            # Also check if this creates a better overall variance
            if new_diff < current_diff and new_min <= bin_sums[max_idx]:
                bins[max_idx].remove(item)
                bins[min_idx].append(item)
                improved = True
                break

    return bins


def cbn_complete_greedy(weights: list[float], N_bin: int) -> list[list[float]]:
    """Complete Greedy: at each step, pick placement that minimizes variance."""
    weights = sorted(weights, reverse=True)
    bins: list[list[float]] = [[] for _ in range(N_bin)]
    bin_sums = [0.0] * N_bin

    for weight in weights:
        best_bin = 0
        best_variance = float('inf')

        for b in range(N_bin):
            # Simulate placing in bin b
            test_sums = bin_sums.copy()
            test_sums[b] += weight
            var = statistics.variance(test_sums) if N_bin > 1 else 0
            if var < best_variance:
                best_variance = var
                best_bin = b

        bins[best_bin].append(weight)
        bin_sums[best_bin] += weight

    return bins


def cbn_karmarkar_karp(weights: list[float], N_bin: int) -> list[list[float]]:
    """
    Karmarkar-Karp differencing algorithm (simplified for N bins).

    For 2 bins, this is optimal for minimizing difference.
    For N > 2, we use a greedy adaptation.
    """
    if N_bin == 2:
        # Classic KK for 2 bins
        import heapq
        heap = [-w for w in weights]  # Max heap via negation
        heapq.heapify(heap)

        while len(heap) > 1:
            largest = -heapq.heappop(heap)
            second = -heapq.heappop(heap)
            diff = largest - second
            if diff > 0:
                heapq.heappush(heap, -diff)

        # Reconstruct bins (simplified: just use LPT for actual assignment)
        return cbn_pure_lpt(weights, 2)
    else:
        # For N > 2, fall back to LPT with rebalancing
        return cbn_lpt_rebalance(weights, N_bin)


# =============================================================================
# BENCHMARK UTILITIES
# =============================================================================


def generate_dataset(size: int, seed: int = SEED) -> list[float]:
    """Generate random weights with power law distribution."""
    random.seed(seed)
    # Power law distribution tends to create challenging bin packing instances
    return [random.random() ** 0.1 for _ in range(size)]


def calculate_variance(bins: list[list[float]]) -> float:
    """Calculate variance of bin weights."""
    sums = [sum(b) for b in bins]
    if len(sums) < 2:
        return 0.0
    return statistics.variance(sums)


def calculate_fill_stats(bins: list[list[float]], V_max: float | None = None) -> dict:
    """Calculate fill level statistics."""
    sums = [sum(b) for b in bins]
    if not sums:
        return {'min': 0, 'max': 0, 'mean': 0, 'std': 0, 'variance': 0}

    result = {
        'min': min(sums),
        'max': max(sums),
        'mean': statistics.mean(sums),
        'variance': statistics.variance(sums) if len(sums) > 1 else 0,
    }
    result['std'] = result['variance'] ** 0.5

    if V_max:
        result['fill_pcts'] = [s / V_max * 100 for s in sums]
        result['mean_fill_pct'] = statistics.mean(result['fill_pcts'])

    return result


def benchmark_algorithm(
    algo: Callable,
    data: list[float],
    *args,
    runs: int = 10
) -> tuple[list, float]:
    """Run algorithm multiple times and return result + avg time."""
    times = []
    result = None

    for _ in range(runs):
        start = time.perf_counter()
        result = algo(data.copy(), *args)
        end = time.perf_counter()
        times.append(end - start)

    return result, statistics.mean(times)


# =============================================================================
# MAIN BENCHMARK
# =============================================================================


def run_constant_volume_benchmark():
    """Benchmark constant-volume algorithms."""
    print("=" * 70)
    print("CONSTANT VOLUME ALGORITHMS")
    print("=" * 70)

    algorithms = [
        ("Best Fit Decreasing (current)", cv_best_fit_decreasing),
        ("First Fit Decreasing", cv_first_fit_decreasing),
        ("Least Loaded Fit", cv_least_loaded_fit),
        ("Target Fill (85%)", lambda w, v: cv_target_fill(w, v, 0.85)),
    ]

    datasets = [
        ("Small (100 items)", 100),
        ("Medium (1,000 items)", 1000),
        ("Large (10,000 items)", 10000),
    ]

    V_max = 5.0  # Fixed max volume

    for ds_name, ds_size in datasets:
        print(f"\n{'─' * 70}")
        print(f"Dataset: {ds_name}")
        print(f"{'─' * 70}")

        data = generate_dataset(ds_size)
        total_weight = sum(data)
        theoretical_min_bins = int(total_weight / V_max) + 1

        print(f"Total weight: {total_weight:.2f}")
        print(f"V_max: {V_max}")
        print(f"Theoretical min bins: {theoretical_min_bins}")
        print()

        print(f"{'Algorithm':<30} {'Bins':>6} {'Time (ms)':>12} {'Variance':>12} {'Fill % range':>15}")
        print("-" * 75)

        for algo_name, algo_func in algorithms:
            bins, avg_time = benchmark_algorithm(algo_func, data, V_max)
            n_bins = len(bins)
            variance = calculate_variance(bins)
            stats = calculate_fill_stats(bins, V_max)

            fill_range = f"{stats['min']/V_max*100:.0f}%-{stats['max']/V_max*100:.0f}%"

            print(f"{algo_name:<30} {n_bins:>6} {avg_time*1000:>12.3f} {variance:>12.4f} {fill_range:>15}")


def run_constant_bin_number_benchmark():
    """Benchmark constant-bin-number algorithms."""
    print("\n")
    print("=" * 70)
    print("CONSTANT BIN NUMBER ALGORITHMS")
    print("=" * 70)

    algorithms = [
        ("Adaptive LPT (current)", cbn_adaptive_lpt),
        ("Pure LPT", cbn_pure_lpt),
        ("LPT + Rebalance", cbn_lpt_rebalance),
        ("Complete Greedy", cbn_complete_greedy),
    ]

    datasets = [
        ("Small (100 items)", 100),
        ("Medium (1,000 items)", 1000),
        ("Large (10,000 items)", 10000),
    ]

    N_bin = 10  # Fixed number of bins

    for ds_name, ds_size in datasets:
        print(f"\n{'─' * 70}")
        print(f"Dataset: {ds_name}, N_bin = {N_bin}")
        print(f"{'─' * 70}")

        data = generate_dataset(ds_size)
        total_weight = sum(data)
        ideal_per_bin = total_weight / N_bin

        print(f"Total weight: {total_weight:.2f}")
        print(f"Ideal per bin: {ideal_per_bin:.2f}")
        print()

        print(f"{'Algorithm':<25} {'Time (ms)':>12} {'Variance':>12} {'Std Dev':>10} {'Min':>10} {'Max':>10}")
        print("-" * 80)

        for algo_name, algo_func in algorithms:
            # Fewer runs for slow algorithms on large data
            runs = 3 if ds_size >= 10000 and "Complete" in algo_name else 10

            bins, avg_time = benchmark_algorithm(algo_func, data, N_bin, runs=runs)
            stats = calculate_fill_stats(bins)

            print(f"{algo_name:<25} {avg_time*1000:>12.3f} {stats['variance']:>12.4f} "
                  f"{stats['std']:>10.4f} {stats['min']:>10.2f} {stats['max']:>10.2f}")


def run_scaling_benchmark():
    """Benchmark how algorithms scale with data size."""
    print("\n")
    print("=" * 70)
    print("SCALING ANALYSIS")
    print("=" * 70)

    sizes = [100, 500, 1000, 2500, 5000, 10000]

    print("\nConstant Volume (Best Fit Decreasing) - Time vs Size:")
    print(f"{'Size':>10} {'Time (ms)':>12}")
    print("-" * 25)

    for size in sizes:
        data = generate_dataset(size)
        _, avg_time = benchmark_algorithm(cv_best_fit_decreasing, data, 5.0, runs=5)
        print(f"{size:>10} {avg_time*1000:>12.3f}")

    print("\nConstant Bin Number (Pure LPT) - Time vs Size:")
    print(f"{'Size':>10} {'Time (ms)':>12}")
    print("-" * 25)

    for size in sizes:
        data = generate_dataset(size)
        _, avg_time = benchmark_algorithm(cbn_pure_lpt, data, 10, runs=5)
        print(f"{size:>10} {avg_time*1000:>12.3f}")


if __name__ == "__main__":
    print("Bin Packing Algorithm Benchmark")
    print(f"Random seed: {SEED}")
    print()

    run_constant_volume_benchmark()
    run_constant_bin_number_benchmark()
    run_scaling_benchmark()

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)
