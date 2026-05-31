#!/usr/bin/env python3
"""Generate a ranked daily study plan for N days remaining.

Usage:
  python study_planner.py <N-days>

Examples:
  python study_planner.py 5
  python study_planner.py 14
"""
import sys
import json
import pathlib

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent
ARCH_GRAPH = VAULT / "graphs" / "ARCHETYPE-GRAPH.json"

# Fallback ranking (in case JSON parse fails). Ordered by exam priority.
FALLBACK_TIER_1 = ["A01", "A02", "A03", "A04", "A05", "A06", "A08"]
FALLBACK_TIER_2 = ["A07", "A11", "A12", "A14", "A19", "A21", "A22", "A23"]
FALLBACK_TIER_3 = ["A09", "A10", "A13", "A15", "A16", "A24"]
FALLBACK_TIER_4 = ["A17", "A18", "A20"]


def tier_score(node: dict) -> float:
    """A composite score: lower tier = higher score; stars add to it."""
    tier = node.get("tier", 4)
    stars = node.get("stars", 1)
    return (5 - tier) * 10 + stars


def build_plan(nodes: list, days: int) -> list:
    """Distribute archetypes across days."""
    if not nodes:
        return [(d, []) for d in range(1, days + 1)]
    ranked = sorted(nodes, key=lambda n: -tier_score(n))

    if days <= 0:
        return []

    if days >= 10:
        # Comfortable plan: Tier-1 first 30-40% of days, T2 next chunk, T3 then T4, last day mock.
        plan = []
        t1 = [n for n in ranked if n.get("tier", 4) == 1]
        t2 = [n for n in ranked if n.get("tier", 4) == 2]
        t3 = [n for n in ranked if n.get("tier", 4) == 3]
        t4 = [n for n in ranked if n.get("tier", 4) == 4]

        t1_days = max(3, days * 4 // 10)        # ~40% on tier 1
        t2_days = max(3, days * 3 // 10)        # ~30% on tier 2
        t3_days = max(2, days * 2 // 10)        # ~20% on tier 3
        # remainder = t4 + mock day(s)

        for day in range(1, days + 1):
            offset = day - 1
            if offset < t1_days and t1:
                items = [t1[(offset * len(t1) // t1_days) % len(t1)]]
            elif offset < t1_days + t2_days and t2:
                idx = offset - t1_days
                items = [t2[(idx * len(t2) // t2_days) % len(t2)]]
            elif offset < t1_days + t2_days + t3_days and t3:
                idx = offset - t1_days - t2_days
                items = [t3[(idx * len(t3) // t3_days) % len(t3)]]
            elif day == days:
                items = []  # mock day
            elif t4:
                items = [t4[(day - 1) % len(t4)]]
            else:
                items = []
            plan.append((day, items))
        return plan

    elif days >= 7:
        # 7-day crash: tier-1 first 3 days, tier-2 next 2, tier-3 day 6, mock day 7.
        plan = []
        t1 = [n for n in ranked if n.get("tier", 4) == 1]
        t2 = [n for n in ranked if n.get("tier", 4) == 2]
        t3 = [n for n in ranked if n.get("tier", 4) == 3]
        per_day = max(1, len(t1) // 3)
        for day in range(1, days + 1):
            if day <= 3:
                items = t1[(day - 1) * per_day:day * per_day]
            elif day <= 5:
                items = t2[(day - 4) * 4:(day - 3) * 4]
            elif day == 6:
                items = t3[:4]
            else:
                items = []  # day 7 = mock cold
            plan.append((day, items))
        return plan

    elif days >= 3:
        # 3-5 day rescue: top tier-1 per day, then mock.
        plan = []
        focus = ranked[:5 * days]
        per_day = max(1, len(focus) // max(1, (days - 1)))
        for day in range(1, days + 1):
            if day < days:
                items = focus[(day - 1) * per_day:day * per_day]
            else:
                items = []  # last day = mock cold + panic-pages
            plan.append((day, items))
        return plan

    else:
        # 1-2 days: emergency tier-1 cram.
        return [(d, ranked[:8] if d == 1 else []) for d in range(1, days + 1)]


def day_label(day: int, total: int, items: list) -> str:
    if day == total:
        return "Day {} (Mock-test cold + final review):".format(day)
    if day == total - 1 and total >= 7:
        return "Day {} (Catch-up + weak-area drill):".format(day)
    return "Day {}:".format(day)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    try:
        days = int(sys.argv[1])
    except ValueError:
        print(f"Bad N-days: {sys.argv[1]!r} — must be a positive integer.")
        return 1
    if days <= 0:
        print(f"Need at least 1 day; got {days}.")
        return 1

    try:
        data = json.loads(ARCH_GRAPH.read_text(encoding="utf-8"))
        nodes = data["nodes"]
    except Exception as e:
        print(f"WARN: could not read ARCHETYPE-GRAPH.json ({e}); using fallback.")
        # Build minimal nodes from fallback
        nodes = []
        for aid in FALLBACK_TIER_1: nodes.append({"id": aid, "label": aid, "tier": 1, "stars": 5, "files": [f"archetypes/{aid}-*.md"]})
        for aid in FALLBACK_TIER_2: nodes.append({"id": aid, "label": aid, "tier": 2, "stars": 3, "files": [f"archetypes/{aid}-*.md"]})
        for aid in FALLBACK_TIER_3: nodes.append({"id": aid, "label": aid, "tier": 3, "stars": 2, "files": [f"archetypes/{aid}-*.md"]})
        for aid in FALLBACK_TIER_4: nodes.append({"id": aid, "label": aid, "tier": 4, "stars": 1, "files": [f"archetypes/{aid}-*.md"]})

    plan = build_plan(nodes, days)

    print(f"Study plan for {days} days")
    print("=" * 70)
    print("Tiers (from archetypes/README.md):")
    print("  Tier 1 - almost certainly tested (A01, A02, A03, A04, A05, A06, A08)")
    print("  Tier 2 - very likely         (A07, A11, A12, A14, A19, A21, A22, A23)")
    print("  Tier 3 - possible            (A09, A10, A13, A15, A16, A24)")
    print("  Tier 4 - low probability     (A17, A18, A20)")
    print("=" * 70)
    print()

    for day, items in plan:
        print(day_label(day, days, items))
        if not items:
            if day == days:
                print("    - Sit the mock test cold (timed 2h, no notes).")
                print("    - Read indexes/MOCK-Q-INDEX.md (marker quirks).")
                print("    - Read quickcheck/QUICKCHECK-ATTACKS.md (60s checklist).")
                print("    - Re-read exam-day/ONE-PAGE-PANIC.md.")
            else:
                print("    - (Float day — catch up on weakest tier-1)")
        else:
            for item in items:
                aid = item["id"]
                stars = "*" * item.get("stars", 0)
                label = item.get("label", aid)
                files = item.get("files", [])
                main_file = files[0] if files else f"archetypes/{aid}-*.md"
                print(f"    - {aid} {stars}  {label}")
                print(f"        Read: {main_file}")
                if len(files) > 1:
                    print(f"        Plus: {files[1]}")
        print()

    print("=" * 70)
    print("After each day:")
    print("  1. Skim quickcheck/<topic>-attacks.md for the family you studied.")
    print("  2. Try 2 sibling problems from question-families/.")
    print("  3. Mark anything you got wrong; revisit on the next floating day.")
    print()
    print(f"See archetypes/README.md for the full ranking and 5-Q composition.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
