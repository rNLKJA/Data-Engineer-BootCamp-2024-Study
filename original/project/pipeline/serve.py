"""Serve the pipeline on a weekly schedule to pick up new DIT releases.

    python -m pipeline.serve

This starts a long-running Prefect process (with a local Prefect server it can
also be watched in the UI at http://127.0.0.1:4200 after `prefect server start`).
Every Monday at 03:00 Adelaide time it runs the whole flow. Because releases are
pinned by checksum in pipeline/sources.yml, a run against unchanged sources is a
no-op apart from cache hits; a re-published file fails the checksum step loudly,
which is the signal to review it and update the manifest on purpose.

Documented, not run in CI: CI runs the flow once per push instead.
"""

from __future__ import annotations

from prefect.schedules import Cron

from pipeline.flow import sa_crash_pipeline

WEEKLY_CRON = "0 3 * * 1"
TIMEZONE = "Australia/Adelaide"


def main() -> None:
    sa_crash_pipeline.serve(
        name="weekly-release-check",
        schedule=Cron(WEEKLY_CRON, timezone=TIMEZONE),
        parameters={"stage": "all"},
        tags=["sa-crash", "batch"],
        description="Weekly check for new DIT road crash releases; runs the full pipeline.",
    )


if __name__ == "__main__":
    main()
