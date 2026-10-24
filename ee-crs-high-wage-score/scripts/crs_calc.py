#!/usr/bin/env python3
"""Express Entry CRS calculator (single applicant) with the 2026-11-03 high-wage points.

Tables: IRCC "CRS criteria: single applicant" page, dated 2026-10-16.
High-wage rules: IRCC backgrounder "Changes to Express Entry for high-wage occupations".
The way the 150 cap combines duration points with the new points is INFERRED
(see references/policy-rules.md); the output says so.

Usage examples:
  python crs_calc.py --age 27 --edu bachelor --clb 9 9 9 9 --cdn-years 1 \
      --offer-noc 21231
  python crs_calc.py --json profile.json
  python crs_calc.py --lookup 21231        # tier of a NOC code
  python crs_calc.py --lookup "software"   # search titles
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOC_TSV = os.path.join(HERE, "..", "references", "high-wage-noc-list.tsv")

AGE = {18: 99, 19: 105, 30: 105, 31: 99, 32: 94, 33: 88, 34: 83, 35: 77, 36: 72,
       37: 66, 38: 61, 39: 55, 40: 50, 41: 39, 42: 28, 43: 17, 44: 6}
EDU = {"none": 0, "secondary": 30, "1yr": 90, "2yr": 98, "bachelor": 120,
       "two_plus": 128, "master": 135, "phd": 150}
EDU_HIGH = {"two_plus", "master", "phd"}      # transferability: 25/50 row
EDU_LOW = {"1yr", "2yr", "bachelor"}          # transferability: 13/25 row
CDN_WORK = {0: 0, 1: 40, 2: 53, 3: 64, 4: 72}  # 5+ -> 80
EXP_BONUS = {1: 70, 2: 40, 3: 20}              # 12 months in a listed occupation
OFFER_BONUS = {1: 100, 2: 70, 3: 50}           # qualifying job offer
LMIF_CAP = 150                                 # single; 140 with spouse (unsupported here)


def age_points(age):
    if 20 <= age <= 29:
        return 110
    return AGE.get(age, 0)


def clb_points(clb, table=(34, 31, 23, 17, 9, 6)):
    if clb >= 10:
        return table[0]
    if clb == 9:
        return table[1]
    if clb == 8:
        return table[2]
    if clb == 7:
        return table[3]
    if clb == 6:
        return table[4]
    if clb >= 4:
        return table[5]
    return 0


def second_lang_points(clbs):
    def one(c):
        return 6 if c >= 9 else 3 if c >= 7 else 1 if c >= 5 else 0
    return min(24, sum(one(c) for c in clbs))


def lang_band(clbs):
    low = min(clbs)
    return "high" if low >= 9 else "mid" if low >= 7 else None


def load_noc():
    out = {}
    with open(NOC_TSV, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["noc"]] = (int(row["tier"]), row["title"])
    return out


def tier_of(noc, table):
    if not noc:
        return None
    noc = str(noc).zfill(5)
    return table[noc][0] if noc in table else None


def transferability(p, cdn_years, band):
    edu = p["edu"]
    fy = int(p.get("foreign_years", 0))
    # Group A: education
    if edu in EDU_HIGH:
        lang_pts = {"mid": 25, "high": 50}.get(band, 0)
        cdn_pts = 25 if cdn_years == 1 else 50 if cdn_years >= 2 else 0
    elif edu in EDU_LOW:
        lang_pts = {"mid": 13, "high": 25}.get(band, 0)
        cdn_pts = 13 if cdn_years == 1 else 25 if cdn_years >= 2 else 0
    else:
        lang_pts = cdn_pts = 0
    group_a = min(50, lang_pts + cdn_pts)
    # Group B: foreign work experience
    if fy >= 3:
        f_lang = {"mid": 25, "high": 50}.get(band, 0)
        f_cdn = 25 if cdn_years == 1 else 50 if cdn_years >= 2 else 0
    elif fy >= 1:
        f_lang = {"mid": 13, "high": 25}.get(band, 0)
        f_cdn = 13 if cdn_years == 1 else 25 if cdn_years >= 2 else 0
    else:
        f_lang = f_cdn = 0
    group_b = min(50, f_lang + f_cdn)
    return min(100, group_a + group_b), {"education": group_a, "foreign_work": group_b}


def compute(p, policy=True):
    noc = load_noc()
    cdn_years = int(p.get("cdn_years", 0))
    clb = p["clb"]
    band = lang_band(clb)
    bd = {}
    bd["age"] = age_points(p["age"])
    bd["education"] = EDU[p["edu"]]
    bd["first_language"] = sum(clb_points(c) for c in clb)
    bd["second_language"] = second_lang_points(p["second_clb"]) if p.get("second_clb") else 0

    dur = 80 if cdn_years >= 5 else CDN_WORK.get(cdn_years, 0)
    bonus_note = None
    exp_t = tier_of(p.get("exp_noc"), noc) if cdn_years >= 1 else None
    offer_t = tier_of(p.get("offer_noc"), noc)
    exp_b = EXP_BONUS.get(exp_t, 0)
    offer_b = OFFER_BONUS.get(offer_t, 0)
    if policy:
        bonus = max(exp_b, offer_b)
        bd["canadian_work_incl_policy"] = min(LMIF_CAP, dur + bonus)
        bonus_note = {"duration_points": dur, "exp_bonus": exp_b, "offer_bonus": offer_b,
                      "applied_bonus": bonus, "capped": dur + bonus > LMIF_CAP}
    else:
        bd["canadian_work_incl_policy"] = dur

    tr, tr_detail = transferability(p, cdn_years, band)
    bd["skill_transferability"] = tr
    bd["canadian_education"] = {"none": 0, "1-2": 15, "3plus": 30}[p.get("cdn_edu", "none")]
    bd["sibling_in_canada"] = 15 if p.get("sibling") else 0
    bd["french_bonus"] = {"none": 0, "25": 25, "50": 50}[str(p.get("french", "none"))]
    bd["provincial_nomination"] = 600 if p.get("pnp") else 0
    total = sum(bd.values())
    return {"total": total, "breakdown": bd, "transferability_groups": tr_detail,
            "policy_detail": bonus_note, "exp_tier": exp_t, "offer_tier": offer_t}


def report(p):
    on = compute(p, policy=True)
    off = compute(p, policy=False)
    print(json.dumps({
        "with_policy": on, "without_policy_total": off["total"],
        "policy_delta": on["total"] - off["total"],
        "warning": "150-cap composition is inferred (duration + max(exp,offer), capped 150); "
                   "re-check against the official CRS page after 2026-11-03. Single applicant only.",
    }, ensure_ascii=False, indent=2))


def lookup(q):
    noc = load_noc()
    q = q.strip()
    if q.isdigit():
        code = q.zfill(5)
        if code in noc:
            print(f"{code}  Tier {noc[code][0]}  {noc[code][1]}")
        else:
            print(f"{code}  NOT on the high-wage list (no points from this policy)")
        return
    hits = [(c, t, n) for c, (t, n) in noc.items() if q.lower() in n.lower()]
    for c, t, n in sorted(hits):
        print(f"{c}  Tier {t}  {n}")
    if not hits:
        print("no match")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--lookup")
    ap.add_argument("--age", type=int)
    ap.add_argument("--edu", choices=sorted(EDU))
    ap.add_argument("--clb", type=int, nargs="+",
                    help="one value (all four) or four values L R W S")
    ap.add_argument("--second-clb", type=int, nargs=4)
    ap.add_argument("--cdn-years", type=int, default=0)
    ap.add_argument("--foreign-years", type=int, default=0)
    ap.add_argument("--cdn-edu", choices=["none", "1-2", "3plus"], default="none")
    ap.add_argument("--sibling", action="store_true")
    ap.add_argument("--french", choices=["none", "25", "50"], default="none")
    ap.add_argument("--pnp", action="store_true")
    ap.add_argument("--exp-noc", help="NOC of the 12-month Canadian experience")
    ap.add_argument("--offer-noc", help="NOC of the qualifying job offer")
    a = ap.parse_args()

    if a.lookup:
        return lookup(a.lookup)
    if a.json:
        with open(a.json, encoding="utf-8") as f:
            p = json.load(f)
    else:
        if a.age is None or not a.edu or not a.clb:
            ap.error("need --age --edu --clb (or --json / --lookup)")
        clb = a.clb * 4 if len(a.clb) == 1 else a.clb
        if len(clb) != 4:
            ap.error("--clb takes 1 or 4 values")
        p = {"age": a.age, "edu": a.edu, "clb": clb, "second_clb": a.second_clb,
             "cdn_years": a.cdn_years, "foreign_years": a.foreign_years,
             "cdn_edu": a.cdn_edu, "sibling": a.sibling, "french": a.french,
             "pnp": a.pnp, "exp_noc": a.exp_noc or a.offer_noc, "offer_noc": a.offer_noc}
        # Without a separate --exp-noc, assume the experience is in the offer's NOC
    report(p)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
