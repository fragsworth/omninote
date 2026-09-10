#!/usr/bin/env python3
"""Exact Fisher test for a 2x2 table. No scipy in this container, so this is done
from first principles with exact rational arithmetic -- no floating-point
accumulation in the tail sum.

Table layout:
        yes   no
  ctl    a     b
  trt    c     d

Two-sided p = sum of hypergeometric probabilities of every table with the same
row and column margins whose probability is <= P(observed), which is the
conventional "sum of tables at least as extreme by probability" definition and
what scipy.stats.fisher_exact reports.
"""
from fractions import Fraction
from math import comb


def _p_table(a, b, c, d):
    """Exact hypergeometric probability of one table with these margins."""
    n = a + b + c + d
    return Fraction(comb(a + b, a) * comb(c + d, c), comb(n, a + c))


def fisher_exact(a, b, c, d):
    """Return (odds_ratio, two_sided_p). odds_ratio is the sample OR, inf/0 allowed."""
    r1, r2 = a + b, c + d
    c1 = a + c
    observed = _p_table(a, b, c, d)
    total = Fraction(0)
    # enumerate every table consistent with the margins, indexed by its top-left cell
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    for x in range(lo, hi + 1):
        t = (x, r1 - x, c1 - x, r2 - (c1 - x))
        p = _p_table(*t)
        if p <= observed:
            total += p
    if b * c == 0:
        odds = float("inf") if a * d > 0 else float("nan")
    else:
        odds = (a * d) / (b * c)
    return odds, float(total)


def fmt_p(p):
    if p >= 0.0095:
        return f"{p:.3f}"
    return f"{p:.1e}"


if __name__ == "__main__":
    # sanity checks against known values
    # Fisher's tea-tasting 3/4 vs 1/4 -> p = 0.4857...
    assert abs(fisher_exact(3, 1, 1, 3)[1] - 0.4857142857) < 1e-9
    # a null table is p = 1.0
    assert abs(fisher_exact(5, 5, 5, 5)[1] - 1.0) < 1e-12
    # complete separation 15/15 vs 0/15
    o, p = fisher_exact(15, 0, 0, 15)
    assert p < 1e-7, p
    # the split the brief names as roughly the detection threshold at n=15
    print("12/15 vs 4/15 ->", fisher_exact(12, 3, 4, 11))
    print("11/15 vs 4/15 ->", fisher_exact(11, 4, 4, 11))
    print("15/15 vs 0/15 ->", fisher_exact(15, 0, 0, 15))
    print("10/15 vs 5/15 ->", fisher_exact(10, 5, 5, 10))
    print("all self-tests passed")
