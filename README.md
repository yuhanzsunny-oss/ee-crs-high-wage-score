# ee-crs-high-wage-score

A [Claude Code](https://claude.com/claude-code) skill (plus a standalone Python calculator) for the
Canada **Express Entry CRS score** under the **high-wage occupation points that take effect on 2026-11-03**.

适用于加拿大 Express Entry:算 CRS 分数,并判断 2026-11-03 起的"高薪职业加分"(offer / 12 个月经验,Tier 1/2/3,150 封顶)能给你加多少分。

## What it does

- Computes CRS for a **single applicant** from the official IRCC tables, with and without the new policy, and shows the delta.
- Looks up any NOC code or occupation keyword in the official **186-occupation** high-wage list.
- Encodes the rule people most often get wrong: the Labour Market Integration factor is the **higher of two routes, not both**: (years-of-work points + high-wage experience bonus, max 80+70=150) **or** (fixed job-offer points 100/70/50). An offer does **not** stack on top of years-of-work points.
- Separates official wording from what IRCC has not said (see `references/policy-rules.md`).

## Use as a Claude Code skill

```bash
git clone https://github.com/yuhanzsunny-oss/ee-crs-high-wage-score.git
cp -r ee-crs-high-wage-score/ee-crs-high-wage-score ~/.claude/skills/
```

Then ask Claude things like "我有 Tier 2 的 offer,英语 CLB9,现在多少分?" and it will use the skill.

## Use the calculator directly (Python 3.8+, no dependencies)

```bash
cd ee-crs-high-wage-score/scripts
python crs_calc.py --lookup 21231            # tier of a NOC code
python crs_calc.py --lookup software         # search by title
python crs_calc.py --age 27 --edu bachelor --clb 9 --cdn-years 1 \
    --exp-noc 21231 --offer-noc 21231
python test_crs_calc.py                      # regression tests
```

`--clb` takes one value (all four abilities) or four values (L R W S).
`--edu`: `secondary 1yr 2yr bachelor two_plus master phd`. `--cdn-edu`: `none 1-2 3plus`.
Optional: `--second-clb`, `--french 25|50`, `--sibling`, `--pnp`, `--exp-noc`, or `--json profile.json`.

## Known limits

- **Single applicants only** (the cap is 140, not 150, with a spouse; tables differ).
- No certificate-of-qualification group.
- Cross-checked against an independent open-source implementation on 8,424 generated profiles: 0 differences (this caught a real bug in an earlier version, documented in `references/policy-rules.md`).
- The market snapshot (draw cut-offs, pool distribution) is dated October 2026 and goes stale.

## Sources

IRCC pages dated 2026-10-16: the high-wage occupations announcement, the high-wage NOC list, and the CRS criteria for single applicants (links in `references/policy-rules.md`).

## Disclaimer

This is an unofficial calculator for information only. It is **not legal or immigration advice** and is not affiliated with IRCC.
Rules change; always confirm with IRCC and a licensed immigration consultant or lawyer before relying on any result.
Never misrepresent your experience or job offer: misrepresentation can lead to a five-year ban.

## License

MIT, see `LICENSE`.
