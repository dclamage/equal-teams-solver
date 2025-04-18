# Equal Team Sum Solver

This Python project uses Google's OR-Tools CP-SAT solver to solve an interesting mathematical problem about equal-sum team combinations. The program determines the minimum number N such that ANY multiset of N integers in the range [1,100] always contains two disjoint 5-element subsets whose sums are equal.

## Problem Description

Given a set of numbers between 1 and 100, the program tries to find two non-overlapping teams of 5 players each that have the same total sum. The goal is to find the threshold number N where it becomes impossible to create a set that doesn't have two equal-sum disjoint teams.

## Requirements

- Python 3.x
- ortools >= 9.4.1874

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
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

Run the program with:
```bash
python equal_teams_solver.py
```

The program will:
1. Test values of N from 14 to 17
2. For each N, try to find a solution using CP-SAT solver
3. Print the solution status and computation time for each N

## Performance

The program uses Google's OR-Tools CP-SAT solver and includes optimizations:
- Symmetry breaking by requiring numbers to be in non-decreasing order
- Pre-computation of all possible 5-element subsets
- Efficient handling of disjoint team combinations
- Multi-threaded search with configurable thread count
- Maximum solving time limit of 10 minutes per instance
- Performance timing information for each calculation

According to the mathematical conjecture, the threshold should be 17, meaning any set of 17 or more numbers between 1 and 100 must contain two disjoint 5-element subsets with equal sums.

## License

[Add your chosen license here]