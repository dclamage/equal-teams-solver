#!/usr/bin/env python3
# Copyright (c) 2025
# 
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import re
from itertools import combinations

def parse_int_prefix(s):
    """
    Grab the leading integer from s (e.g. "123," → 123, "45abc" → 45),
    or return None if there is no integer at the start.
    """
    m = re.match(r'^([+-]?\d+)', s)
    return int(m.group(1)) if m else None

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <int1>[,] <int2>[,] ...")
        sys.exit(1)

    # Parse all args (splitting on commas) and extract integer prefixes
    values = []
    for arg in sys.argv[1:]:
        for part in arg.split(','):
            part = part.strip()
            if not part:
                continue
            val = parse_int_prefix(part)
            if val is None:
                print(f"Warning: skipping '{part}' (no leading integer)")
            else:
                values.append(val)

    # Print parsed array for confirmation
    print("Parsed", len(values), "values:", values)

    # Need at least 10 values to form two disjoint 5‑element subsets
    if len(values) < 10:
        print("Error: need at least 10 integers to form two disjoint subsets of size 5.")
        sys.exit(1)

    # Scan all index‑based combinations of size 5, bucket by sum,
    # and look for two disjoint subsets with the same sum.
    sum_to_combos = {}
    for combo in combinations(range(len(values)), 5):
        s = sum(values[i] for i in combo)
        if s in sum_to_combos:
            for prev in sum_to_combos[s]:
                if set(prev).isdisjoint(combo):
                    print(f"\nFound two disjoint subsets of size 5 with sum = {s}:")
                    print(f"  Indices {prev} → {[values[i] for i in prev]}")
                    print(f"  Indices {combo} → {[values[i] for i in combo]}")
                    return
            sum_to_combos[s].append(combo)
        else:
            sum_to_combos[s] = [combo]

    print("\nNo two disjoint size-5 subsets have the same sum.")

if __name__ == "__main__":
    main()

