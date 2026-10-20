"""Integration tests: the dashboard JSON reconciles with the warehouse."""

from __future__ import annotations

import datetime as dt
import json

import duckdb
import pytest

from pipeline.export_dashboard import export

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def committed(settings_module):
    return json.loads(settings_module.dashboard_json.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def settings_module():
    from pipeline.config import load_settings

    return load_settings()


@pytest.fixture(scope="module")
def con(settings_module):
    connection = duckdb.connect(str(settings_module.warehouse_path), read_only=True)
    yield connection
    connection.close()


def test_dashboard_has_at_least_two_tiles(committed):
    tiles = committed["tiles"]
    assert len(tiles["crash_type_fsi"]) == 13  # categorical tile: every DIT crash type
    assert len(tiles["monthly_fsi"]) == 168  # temporal tile: Jan 2012 to Dec 2025
    assert len(tiles) >= 2


def test_months_are_continuous_from_2012_to_2025(committed):
    months = [row["month"] for row in committed["tiles"]["monthly_fsi"]]
    expected = [f"{y}-{m:02d}" for y in range(2012, 2026) for m in range(1, 13)]
    assert months == expected
    assert committed["coverage"]["first_month"] == "2012-01"
    assert committed["coverage"]["last_month"] == "2025-12"


def test_rolling_mean_is_the_trailing_twelve_month_average(committed):
    rows = committed["tiles"]["monthly_fsi"]
    assert all(r["fsi_rolling_12_mean"] is None for r in rows[:11])
    for i in range(11, len(rows)):
        window = [r["fsi_crashes"] for r in rows[i - 11 : i + 1]]
        assert rows[i]["fsi_rolling_12_mean"] == round(sum(window) / 12, 2)


def test_totals_reconcile_with_the_warehouse(committed, con):
    kpis = committed["kpis"]
    crashes, fsi, fatal, fats, si, cas = con.execute(
        """select count(*), count(*) filter (where is_fsi), count(*) filter (where severity_code = 4),
                  sum(total_fats), sum(total_si), sum(total_cas) from fct_crashes"""
    ).fetchone()
    assert (kpis["crashes"], kpis["fsi_crashes"], kpis["fatal_crashes"]) == (crashes, fsi, fatal)
    assert (kpis["fatalities"], kpis["serious_injuries"], kpis["casualties"]) == (fats, si, cas)
    tiles = committed["tiles"]
    assert sum(r["fsi_crashes"] for r in tiles["monthly_fsi"]) == fsi
    assert sum(r["fsi_crashes"] for r in tiles["crash_type_fsi"]) == fsi
    assert sum(r["fatal_crashes"] + r["serious_injury_crashes"] for r in tiles["crash_type_fsi"]) == fsi
    assert sum(r["fatalities"] for r in tiles["annual_people"]) == fats
    assert sum(r["crashes"] for r in tiles["regions"]) == crashes


def test_council_ranking_holds_only_councils(committed, con):
    tiles = committed["tiles"]
    top = tiles["top_lgas"]
    assert [r["rank"] for r in top] == list(range(1, 11))
    assert not any("UNINCORP" in r["lga_name"] for r in top)
    unknown = [r for r in tiles["non_council_lgas"] if r["is_unknown"]]
    assert [r["lga_name"] for r in unknown] == ["UNINCORPORATED OR UNKNOWN"]
    assert unknown[0]["crashes"] == committed["kpis"]["crashes_without_lga"]
    non_council_fsi = con.execute(
        "select count(*) filter (where is_fsi) from fct_crashes where lga_name like '%UNINCORP%'"
    ).fetchone()[0]
    assert sum(r["fsi_crashes"] for r in tiles["non_council_lgas"]) == non_council_fsi


def test_crash_types_are_sorted_by_fsi(committed):
    fsi = [r["fsi_crashes"] for r in committed["tiles"]["crash_type_fsi"]]
    assert fsi == sorted(fsi, reverse=True)


def test_only_the_latest_year_is_provisional(committed):
    flagged = {r["year"] for r in committed["tiles"]["annual_people"] if r["provisional"]}
    assert flagged == {committed["coverage"]["provisional_year"]} == {2025}
    assert all(r["provisional"] == r["month"].startswith("2025") for r in committed["tiles"]["monthly_fsi"])


def test_export_is_deterministic_and_matches_the_committed_file(tmp_path, settings_module):
    first = export(settings_module, tmp_path / "a.json").read_bytes()
    second = export(settings_module, tmp_path / "b.json").read_bytes()
    assert first == second
    assert first == settings_module.dashboard_json.read_bytes()
    assert b"generated_at" not in first


def test_attribution_and_release_dates_travel_with_the_data(committed):
    source = committed["source"]
    assert source["licence"] == "CC BY 4.0"
    assert source["attribution"].startswith("Road Crash Data, Department for Infrastructure and Transport")
    assert {r["as_at"] for r in source["releases"]} == {"2021-05-27", "2026-10-09"}
    assert all(dt.date.fromisoformat(r["valid_from"]) for r in committed["pdo_regimes"])


def test_2023_matches_the_published_road_safety_annual_report(committed):
    """External cross-check, not a target the pipeline was tuned to.

    DIT's Road Safety Action Plan 2023-2025 Annual Report 2023
    (https://dit.sa.gov.au/thinkroadsafety/road-safety-strategy/action-plan-2023-2025/annual-report-2023,
    read on 2026-10-20) says 117 lives were lost and 824 people were seriously
    injured on South Australian roads in 2023. The pipeline counts the same two
    figures from casualty rows (Injury Extent = Fatal / Admitted to Hospital).
    """
    row = next(r for r in committed["tiles"]["annual_people"] if r["year"] == 2023)
    assert (row["fatalities"], row["admitted_to_hospital"]) == (117, 824)
