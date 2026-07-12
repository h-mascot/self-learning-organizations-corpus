#!/usr/bin/env python3
"""Generate the canonical, cross-wave saturation aggregation and dashboard."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "metadata" / "saturation.json"
DASHBOARD = ROOT / "research" / "saturation-dashboard.md"
STATISTICS = ROOT / "metadata" / "statistics.json"
THRESHOLD = 0.05


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def ordinary_rounds(path: Path, wave: str, default_channel: str | None = None) -> list[dict]:
    result = []
    for original in jsonl(path):
        row = dict(original)
        if default_channel and "channel" not in row:
            row["channel"] = default_channel
        candidates = row.get("retrieved_candidates", row.get("result_count", 0))
        rate = row.get("net_new_accepted_unique_rate", row.get("net_new_accepted_rate", 0.0))
        if isinstance(rate, dict):
            rate = rate["value"]
        result.append(canonical(row, wave, candidates, float(rate)))
    return result


def native_four(root: Path) -> list[dict]:
    result = []
    for channel in ("x", "reddit", "substack", "youtube"):
        grouped: dict[int, list[dict]] = defaultdict(list)
        for row in jsonl(root / "research" / "native-saturation-4" / f"{channel}.jsonl"):
            grouped[row["round"]].append(row)
        for number, rows in sorted(grouped.items()):
            dispositions = Counter(row["disposition"] for row in rows)
            first = rows[0]
            accepted = dispositions["accepted"]
            blocked = dispositions["blocked"]
            complete = all(any(word in row["access_evidence"].lower() for word in ("complete", "full", "reviewed")) for row in rows)
            raw = {
                "channel": channel, "round": number, "query_family": first["query_family"],
                "backend": first["backend"], "query": first["query"], "searched_at": first["searched_at"],
                "accepted": accepted, "rejected": dispositions["rejected"], "duplicates": dispositions["duplicate"],
                "blocked": blocked, "saturation_eligible": complete and not blocked and accepted / len(rows) < THRESHOLD,
                "material_difference": first["access_path"],
                "eligibility_note": "Derived from complete candidate-level native/public review.",
            }
            result.append(canonical(raw, "native-saturation-4", len(rows), accepted / len(rows)))
    return result


def canonical(row: dict, wave: str, candidates: int, rate: float) -> dict:
    return {
        "wave": wave, "channel": row["channel"], "round": row["round"],
        "searched_at": row["searched_at"], "query_family": row["query_family"],
        "backend": row["backend"], "query": row["query"],
        "material_difference": row.get("material_difference", row.get("eligibility_note", "")),
        "candidate_count": candidates, "accepted": row.get("accepted", 0),
        "rejected": row.get("rejected", 0), "duplicates": row.get("duplicates", 0),
        "blocked": row.get("blocked", 0), "novelty_rate": rate,
        "eligible": bool(row.get("saturation_eligible")),
        "eligibility_note": row.get("eligibility_note", ""),
    }


def build(root: Path = ROOT) -> tuple[dict, str, list[str]]:
    rounds = []
    inputs = (
        ("initial-saturation", "research/saturation/rounds.jsonl"),
        ("web-media-followup", "research/web-media-followup/rounds.jsonl"),
        ("native-saturation-3", "research/native-saturation-3/rounds.jsonl"),
        ("web-media-saturation-4", "research/web-media-saturation-4/rounds.jsonl"),
        ("academic-saturation-5", "research/academic-saturation-5/rounds.jsonl"),
        ("academic-saturation-6", "research/academic-saturation-6/rounds.jsonl"),
    )
    for wave, relative in inputs:
        rounds.extend(ordinary_rounds(root / relative, wave, "academic" if wave.startswith("academic-saturation-") else None))
    rounds.extend(native_four(root))
    rounds.sort(key=lambda row: (row["searched_at"], row["wave"], row["channel"], row["round"]))

    errors: list[str] = []
    proof: dict[str, list[dict]] = {}
    by_channel: dict[str, list[dict]] = defaultdict(list)
    for row in rounds:
        by_channel[row["channel"]].append(row)
        if row["eligible"] and (not row["candidate_count"] or row["blocked"] or row["novelty_rate"] >= THRESHOLD):
            errors.append(f"ineligible evidence marked eligible: {row['wave']}/{row['channel']}/{row['round']}")
    for channel, items in by_channel.items():
        for wave in dict.fromkeys(row["wave"] for row in items):
            eligible = [row for row in items if row["wave"] == wave and row["eligible"]]
            eligible.sort(key=lambda row: row["round"])
            for index in range(len(eligible) - 2):
                run = eligible[index:index + 3]
                if ([row["round"] for row in run] == list(range(run[0]["round"], run[0]["round"] + 3))
                        and len({row["query_family"] for row in run}) == 3
                        and all(row["material_difference"] for row in run)):
                    proof[channel] = run
    channels = {}
    for channel, items in sorted(by_channel.items()):
        channels[channel] = {
            "round_count": len(items), "candidate_count": sum(row["candidate_count"] for row in items),
            "accepted": sum(row["accepted"] for row in items), "rejected": sum(row["rejected"] for row in items),
            "duplicates": sum(row["duplicates"] for row in items), "blocked": sum(row["blocked"] for row in items),
            "eligible_round_count": sum(row["eligible"] for row in items),
            "saturated": channel in proof,
            "qualifying_rounds": [{"wave": row["wave"], "round": row["round"], "query_family": row["query_family"],
                                    "candidate_count": row["candidate_count"], "novelty_rate": row["novelty_rate"],
                                    "blocked": row["blocked"]} for row in proof.get(channel, [])],
        }
    saturated = sorted(proof)
    data = {
        "schema_version": 1, "threshold": THRESHOLD,
        "rule": "three consecutive eligible rounds in one wave, with materially distinct query families and less than 5% net-new accepted unique sources",
        "input_waves": [wave for wave, _ in inputs] + ["native-saturation-4"],
        "round_count": len(rounds), "candidate_count": sum(row["candidate_count"] for row in rounds),
        "eligible_round_count": sum(row["eligible"] for row in rounds),
        "saturated_channels": saturated, "unsaturated_channels": sorted(set(channels) - set(saturated)),
        "academic_status": ("met: wave 6 has three consecutive eligible post-acceptance rounds below 5%"
                            if "academic" in proof else "unmet: no qualifying three-round academic sequence"),
        "channels": channels, "rounds": rounds,
    }
    lines = ["# Canonical Saturation Dashboard", "", "Generated from every saturation wave; raw lane ledgers remain authoritative evidence.", "",
             f"- Qualifying channels: **{len(saturated)}** — {', '.join(saturated) if saturated else 'none'}",
             f"- Academic: **{'met' if 'academic' in proof else 'unmet'}** — {data['academic_status'].split(': ', 1)[1]}",
             f"- Canonical rounds: **{data['round_count']}**; candidates reviewed: **{data['candidate_count']}**", "",
             "| Channel | Rounds | Candidates | Eligible | Blocked | Three-round proof |", "| --- | ---: | ---: | ---: | ---: | --- |"]
    for channel, item in channels.items():
        evidence = ", ".join(f"{x['wave']} r{x['round']} ({x['novelty_rate']:.1%})" for x in item["qualifying_rounds"]) or "unmet"
        lines.append(f"| {channel} | {item['round_count']} | {item['candidate_count']} | {item['eligible_round_count']} | {item['blocked']} | {evidence} |")
    return data, "\n".join(lines) + "\n", errors


def render_statistics(path: Path, data: dict) -> str:
    statistics = json.loads(path.read_text())
    statistics["saturation"] = {
        "threshold": data["threshold"], "round_count": data["round_count"],
        "candidate_count": data["candidate_count"], "eligible_round_count": data["eligible_round_count"],
        "saturated_channels": data["saturated_channels"], "unsaturated_channels": data["unsaturated_channels"],
        "academic_status": data["academic_status"],
    }
    return json.dumps(statistics, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    data, markdown, errors = build()
    if errors:
        print("\n".join(errors)); return 1
    rendered = json.dumps(data, indent=2, sort_keys=True) + "\n"
    statistics = render_statistics(STATISTICS, data)
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, expected in ((OUTPUT, rendered), (DASHBOARD, markdown), (STATISTICS, statistics)) if not path.exists() or path.read_text() != expected]
        if stale: print("stale generated artifacts: " + ", ".join(stale)); return 1
    else:
        OUTPUT.write_text(rendered); DASHBOARD.write_text(markdown); STATISTICS.write_text(statistics)
    print(f"canonical saturation: {len(data['saturated_channels'])} qualifying, academic {'met' if 'academic' in data['saturated_channels'] else 'unmet'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
