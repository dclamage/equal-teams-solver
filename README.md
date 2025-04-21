# Equal Team Sum Solver

This Python project uses Google's OR-Tools CP-SAT solver to explore a mathematical conjecture about equal-sum team combinations. For a given number N, it tries to find a counterexample - a set of N integers between 1 and 100 that does NOT contain any two disjoint 5-element subsets with equal sums. The program can be used to test different values of N to find these counterexamples or prove that none exist.

A counterexample is a set of N integers between 1 and 100 that demonstrates the property doesn't hold - meaning there are NO two disjoint 5-element subsets within it that sum to the same value. The absence of a counterexample for a given N would prove that ANY set of N integers between 1 and 100 must contain two disjoint 5-element subsets with equal sums.

## Known Counter-Examples

Here are the known counter-examples for different values of N. A counter-example is a set of N numbers that contains NO two disjoint 5-element subsets with equal sums:

| N   | Counter-Example |
|-----|---------------------------|
| 11  |1, 1, 1, 1, 1, 1, 1, 1, 3, 4, 5|
| 12  |1, 1, 3, 3, 4, 4, 4, 4, 4, 5, 15, 25|
| 13  |1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 6, 99|
| 14  |1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 14, 67|
| 15  |1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 5, 24, 38, 50|
| 16  |1, 2, 3, 3, 3, 3, 3, 11, 29, 33, 47, 99, 99, 99, 99, 99|
| 17  |1, 2, 3, 5, 8, 14, 25, 47, 100, 100, 100, 100, 100, 100, 100, 100, 100|

## Theoretical Bounds

It has been theoretically proven that there exists some N ≤ 35 such that every set of N integers from [1,100] must contain two disjoint 5-element subsets with equal sums. In other words, 35 is an upper bound on the threshold - it's impossible to construct a counter-example with 35 or more numbers. The exact threshold may be (and likely is) lower than this bound.

See this [Math Overflow](https://mathoverflow.net/questions/448083/how-many-players-are-needed-so-that-two-evenly-matched-teams-can-be-picked) post for the proof.

## Requirements

- Python 3.x
- ortools >= 9.4.1874

## Installation

1. Clone this repository:
```bash
git clone https://github.com/dclamage/equal-teams-solver
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Main Solver

Run the solver program with:
```bash
python equal_teams_solver.py [options]
```

Command line options:
- `--limit SECONDS`: Global time limit in seconds (default: 600)
- `--threads N`: Number of worker threads (default: CPU count)
- `--start N`: First N to try (default: 14)
- `--end N`: Last N to try (default: 17)
- `--no-cegar`: Disable CEGAR and use static solve instead

The program will:
1. Test values of N from the start value to the end value
2. For each N, try to find a solution using CP-SAT solver
3. Use either CEGAR (Counter-Example Guided Abstraction Refinement) or static solving
4. Print the solution status and computation time for each N

### Example Checker

To verify potential counter-examples, use the example checker:
```bash
python example_checker.py <int1>[,] <int2>[,] ...
```

The example checker takes a list of integers (comma-separated or space-separated) and:
1. Checks if there are two disjoint 5-element subsets with equal sums
2. If found, prints the subsets and their indices
3. If not found, confirms the set is a valid counter-example

Example usage:
```bash
python example_checker.py 1, 2, 3, 5, 8, 14, 25, 47, 100, 100, 100, 100, 100, 100, 100, 100, 100
```

## Performance

The program uses Google's OR-Tools CP-SAT solver and includes optimizations:
- Symmetry breaking by requiring numbers to be in non-decreasing order
- Pre-computation of all possible 5-element subsets
- Efficient handling of disjoint team combinations
- Multi-threaded search with configurable thread count
- Maximum solving time limit (configurable per instance)
- Performance timing information for each calculation
- CEGAR ([Counter-Example Guided Abstraction Refinement](https://en.wikipedia.org/wiki/Counterexample-guided_abstraction_refinement)) by default
- Optional static solving mode (sometimes faster)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
