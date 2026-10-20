"""Load and validate the pinned source manifest (``sources.yml``)."""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ManifestError(ValueError):
    """The source manifest is malformed or inconsistent."""


@dataclass(frozen=True)
class Release:
    """One DIT zip release covering one or more calendar years."""

    release_id: str
    first_year: int
    last_year: int
    as_at: dt.date
    resource_id: str
    file: str
    bytes: int
    sha256: str
    url: str

    @property
    def years(self) -> list[int]:
        return list(range(self.first_year, self.last_year + 1))


@dataclass(frozen=True)
class Manifest:
    dataset: dict[str, Any]
    releases: list[Release]

    @property
    def years(self) -> list[int]:
        return [year for release in self.releases for year in release.years]

    @property
    def provisional_year(self) -> int:
        """The newest year in the data. DIT still revises it, so label it provisional."""
        return max(self.years)

    def release(self, release_id: str) -> Release:
        for release in self.releases:
            if release.release_id == release_id:
                return release
        raise KeyError(release_id)


def _as_date(value: Any, release_id: str) -> dt.date:
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError as exc:
        raise ManifestError(f"{release_id}: as_at {value!r} is not an ISO date") from exc


def parse_manifest(raw: dict[str, Any], *, require_contiguous: bool = True) -> Manifest:
    """Validate a manifest dictionary and return typed releases.

    Checks: required keys, SHA-256 format, positive sizes, unique ids, no year
    claimed by two releases, and (unless ``require_contiguous`` is False, which
    the small test fixture needs) no gap between the first and last year.
    """
    if not isinstance(raw, dict) or "dataset" not in raw or "releases" not in raw:
        raise ManifestError("manifest needs top-level 'dataset' and 'releases' keys")
    dataset = raw["dataset"]
    template = dataset.get("url_template")
    package_id = dataset.get("package_id")
    if not template or not package_id:
        raise ManifestError("dataset needs 'url_template' and 'package_id'")

    required = ("release_id", "first_year", "last_year", "as_at", "resource_id", "file", "bytes", "sha256")
    releases: list[Release] = []
    for entry in raw["releases"]:
        missing = [key for key in required if key not in entry]
        if missing:
            raise ManifestError(f"release {entry.get('release_id', '?')} is missing {missing}")
        release_id = str(entry["release_id"])
        first, last = int(entry["first_year"]), int(entry["last_year"])
        if first > last:
            raise ManifestError(f"{release_id}: first_year {first} is after last_year {last}")
        sha = str(entry["sha256"]).lower()
        if not SHA256_RE.match(sha):
            raise ManifestError(f"{release_id}: sha256 must be 64 lowercase hex characters")
        size = int(entry["bytes"])
        if size <= 0:
            raise ManifestError(f"{release_id}: bytes must be positive")
        releases.append(
            Release(
                release_id=release_id,
                first_year=first,
                last_year=last,
                as_at=_as_date(entry["as_at"], release_id),
                resource_id=str(entry["resource_id"]),
                file=str(entry["file"]),
                bytes=size,
                sha256=sha,
                url=template.format(
                    package_id=package_id,
                    resource_id=entry["resource_id"],
                    file=entry["file"],
                ),
            )
        )

    if not releases:
        raise ManifestError("manifest lists no releases")
    ids = [r.release_id for r in releases]
    if len(set(ids)) != len(ids):
        raise ManifestError("release_id values must be unique")

    releases.sort(key=lambda r: r.first_year)
    seen: dict[int, str] = {}
    for release in releases:
        for year in release.years:
            if year in seen:
                raise ManifestError(
                    f"year {year} appears in both {seen[year]} and {release.release_id}"
                )
            seen[year] = release.release_id
    years = sorted(seen)
    if require_contiguous and years != list(range(years[0], years[-1] + 1)):
        gaps = sorted(set(range(years[0], years[-1] + 1)) - set(years))
        raise ManifestError(f"releases leave a gap in years {gaps}")
    return Manifest(dataset=dataset, releases=releases)


def load_manifest(path: Path) -> Manifest:
    with Path(path).open(encoding="utf-8") as handle:
        return parse_manifest(yaml.safe_load(handle))
