"""Run dbt in-process with dbtRunner and release the DuckDB file afterwards."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from dbt.cli.main import dbtRunner


@dataclass(frozen=True)
class DbtOutcome:
    success: bool
    statuses: dict[str, int]
    exception: BaseException | None


def _close_dbt_duckdb() -> None:
    """dbt-duckdb keeps the warehouse open for the life of the process.

    Close it so the benchmark and export steps (and tests) can open the file
    read-only in the same process.
    """
    from dbt.adapters.duckdb.connections import DuckDBConnectionManager

    environment = getattr(DuckDBConnectionManager, "_ENV", None)
    if environment is not None:
        environment.close()
    DuckDBConnectionManager.close_all_connections()


def run_dbt(args: list[str]) -> DbtOutcome:
    try:
        result = dbtRunner().invoke(args)
    finally:
        _close_dbt_duckdb()
    nodes = getattr(result.result, "results", None) or []
    statuses = Counter(str(getattr(node.status, "value", node.status)) for node in nodes)
    return DbtOutcome(result.success, dict(sorted(statuses.items())), result.exception)
