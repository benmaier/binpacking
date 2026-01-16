import csv
import os
from typing import Any, Sequence


def load_csv(
    filepath: str,
    weight_column: int | str,
    has_header: bool = False,
    delim: str = ',',
    quotechar: str = '"',
) -> tuple[list[list[Any]], int, list[str] | None]:
    """Load CSV file and extract weight column.

    Returns:
        Tuple of (data rows, weight column index, header row or None)
    """
    weight_col_is_str = isinstance(weight_column, str)

    if weight_col_is_str and not has_header:
        raise Exception("weight key " + weight_column + " useless, since given csv has no header")

    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=delim, quotechar=quotechar)

        data: list[list[Any]] = []
        row_count = 0
        header: list[str] | None = None

        for row in reader:

            if has_header and row_count == 0:
                header = row
                if weight_column in header:
                    weight_column = header.index(weight_column)
                elif weight_col_is_str:
                    raise Exception("weight key " + str(weight_column) + " not found in header")
            else:
                row[weight_column] = float(row[weight_column])  # type: ignore[index]
                data.append(row)

            row_count += 1

    return data, weight_column, header  # type: ignore[return-value]


def print_binsizes(bins: list[list[Any]], weight_column: int) -> None:
    """Print bin sizes to stdout."""
    # Calculate stats for each bin
    bin_weights = [sum(t[weight_column] for t in b) for b in bins]
    bin_counts = [len(b) for b in bins]
    total_weight = sum(bin_weights)
    total_count = sum(bin_counts)

    # Determine column widths (minimum width for headers, "Total" label)
    bin_width = max(5, len(str(len(bins) - 1)))  # "Total" is 5 chars
    count_width = max(5, len(str(total_count)))  # "Items"
    weight_width = max(6, max((len(f"{w:.2f}") for w in bin_weights), default=1), len(f"{total_weight:.2f}"))  # "Weight"

    # Print header
    print(f"{'Bin':>{bin_width}}  {'Items':>{count_width}}  {'Weight':>{weight_width}}  {'%':>6}")
    total_width = bin_width + count_width + weight_width + 16
    print("-" * total_width)

    # Print each bin
    for ib, (weight, count) in enumerate(zip(bin_weights, bin_counts)):
        pct = (weight / total_weight * 100) if total_weight > 0 else 0
        print(f"{ib:>{bin_width}}  {count:>{count_width}}  {weight:>{weight_width}.2f}  {pct:>5.1f}%")

    # Print total
    print("-" * total_width)
    print(f"{'Total':>{bin_width}}  {total_count:>{count_width}}  {total_weight:>{weight_width}.2f}")


def save_csvs(
    bins: list[list[Any]],
    filepath: str,
    header: list[str] | None,
    delim: str = ',',
    quotechar: str = '"',
) -> None:
    """Save bins to separate CSV files."""
    filename, file_extension = os.path.splitext(filepath)

    formatstr = "%0" + str(len(str(len(bins)))) + "d"

    for ib, b in enumerate(bins):
        current_path = filename + "_" + formatstr % ib + file_extension
        with open(current_path, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=delim, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
            if header is not None:
                writer.writerow(header)
            for row in b:
                writer.writerow(row)


def get[T](lst: Sequence[T], ndx: Sequence[int]) -> list[T]:
    """Get elements from list at specified indices."""
    return [lst[n] for n in ndx]


def argmin(lst: Sequence[float]) -> int:
    """Return index of minimum value."""
    return min(range(len(lst)), key=lst.__getitem__)


def argmax(lst: Sequence[float]) -> int:
    """Return index of maximum value."""
    return max(range(len(lst)), key=lst.__getitem__)


def argsort(lst: Sequence[float]) -> list[int]:
    """Return indices that would sort the list ascending."""
    return sorted(range(len(lst)), key=lst.__getitem__)


def revargsort(lst: Sequence[float]) -> list[int]:
    """Return indices that would sort the list descending."""
    return sorted(range(len(lst)), key=lambda i: -lst[i])
