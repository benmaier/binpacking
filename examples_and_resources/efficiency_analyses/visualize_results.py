"""
Visualize bin packing algorithm comparison.

Creates text-based charts showing algorithm performance.
"""

from benchmark_algorithms import (
    SEED,
    generate_dataset,
    cv_best_fit_decreasing,
    cv_first_fit_decreasing,
    cv_least_loaded_fit,
    cv_target_fill,
    cbn_adaptive_lpt,
    cbn_pure_lpt,
    cbn_lpt_rebalance,
    calculate_fill_stats,
)


def bar_chart(values: list[float], max_width: int = 50, label: str = "") -> None:
    """Print a simple horizontal bar chart."""
    if not values:
        return

    max_val = max(values)
    for i, v in enumerate(values):
        bar_len = int(v / max_val * max_width) if max_val > 0 else 0
        bar = "█" * bar_len
        print(f"  Bin {i:2d}: {bar} {v:.2f}")


def compare_bin_distributions():
    """Show side-by-side bin weight distributions."""
    print("=" * 70)
    print("BIN WEIGHT DISTRIBUTIONS")
    print("=" * 70)

    # Use medium dataset for visibility
    data = generate_dataset(500)
    V_max = 5.0
    N_bin = 8

    print("\n--- CONSTANT VOLUME (V_max=5.0) ---\n")

    cv_algos = [
        ("Best Fit Decreasing", cv_best_fit_decreasing(data, V_max)),
        ("Least Loaded Fit", cv_least_loaded_fit(data, V_max)),
    ]

    for name, bins in cv_algos:
        sums = sorted([sum(b) for b in bins], reverse=True)
        stats = calculate_fill_stats(bins, V_max)

        print(f"{name}")
        print(f"  Bins: {len(bins)}, Variance: {stats['variance']:.4f}")
        print(f"  Fill range: {stats['min']/V_max*100:.1f}% - {stats['max']/V_max*100:.1f}%")

        # Show first 10 and last 5 bins
        print("  Top 10 bins:")
        for i, s in enumerate(sums[:10]):
            fill_pct = s / V_max * 100
            bar_len = int(fill_pct / 2)
            print(f"    {i:2d}: {'█' * bar_len}{'░' * (50-bar_len)} {fill_pct:5.1f}%")

        if len(sums) > 15:
            print(f"    ... ({len(sums) - 15} more bins) ...")

        print("  Bottom 5 bins:")
        for i, s in enumerate(sums[-5:]):
            fill_pct = s / V_max * 100
            bar_len = int(fill_pct / 2)
            idx = len(sums) - 5 + i
            print(f"    {idx:2d}: {'█' * bar_len}{'░' * (50-bar_len)} {fill_pct:5.1f}%")
        print()

    print("\n--- CONSTANT BIN NUMBER (N_bin=8) ---\n")

    cbn_algos = [
        ("Adaptive LPT (current)", cbn_adaptive_lpt(data, N_bin)),
        ("Pure LPT", cbn_pure_lpt(data, N_bin)),
        ("LPT + Rebalance", cbn_lpt_rebalance(data, N_bin)),
    ]

    total = sum(data)
    ideal = total / N_bin

    for name, bins in cbn_algos:
        sums = [sum(b) for b in bins]
        stats = calculate_fill_stats(bins)

        print(f"{name}")
        print(f"  Ideal per bin: {ideal:.2f}")
        print(f"  Variance: {stats['variance']:.6f}, Std Dev: {stats['std']:.4f}")
        print(f"  Range: {stats['min']:.2f} - {stats['max']:.2f}")

        # Visualize deviation from ideal
        print("  Bins (deviation from ideal):")
        for i, s in enumerate(sums):
            deviation = s - ideal
            deviation_pct = deviation / ideal * 100

            if deviation >= 0:
                bar = "+" * min(int(abs(deviation_pct) * 5), 25)
                print(f"    Bin {i}: {s:7.2f}  {bar:>25} +{deviation_pct:.2f}%")
            else:
                bar = "-" * min(int(abs(deviation_pct) * 5), 25)
                print(f"    Bin {i}: {s:7.2f}  {bar:<25} {deviation_pct:.2f}%")
        print()


def show_challenging_case():
    """Show a case where algorithms differ more significantly."""
    print("\n" + "=" * 70)
    print("CHALLENGING CASE: Skewed Distribution")
    print("=" * 70)

    # Create a more challenging distribution with some large items
    import random
    random.seed(SEED)

    # Mix of large and small items
    data = (
        [4.5, 4.3, 4.1, 3.9, 3.7, 3.5]  # Large items
        + [random.uniform(0.1, 1.0) for _ in range(50)]  # Many small items
    )
    random.shuffle(data)

    V_max = 5.0
    N_bin = 5

    print(f"\nItems: {len(data)}, Total: {sum(data):.2f}")
    print(f"Large items (>3.0): {[f'{x:.1f}' for x in sorted(data, reverse=True) if x > 3.0]}")

    print("\n--- CONSTANT VOLUME ---\n")

    for name, algo in [
        ("Best Fit Decreasing", cv_best_fit_decreasing),
        ("Least Loaded Fit", cv_least_loaded_fit),
    ]:
        bins = algo(data, V_max)
        sums = [sum(b) for b in bins]
        stats = calculate_fill_stats(bins, V_max)

        print(f"{name}: {len(bins)} bins")
        print(f"  Variance: {stats['variance']:.4f}")
        for i, s in enumerate(sums):
            print(f"  Bin {i}: {s:.2f} ({s/V_max*100:.0f}%)")
        print()

    print("--- CONSTANT BIN NUMBER ---\n")

    for name, algo in [
        ("Adaptive LPT", cbn_adaptive_lpt),
        ("Pure LPT", cbn_pure_lpt),
        ("LPT + Rebalance", cbn_lpt_rebalance),
    ]:
        bins = algo(data, N_bin)
        sums = [sum(b) for b in bins]
        stats = calculate_fill_stats(bins)

        print(f"{name}: variance={stats['variance']:.4f}")
        for i, s in enumerate(sums):
            print(f"  Bin {i}: {s:.2f}")
        print()


if __name__ == "__main__":
    compare_bin_distributions()
    show_challenging_case()
