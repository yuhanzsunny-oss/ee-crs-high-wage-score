#!/usr/bin/env python3
"""Regression tests on fictional profiles. Every expected number was derived by hand
from the IRCC CRS tables (see comments), not copied from the calculator's output.
Run: python test_crs_calc.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crs_calc import compute  # noqa: E402

# P1: age 27, bachelor's, CLB 9 x4, 1 year Canadian work, no foreign work, no Canadian degree.
#   age 110 + edu 120 + language 124 + Canadian work 40
#   + transferability: edu+language 25, edu+Canadian work 13 -> 38      = 432
P1 = dict(age=27, edu="bachelor", clb=[9] * 4, cdn_years=1)
# P2: same as P1 but no Canadian work yet. 110+120+124 + (edu+language 25)      = 379
P2 = dict(P1, cdn_years=0)
# P3: age 30, master's, CLB 8 x4, 3 yrs foreign work.
#   105 + 135 + 92 + (edu+language 25) + (foreign+language 25)                  = 382
P3 = dict(age=30, edu="master", clb=[8] * 4, foreign_years=3)
# P4: age 25, bachelor's, CLB 9 x4, 2 yrs Canadian + 2 yrs foreign work.
#   110 + 120 + 124 + Canadian work 53
#   + transferability: edu (25 lang + 25 Cdn work) 50, foreign (25 lang + 25 Cdn work) 50 = 507
P4 = dict(age=25, edu="bachelor", clb=[9] * 4, cdn_years=2, foreign_years=2)

CASES = [
    ("P1 no policy", P1, False, 432),
    ("P1 + Tier 2 offer (+70)", dict(P1, offer_noc="21231"), True, 502),
    ("P1 + Tier 1 offer (+100)", dict(P1, offer_noc="10010"), True, 532),
    ("P1 + Tier 3 experience only (+20)", dict(P1, exp_noc="11100"), True, 452),
    ("P1 listening CLB 10 (+3 language), Tier 2 offer", dict(P1, clb=[10, 9, 9, 9], offer_noc="21231"), True, 505),
    ("P1 at age 32 (94), no policy", dict(P1, age=32), False, 416),
    ("P1 at age 32 + Tier 2 offer", dict(P1, age=32, offer_noc="21231"), True, 486),
    ("P1 at age 33 (88) + Tier 2 offer", dict(P1, age=33, offer_noc="21231"), True, 480),
    ("P2 no policy", P2, False, 379),
    ("P2 + Tier 3 offer (+50), no Canadian work yet", dict(P2, offer_noc="11100"), True, 429),
    ("P3 no policy", P3, False, 382),
    ("P3 + Tier 2 offer", dict(P3, offer_noc="21231"), True, 452),
    ("P4 no policy", P4, False, 507),
    ("P4 + Tier 3 offer (53+50=103, under cap)", dict(P4, offer_noc="11100"), True, 557),
    # Theoretical maximum for a single applicant without French/PhD: 676 with a Tier 1
    # offer and 5 years of experience, 606 without the policy.
    ("MAX with policy", dict(age=29, edu="master", clb=[10] * 4, cdn_years=5, foreign_years=3,
                             cdn_edu="3plus", sibling=True, offer_noc="10010"), True, 676),
    ("MAX without policy", dict(age=29, edu="master", clb=[10] * 4, cdn_years=5, foreign_years=3,
                                cdn_edu="3plus", sibling=True, offer_noc="10010"), False, 606),
]

fails = 0
for name, p, policy, want in CASES:
    got = compute(p, policy)["total"]
    ok = got == want
    fails += not ok
    print(("PASS" if ok else "FAIL"), f"{name}: got {got}, want {want}")


def delta(p):
    return compute(p, True)["total"] - compute(p, False)["total"]


# Cap: 5 years (80) + Tier 1 offer (100) = 180 -> capped at 150, so only +70 over no policy.
CAP = dict(age=29, edu="master", clb=[10] * 4, cdn_years=5, foreign_years=3, cdn_edu="3plus", offer_noc="10010")
# No stacking: Tier 2 experience (+40) and Tier 2 offer (+70) -> +70, not +110.
BOTH = dict(P1, exp_noc="21231", offer_noc="21231")
EXP = dict(P1, exp_noc="21231")
for name, got, want in [("cap: 5y + Tier 1 offer adds", delta(CAP), 70),
                        ("no stacking: experience + offer adds", delta(BOTH), 70),
                        ("experience only adds", delta(EXP), 40),
                        ("off-list NOC adds", delta(dict(P1, offer_noc="22220")), 0)]:
    ok = got == want
    fails += not ok
    print(("PASS" if ok else "FAIL"), f"{name} {got}, want {want}")

sys.exit(1 if fails else 0)
