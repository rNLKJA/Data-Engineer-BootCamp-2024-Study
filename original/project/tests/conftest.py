"""Shared fixtures for the SA road crash pipeline tests.

Offline tests (default) use the small real-data slice in tests/fixtures and a
local HTTP server, so they never touch data.sa.gov.au. Tests marked
``integration`` read the real warehouse built by ``python -m pipeline.flow``.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import shutil
import sys
import threading
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.config import load_settings  # noqa: E402
from pipeline.sources import Manifest, Release, parse_manifest  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ZIP_DATE = (2026, 10, 20, 0, 0, 0)

# Fixture releases mirror two real ones: a single-year release and the bundle.
FIXTURE_RELEASES = (
    {
        "release_id": "fixture_2019",
        "first_year": 2019,
        "last_year": 2019,
        "as_at": "2021-05-27",
        "resource_id": "fixture-2019",
        "file": "2019_data_sa_as_at_20210527.zip",
        "prefix": "2019",
    },
    {
        "release_id": "fixture_2021_2025",
        "first_year": 2021,
        "last_year": 2025,
        "as_at": "2026-10-09",
        "resource_id": "fixture-2021-2025",
        "file": "2021-2025_data_sa_crash_as_at_20261009.zip",
        "prefix": "2021-2025",
    },
)


def build_zip(prefix: str, target: Path, csv_dir: Path = FIXTURES) -> Path:
    """Zip the three fixture CSVs with fixed timestamps (byte-stable output)."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for table in ("Crash", "Casualty", "Units"):
            name = f"{prefix}_DATA_SA_{table}.csv"
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (csv_dir / name).read_bytes())
    return target


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FakeDIT:
    """A tiny local stand-in for data.sa.gov.au with scriptable responses."""

    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}
        self.failures: dict[str, list[int]] = {}
        self.requests: list[str] = []
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 (http.server API)
                fake.requests.append(self.path)
                queued = fake.failures.get(self.path)
                if queued:
                    status = queued.pop(0)
                    self.send_response(status)
                    self.end_headers()
                    return
                body = fake.files.get(self.path)
                if body is None:
                    self.send_response(404)
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args: object) -> None:
                return

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self.server.server_address[:2]
        return f"http://{host}:{port}"

    def url_template(self) -> str:
        return self.base_url + "/dataset/{package_id}/resource/{resource_id}/download/{file}"


@pytest.fixture
def fake_dit():
    fake = FakeDIT()
    fake.thread.start()
    try:
        yield fake
    finally:
        fake.server.shutdown()
        fake.server.server_close()


@pytest.fixture
def fixture_zips(tmp_path: Path) -> dict[str, Path]:
    out = tmp_path / "fixture_zips"
    return {r["release_id"]: build_zip(r["prefix"], out / r["file"]) for r in FIXTURE_RELEASES}


def fixture_manifest(zips: dict[str, Path], url_template: str = "http://127.0.0.1:9/{package_id}/{resource_id}/{file}") -> Manifest:
    releases = []
    for spec in FIXTURE_RELEASES:
        path = zips[spec["release_id"]]
        entry = {k: v for k, v in spec.items() if k != "prefix"}
        entry.update({"bytes": path.stat().st_size, "sha256": sha256(path)})
        releases.append(entry)
    return parse_manifest(
        {
            "dataset": {"package_id": "fixture-package", "url_template": url_template, "title": "fixture"},
            "releases": releases,
        },
        require_contiguous=False,  # the fixture has 2019 and 2023 only
    )


@pytest.fixture
def manifest(fixture_zips: dict[str, Path]) -> Manifest:
    return fixture_manifest(fixture_zips)


@pytest.fixture
def settings():
    return load_settings()


def release_with(release: Release, **changes: object) -> Release:
    values = {**release.__dict__, **changes}
    if isinstance(values.get("as_at"), str):
        values["as_at"] = dt.date.fromisoformat(values["as_at"])
    return Release(**values)


def copy_fixture_csvs(target: Path) -> Path:
    target.mkdir(parents=True, exist_ok=True)
    for path in FIXTURES.glob("*.csv"):
        shutil.copy(path, target / path.name)
    return target
