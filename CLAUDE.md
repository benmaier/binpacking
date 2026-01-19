# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python 3.10+ package providing greedy algorithms for two bin packing problems:
1. **Constant bin number**: Distribute items to exactly N bins with approximately equal total weight per bin (LPT algorithm)
2. **Constant volume**: Distribute items to minimum number of bins, each with a maximum volume V (Least Loaded Fit Decreasing)

## Development Environment

Always use the virtual environment in `.venv`:

```bash
source .venv/bin/activate
```

## Development Commands

```bash
# Install in development mode
pip install -e .

# Install with numpy acceleration
pip install -e ".[numpy]"

# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run a single test file
pytest binpacking/tests/test_constant_volume.py
pytest binpacking/tests/test_constant_bin_number.py

# Run with coverage
pytest --cov=binpacking/
```

## Code Architecture

### Core Algorithms (`binpacking/`)

- `to_constant_bin_number.py`: **LPT (Longest Processing Time)** algorithm. Sorts items by weight (descending), places each in the bin with lowest current weight sum.

- `to_constant_volume.py`: **Least Loaded Fit Decreasing** algorithm. Sorts items by weight (descending), places each in the emptiest bin where it fits.

- `numpy.py`: NumPy-accelerated versions of both algorithms for large datasets. Same API, better performance.

Both algorithms accept:
- Plain lists of weights
- Dictionaries `{key: weight}`
- Lists of tuples with `weight_pos` or `key` function to extract weights

### Input Flexibility

The algorithms preserve the original data structure in output:
- List input → list of lists
- Dict input → list of dicts
- Tuple list input → list of tuple lists (use `weight_pos` parameter)

### CLI Tool

`binpacking_binary.py` provides the `binpacking` command for processing CSV files:
- Use `-V` for constant volume or `-N` for constant bin number (mutually exclusive)
- Use `--use-numpy` for NumPy acceleration
- Use `-o` / `--output-dir` to specify output directory (default: cwd)

### Utilities (`utilities.py`)

Helper functions for CSV I/O (`load_csv`, `save_csvs`, `print_binsizes`) and list operations (`argmin`, `argmax`, `revargsort`, `get`).

## Code Style

- Python 3.10+ with modern type annotations (`list[T]`, `X | Y`)
- Max line length: 120 characters (see pyproject.toml)
- Uses `@overload` decorators for polymorphic function signatures

## Testing

126 tests with 95% coverage. Tests are in `binpacking/tests/`:
- `test_constant_volume.py` - constant volume algorithm
- `test_constant_bin_number.py` - constant bin number algorithm
- `test_numpy.py` - NumPy-accelerated versions
- `test_csv_operations.py` - CSV loading/saving
- `test_cli.py` - CLI interface
- `test_utilities.py` - utility functions

## Algorithm Analysis

See `examples_and_resources/efficiency_analyses/` for benchmarks comparing algorithm variants and justification for the chosen algorithms.
