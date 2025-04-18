#!/usr/bin/env python3
# Copyright (c) 2025
# 
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
equal_teams_cp_sat.py
---------------------
CP-SAT proof of the minimum N such that *every* multiset of N
integers in [1,100] contains two disjoint 5-subsets with equal sum.

By default it uses:
  • Symmetry-breaking via fixing the minimum at 1 and enforcing non-decreasing order.
  • Iterative refinement (CEGAR): only adds "sum != sum" constraints when needed.

With --no-cegar it instead builds the full static model once.
"""

from __future__ import annotations
from ortools.sat.python import cp_model
from itertools import combinations
from argparse import ArgumentParser
from time import perf_counter
import os

# Cache for 5-subset combinations per N
TEAMS_CACHE: dict[int, list[tuple[int, ...]]] = {}

def get_5_subsets(N: int) -> list[tuple[int, ...]]:
    """Return (and cache) all 5-element subsets of range(N)."""
    if N not in TEAMS_CACHE:
        TEAMS_CACHE[N] = list(combinations(range(N), 5))
    return TEAMS_CACHE[N]


def find_equal_pair(scores: list[int]) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """Return a disjoint pair of 5-element subsets with equal sum, or None."""
    by_sum: dict[int, list[tuple[int, ...]]] = {}
    for T in get_5_subsets(len(scores)):
        s = sum(scores[i] for i in T)
        for U in by_sum.get(s, []):
            if set(T).isdisjoint(U):
                return T, U
        by_sum.setdefault(s, []).append(T)
    return None


def setup_base_model(N: int) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    """Create model and score variables with symmetry-breaking and trivial pruning."""
    mdl = cp_model.CpModel()
    score = [mdl.NewIntVar(1, 100, f"s[{i}]") for i in range(N)]

    # Symmetry-breaking: minimum = 1, non-decreasing
    mdl.Add(score[0] == 1)
    for i in range(N - 1):
        mdl.Add(score[i] <= score[i + 1])

    # Pruning 1: no 10 identical scores in a row
    for i in range(N - 9):
        mdl.Add(score[i] != score[i + 9])

    # Pruning 2: no more than 4 duplicate-pairs total
    pair_vars = []
    for v in range(1, 101):
        # eq_bools[i] == True <=> score[i] == v
        eq_bools = []
        for i in range(N):
            b = mdl.NewBoolVar(f"is_{v}_{i}")
            mdl.Add(score[i] == v).OnlyEnforceIf(b)
            mdl.Add(score[i] != v).OnlyEnforceIf(b.Not())
            eq_bools.append(b)
        # count how many times v appears
        count_v = sum(eq_bools)
        # pair_v = floor(count_v/2)
        pair_v = mdl.NewIntVar(0, N//2, f"pairs_{v}")
        mdl.Add(pair_v * 2 <= count_v)
        mdl.Add(count_v <= pair_v * 2 + 1)
        pair_vars.append(pair_v)
    # total pairs across all values must be <= 4
    mdl.Add(sum(pair_vars) <= 4)

    return mdl, score


def prove_with_cegar(N: int, wallclock_limit: float, threads: int) -> bool:
    """
    CEGAR solve: incrementally add blocking clauses.
    Returns True if UNSAT (property holds for all N-tuples),
    False if a counter-example is found, or raises TimeoutError.
    """
    block_clauses: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    t0 = perf_counter()

    while True:
        mdl, score = setup_base_model(N)
        # add current blocking clauses
        for T, U in block_clauses:
            mdl.Add(sum(score[i] for i in T) != sum(score[i] for i in U))

        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = threads
        solver.parameters.max_time_in_seconds = max(0.0, wallclock_limit - (perf_counter() - t0))
        status = solver.Solve(mdl)

        if status == cp_model.INFEASIBLE:
            print(f"  UNSAT after {len(block_clauses)} refinements")
            return True

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            sol = [solver.Value(x) for x in score]
            pair = find_equal_pair(sol)
            if pair is None:
                print("  SAT (counter-example found)")
                print("   ", sol)
                return False
            block_clauses.append(pair)
            continue

        raise TimeoutError(f"time limit {wallclock_limit}s exceeded for N={N}")


def prove_static(N: int, wallclock_limit: float, threads: int) -> bool:
    """
    Static solve: build all disjoint-pair constraints once.
    Returns True if UNSAT, False if counter-example, or raises TimeoutError.
    """
    mdl, score = setup_base_model(N)
    teams = get_5_subsets(N)
    # precompute sums for each team
    team_sums = [sum(score[k] for k in T) for T in teams]

    for i, Ti in enumerate(teams):
        si = team_sums[i]
        set_i = set(Ti)
        for j in range(i + 1, len(teams)):
            if set_i.isdisjoint(teams[j]):
                mdl.Add(si != team_sums[j])

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = threads
    solver.parameters.max_time_in_seconds = wallclock_limit
    status = solver.Solve(mdl)

    if status == cp_model.INFEASIBLE:
        print("  UNSAT (static model)")
        return True
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = [solver.Value(x) for x in score]
        print("  SAT (counter-example found)")
        print("   ", sol)
        return False

    raise TimeoutError(f"time limit {wallclock_limit}s exceeded for N={N} (static)")


def main():
    parser = ArgumentParser(description="CP-SAT proof of the 17-player threshold.")
    parser.add_argument("--limit",   type=int, default=600,
                        help="global time-limit in seconds (default 600)")
    parser.add_argument("--threads", type=int, default=os.cpu_count() or 1,
                        help="number of worker threads (default = CPU count)")
    parser.add_argument("--start",   type=int, default=14,
                        help="first N to try (default 14)")
    parser.add_argument("--end",     type=int, default=17,
                        help="last  N to try (default 17)")
    parser.add_argument("--no-cegar", dest="no_cegar", action="store_true",
                        help="disable CEGAR and use static solve instead")
    args = parser.parse_args()

    mode = "static" if args.no_cegar else "cegar"
    print(f"CP-SAT proof  mode={mode}  threads={args.threads}  limit={args.limit}s\n")

    for N in range(args.start, args.end + 1):
        print(f"N = {N}")
        try:
            if args.no_cegar:
                done = prove_static(N, args.limit, args.threads)
            else:
                done = prove_with_cegar(N, args.limit, args.threads)
            if done:
                break
        except TimeoutError as e:
            print("  »", e)
            break


if __name__ == "__main__":
    main()
