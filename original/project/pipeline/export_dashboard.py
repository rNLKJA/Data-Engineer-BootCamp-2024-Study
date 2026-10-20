"""Export the dbt reporting tables to the JSON that the web dashboard imports.

The output is deterministic: sorted keys, fixed rounding, no timestamps, so
CI can run the pipeline from scratch and ``git diff --exit-code`` the result
against the committed file. Every number on /project comes from this file.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

import duckdb

from pipeline.config import Settings, load_settings
from pipeline.sources import load_manifest

SCHEMA_VERSION = 1
TOP_LGAS = 10


def _rows(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict[str, Any]]:
    cursor = con.execute(sql)
    names = [d[0] for d in cursor.description]
    return [dict(zip(names, row, strict=True)) for row in cursor.fetchall()]


def _clean(value: Any) -> Any:
    """Make DuckDB values JSON-stable: ints stay ints, floats get 2 decimals."""
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return round(value, 2)
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_clean(v) for v in value]
    return value


def build_payload(con: duckdb.DuckDBPyConnection, settings: Settings) -> dict[str, Any]:
    manifest = load_manifest(settings.sources_path)
    dataset = manifest.dataset

    kpis = _rows(con, "select * from rpt_kpis")[0]
    monthly = _rows(
        con,
        """select strftime(crash_month, '%Y-%m') as month, crash_year as year,
                  fatal_crashes, serious_injury_crashes, fsi_crashes, fsi_rolling_12_mean,
                  crashes, casualty_crashes, pdo_regime_id, is_provisional as provisional
           from rpt_monthly_severity order by crash_month""",
    )
    crash_types = _rows(
        con,
        """select crash_type, fsi_rank as rank, fatal_crashes, serious_injury_crashes, fsi_crashes,
                  crashes, casualty_crashes, fsi_pct_of_casualty_crashes, fatal_pct_of_fsi, pct_of_all_fsi
           from rpt_crash_type_severity order by fsi_rank""",
    )
    annual = _rows(
        con,
        """select crash_year as year, fatalities, admitted_to_hospital, fatal_crashes,
                  serious_injury_crashes, fsi_crashes, crashes, is_provisional as provisional
           from rpt_annual_people order by crash_year""",
    )
    regions = _rows(
        con,
        """select stats_area, crashes, casualty_crashes, fsi_crashes, fatal_crashes,
                  serious_injury_crashes, fatalities, fsi_pct_of_casualty_crashes, pct_of_all_fsi
           from rpt_region_fsi order by fsi_crashes desc, stats_area""",
    )
    # Only councils are ranked. Crashes with no council recorded and DIT's
    # unincorporated-area groupings are exported separately, not ranked.
    lgas = _rows(
        con,
        f"""select fsi_rank as rank, lga_name, main_stats_area, fsi_crashes, fatal_crashes,
                   serious_injury_crashes, crashes, fsi_pct_of_casualty_crashes
            from rpt_lga_fsi where is_council order by fsi_rank limit {TOP_LGAS}""",
    )
    non_councils = _rows(
        con,
        """select lga_name, is_unknown, main_stats_area, stats_areas, fsi_crashes, fatal_crashes,
                  serious_injury_crashes, crashes
           from rpt_lga_fsi where not is_council order by is_unknown desc, fsi_crashes desc, lga_name""",
    )
    lga_fsi_total = con.execute("select sum(fsi_crashes) from rpt_lga_fsi").fetchone()[0]
    regimes = _rows(
        con,
        """select regime_id, valid_from, valid_to, pdo_rule_summary as summary
           from pdo_reporting_regimes order by regime_id""",
    )

    # Reconcile before writing: every tile must add up to the same totals.
    checks = {
        "monthly FSI": sum(r["fsi_crashes"] for r in monthly),
        "crash type FSI": sum(r["fsi_crashes"] for r in crash_types),
        "annual FSI": sum(r["fsi_crashes"] for r in annual),
        "region FSI": sum(r["fsi_crashes"] for r in regions),
        "council area FSI": lga_fsi_total,
    }
    for name, total in checks.items():
        if total != kpis["fsi_crashes"]:
            raise ValueError(f"{name} total {total} does not match rpt_kpis.fsi_crashes {kpis['fsi_crashes']}")
    if sum(r["fatalities"] for r in annual) != kpis["fatalities"]:
        raise ValueError("annual fatalities do not match rpt_kpis.fatalities")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "title": "Serious road crashes in South Australia",
        "question": (
            "Where, when and how do the most serious road crashes happen in South Australia, "
            f"{kpis['first_year']}-{kpis['last_year']}?"
        ),
        "source": {
            "title": dataset["title"],
            "publisher": dataset["publisher"],
            "page": dataset["page"],
            "licence": dataset["licence"],
            "licence_url": dataset["licence_url"],
            "attribution": dataset["attribution"],
            "releases": [
                {
                    "release_id": r.release_id,
                    "first_year": r.first_year,
                    "last_year": r.last_year,
                    "as_at": r.as_at.isoformat(),
                    "file": r.file,
                    "sha256": r.sha256,
                }
                for r in manifest.releases
            ],
        },
        "coverage": {
            "first_year": kpis["first_year"],
            "last_year": kpis["last_year"],
            "first_month": monthly[0]["month"],
            "last_month": monthly[-1]["month"],
            "months": len(monthly),
            "provisional_year": manifest.provisional_year,
        },
        "kpis": {
            key: kpis[key]
            for key in (
                "crashes", "casualty_crashes", "fsi_crashes", "fatal_crashes", "casualties",
                "fatalities", "serious_injuries", "council_areas", "crashes_without_lga",
            )
        },  # fmt: skip
        "pdo_regimes": regimes,
        "tiles": {
            "crash_type_fsi": crash_types,
            "monthly_fsi": monthly,
            "annual_people": annual,
            "regions": regions,
            "top_lgas": lgas,
            "non_council_lgas": non_councils,
        },
        "generated_by": "original/project/pipeline/export_dashboard.py from dbt reporting models",
    }
    return _clean(payload)


def render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def export(settings: Settings | None = None, target: Path | None = None) -> Path:
    settings = settings or load_settings()
    target = Path(target or settings.dashboard_json)
    con = duckdb.connect(str(settings.warehouse_path), read_only=True)
    try:
        payload = build_payload(con, settings)
    finally:
        con.close()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(payload), encoding="utf-8")
    kpis = payload["kpis"]
    print(
        f"exported {payload['coverage']['months']} months, {len(payload['tiles']['crash_type_fsi'])} crash types; "
        f"crashes={kpis['crashes']} fsi_crashes={kpis['fsi_crashes']} fatalities={kpis['fatalities']} "
        f"serious_injuries={kpis['serious_injuries']}"
    )
    print(summarise(payload))
    return target


def summarise(payload: dict[str, Any]) -> str:
    """Plain-text digest of the exported tiles, printed into the run log."""
    tiles = payload["tiles"]
    lines = ["", "Dashboard summary (from the exported JSON)", "FSI crashes by crash type:"]
    for row in tiles["crash_type_fsi"]:
        lines.append(
            f"  {row['rank']:>2}. {row['crash_type']:<28} fsi={row['fsi_crashes']:>5} fatal={row['fatal_crashes']:>4} "
            f"serious={row['serious_injury_crashes']:>5} share_of_fsi={row['pct_of_all_fsi']:>5}% "
            f"crashes={row['crashes']:>6} fsi_pct_of_casualty_crashes={row['fsi_pct_of_casualty_crashes']}%"
        )
    lines.append("People per year (casualty rows):")
    for row in tiles["annual_people"]:
        flag = " provisional" if row["provisional"] else ""
        lines.append(
            f"  {row['year']}: lives_lost={row['fatalities']:>3} admitted_to_hospital={row['admitted_to_hospital']:>4} "
            f"fsi_crashes={row['fsi_crashes']:>4} crashes={row['crashes']:>6}{flag}"
        )
    lines.append("FSI crashes by statistical area:")
    for row in tiles["regions"]:
        lines.append(
            f"  {row['stats_area']:<13} fsi={row['fsi_crashes']:>5} share_of_fsi={row['pct_of_all_fsi']}% "
            f"crashes={row['crashes']:>6} fsi_pct_of_casualty_crashes={row['fsi_pct_of_casualty_crashes']}%"
        )
    lines.append("Top council areas by FSI crashes (councils only):")
    for row in tiles["top_lgas"]:
        lines.append(
            f"  {row['rank']:>2}. {row['lga_name']:<32} fsi={row['fsi_crashes']:>4} fatal={row['fatal_crashes']:>3} "
            f"crashes={row['crashes']:>6} main_area={row['main_stats_area']}"
        )
    lines.append("Not ranked (not a council):")
    for row in tiles["non_council_lgas"]:
        lines.append(
            f"      {row['lga_name']:<32} fsi={row['fsi_crashes']:>4} fatal={row['fatal_crashes']:>3} "
            f"crashes={row['crashes']:>6} main_area={row['main_stats_area']} stats_areas={row['stats_areas']}"
        )
    monthly = tiles["monthly_fsi"]
    peak = max(monthly, key=lambda r: (r["fsi_crashes"], r["month"]))
    rolling = [r for r in monthly if r["fsi_rolling_12_mean"] is not None]
    low = min(rolling, key=lambda r: (r["fsi_rolling_12_mean"], r["month"]))
    high = max(rolling, key=lambda r: (r["fsi_rolling_12_mean"], r["month"]))
    lines.append(
        f"Monthly FSI: peak month {peak['month']} ({peak['fsi_crashes']}); 12-month mean lowest "
        f"{low['fsi_rolling_12_mean']} (to {low['month']}), highest {high['fsi_rolling_12_mean']} (to {high['month']})"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    export()
