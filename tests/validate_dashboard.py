#!/usr/bin/env python3
"""Static validation helpers for the Grafana dashboard JSON."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, List

REQUIRED_VARIABLES = ("job", "node", "port")
REQUIRED_DATASOURCES = ("prometheus",)


def load_dashboard(path: Path) -> dict:
    """Load the dashboard JSON file and return the parsed dict."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:  # pragma: no cover - fatal error path
        raise SystemExit(f"Failed to parse {path}: {exc}") from exc


def validate_variables(templating_list: Iterable[dict]) -> List[str]:
    errors: List[str] = []
    available = {item.get("name") for item in templating_list}
    for required in REQUIRED_VARIABLES:
        if required not in available:
            errors.append(
                f"Missing required dashboard variable '{required}'."
            )
    return errors


def validate_panels(panels: Iterable[dict]) -> List[str]:
    errors: List[str] = []
    for panel in panels:
        # Row panels only group other panels and do not have PromQL targets.
        if panel.get("type") == "row":
            continue
        targets = panel.get("targets", [])
        if not targets:
            errors.append(
                f"Panel '{panel.get('title', 'unnamed')}' does not define any targets."
            )
    return errors


def validate_datasources(requirements: Iterable[dict]) -> List[str]:
    errors: List[str] = []
    available = {item.get("id", "").lower() for item in requirements}
    for required in REQUIRED_DATASOURCES:
        if required not in available:
            errors.append(
                f"Required datasource '{required}' is not declared in '__requires'."
            )
    return errors


def validate_dashboard(dashboard: dict) -> List[str]:
    errors: List[str] = []

    if not dashboard.get("panels"):
        errors.append("Dashboard must define at least one panel.")
    else:
        errors.extend(validate_panels(dashboard["panels"]))

    templating = dashboard.get("templating", {}).get("list", [])
    errors.extend(validate_variables(templating))

    requirements = dashboard.get("__requires", [])
    errors.extend(validate_datasources(requirements))

    schema_version = dashboard.get("schemaVersion")
    if not isinstance(schema_version, int) or schema_version < 16:
        errors.append(
            "Dashboard 'schemaVersion' must be an integer >= 16 for modern Grafana."
        )

    return errors


def run_validation(path: Path) -> None:
    dashboard = load_dashboard(path)
    errors = validate_dashboard(dashboard)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        raise SystemExit(1)
    print(f"Dashboard validation successful: {path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "dashboard",
        nargs="?",
        default="10619_rev2.json",
        help="Path to the Grafana dashboard JSON file to validate",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = Path(args.dashboard)
    if not path.exists():
        raise SystemExit(f"Dashboard file not found: {path}")
    run_validation(path)


if __name__ == "__main__":
    main()
