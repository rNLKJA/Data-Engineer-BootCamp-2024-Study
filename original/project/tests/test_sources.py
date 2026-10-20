"""Offline tests for the pinned source manifest (pipeline/sources.yml)."""

from __future__ import annotations

import copy

import pytest
import yaml

from pipeline.sources import ManifestError, load_manifest, parse_manifest


@pytest.fixture
def raw_manifest(settings):
    return yaml.safe_load(settings.sources_path.read_text(encoding="utf-8"))


def test_repo_manifest_covers_2012_to_2025_without_gaps(settings):
    manifest = load_manifest(settings.sources_path)
    assert len(manifest.releases) == 10
    assert manifest.years == list(range(2012, 2026))
    assert manifest.provisional_year == 2025
    bundle = manifest.release("sa_crash_2021_2025_as_at_20261009")
    assert bundle.years == [2021, 2022, 2023, 2024, 2025]
    assert bundle.as_at.isoformat() == "2026-10-09"


def test_repo_manifest_urls_point_at_data_sa(settings):
    manifest = load_manifest(settings.sources_path)
    for release in manifest.releases:
        assert release.url.startswith("https://data.sa.gov.au/data/dataset/21386a53-56a1-4edf-bd0b-61ed15f10acf/")
        assert f"/resource/{release.resource_id}/download/{release.file}" in release.url
        assert len(release.sha256) == 64 and release.bytes > 500_000


def test_repo_manifest_records_licence_and_attribution(settings):
    dataset = load_manifest(settings.sources_path).dataset
    assert dataset["licence"] == "CC BY 4.0"
    assert "Department for Infrastructure and Transport" in dataset["attribution"]


def test_overlapping_years_are_rejected(raw_manifest):
    broken = copy.deepcopy(raw_manifest)
    broken["releases"][1]["first_year"] = 2012  # 2013 release now also claims 2012
    with pytest.raises(ManifestError, match="year 2012 appears in both"):
        parse_manifest(broken)


def test_gap_in_years_is_rejected(raw_manifest):
    broken = copy.deepcopy(raw_manifest)
    broken["releases"] = [r for r in broken["releases"] if r["first_year"] != 2016]
    with pytest.raises(ManifestError, match="gap in years \\[2016\\]"):
        parse_manifest(broken)


def test_malformed_checksum_is_rejected(raw_manifest):
    broken = copy.deepcopy(raw_manifest)
    broken["releases"][0]["sha256"] = "not-a-checksum"
    with pytest.raises(ManifestError, match="sha256"):
        parse_manifest(broken)


def test_duplicate_release_ids_are_rejected(raw_manifest):
    broken = copy.deepcopy(raw_manifest)
    broken["releases"][1]["release_id"] = broken["releases"][0]["release_id"]
    with pytest.raises(ManifestError, match="unique"):
        parse_manifest(broken)


def test_missing_keys_are_rejected(raw_manifest):
    broken = copy.deepcopy(raw_manifest)
    del broken["releases"][3]["bytes"]
    with pytest.raises(ManifestError, match="missing"):
        parse_manifest(broken)
