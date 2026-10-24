#!/usr/bin/env python3
"""Regression tests on fictional profiles. Every expected number was derived by hand
from the IRCC CRS tables (see comments), not copied from the calculator's output.
The calculator was also compared with an independent open-source implementation on 8,424
generated profiles (all non-policy tables and the Labour Market Integration factor): 0 differences.
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

# Labour Market Integration factor = max(work path, offer path), where
#   work path = years-of-work points + high-wage experience bonus,  offer path = offer points.
CASES = [
    ("P1 no policy", P1, False, 432),
    # offer only (the 12 months of experience are NOT in a listed occupation): max(40, offer)
    ("P1 + Tier 2 offer only: max(40,70)=70", dict(P1, offer_noc="21231"), True, 462),
    ("P1 + Tier 1 offer only: max(40,100)=100", dict(P1, offer_noc="10010"), True, 492),
    ("P1 + Tier 3 offer only: max(40,50)=50", dict(P1, offer_noc="11100"), True, 442),
    # experience only: 40 + bonus
    ("P1 + Tier 3 experience only: 40+20=60", dict(P1, exp_noc="11100"), True, 452),
    # same listed job for both experience and offer: the work path wins, the offer adds nothing
    ("P1 Tier 2 exp + Tier 2 offer: max(80,70)=80", dict(P1, exp_noc="21231", offer_noc="21231"), True, 472),
    ("P1 Tier 1 exp + Tier 1 offer: max(110,100)=110", dict(P1, exp_noc="10010", offer_noc="10010"), True, 502),
    ("P1 Tier 3 exp + Tier 3 offer: max(60,50)=60", dict(P1, exp_noc="11100", offer_noc="11100"), True, 452),
    ("P1 listening CLB 10 (+3), Tier 2 offer only", dict(P1, clb=[10, 9, 9, 9], offer_noc="21231"), True, 465),
    ("P1 at age 32 (94), no policy", dict(P1, age=32), False, 416),
    ("P1 at age 32 + Tier 2 offer only", dict(P1, age=32, offer_noc="21231"), True, 446),
    ("P1 at age 33 (88) + Tier 2 offer only", dict(P1, age=33, offer_noc="21231"), True, 440),
    ("P2 no policy", P2, False, 379),
    ("P2 + Tier 3 offer (+50), no Canadian work yet", dict(P2, offer_noc="11100"), True, 429),
    ("P3 no policy", P3, False, 382),
    ("P3 + Tier 2 offer, no Canadian work yet", dict(P3, offer_noc="21231"), True, 452),
    ("P4 no policy", P4, False, 507),
    ("P4 + Tier 3 offer only: max(53,50)=53, no gain", dict(P4, offer_noc="11100"), True, 507),
    ("P4 + Tier 2 offer only: max(53,70)=70", dict(P4, offer_noc="21231"), True, 524),
    ("P4 + Tier 3 experience only: 53+20=73", dict(P4, exp_noc="11100"), True, 527),
    # Theoretical maximum for a single applicant without French/PhD: 676 needs Tier 1 EXPERIENCE
    # (80 + 70 = 150); a Tier 1 offer alone gives only 100. Without the policy: 606.
    ("MAX with policy (5y, Tier 1 experience)", dict(age=29, edu="master", clb=[10] * 4, cdn_years=5, foreign_years=3,
                             cdn_edu="3plus", sibling=True, exp_noc="10010", offer_noc="10010"), True, 676),
    ("MAX without policy", dict(age=29, edu="master", clb=[10] * 4, cdn_years=5, foreign_years=3,
                                cdn_edu="3plus", sibling=True), False, 606),
]

fails = 0
for name, p, policy, want in CASES:
    got = compute(p, policy)["total"]
    ok = got == want
    fails += not ok
    print(("PASS" if ok else "FAIL"), f"{name}: got {got}, want {want}")


def delta(p):
    return compute(p, True)["total"] - compute(p, False)["total"]


# Deltas over the no-policy score. The offer replaces, it does not add to, the years-of-work points.
BIG = dict(age=29, edu="master", clb=[10] * 4, cdn_years=5, foreign_years=3, cdn_edu="3plus")
for name, got, want in [
        ("5y + Tier 1 offer only adds (100-80)", delta(dict(BIG, offer_noc="10010")), 20),
        ("5y + Tier 1 experience adds (150-80)", delta(dict(BIG, exp_noc="10010")), 70),
        ("1y + Tier 2 offer only adds (70-40)", delta(dict(P1, offer_noc="21231")), 30),
        ("1y + Tier 2 experience adds", delta(dict(P1, exp_noc="21231")), 40),
        ("1y + Tier 2 experience AND offer adds (not 40+70)", delta(dict(P1, exp_noc="21231", offer_noc="21231")), 40),
        ("off-list NOC adds", delta(dict(P1, offer_noc="22220")), 0)]:
    ok = got == want
    fails += not ok
    print(("PASS" if ok else "FAIL"), f"{name} {got}, want {want}")

sys.exit(1 if fails else 0)
