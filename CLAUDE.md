# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python package providing greedy algorithms for two bin packing problems:
1. **Constant bin number**: Distribute items to exactly N bins with approximately equal total weight per bin
2. **Constant volume**: Distribute items to minimum number of bins, each with a maximum volume V

## Development Environment

Always use the virtual environment in `.venv`:

```bash
source .venv/bin/activate
```

## Development Commands

```bash
# Install in development mode
pip install -e .

# Run all tests
pytest

# Run a single test file
pytest binpacking/tests/constant_volume.py
pytest binpacking/tests/constant_bin_number.py

# Run a specific test
pytest binpacking/tests/constant_volume.py::test_exact_fit
```

## Code Architecture

### Core Algorithms (`binpacking/`)

- `to_constant_bin_number.py`: Greedy algorithm that distributes items to a fixed number of bins, keeping weight sums balanced. Places each item (sorted by weight descending) into the bin with the lowest current weight sum.

- `to_constant_volume.py`: Greedy first-fit decreasing algorithm that places items into bins with fixed maximum capacity, minimizing the number of bins needed.

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

`binpacking_binary.py` provides the `binpacking` command for processing CSV files. Use `-V` for constant volume or `-N` for constant bin number (mutually exclusive).

### Utilities (`utilities.py`)

Helper functions for CSV I/O and list operations (`argmin`, `argmax`, `revargsort`, `get`).

## Code Style

- Max line length: 120 characters (see setup.cfg)
- Python 2/3 compatible (uses `__future__` imports and `builtins`)
