#!/usr/bin/env python3
"""Regenerates stations.json from the onradio-cover-bridge project's
app/stations.py (the canonical source of truth for the station catalog).

Usage:
    python3 generate.py <path-to-onradio-cover-bridge-checkout> [output-path]

Standard library only - no dependency on the source project's own
requirements (FastAPI, pychromecast, ...), since stations.py itself only
uses stdlib.
"""
from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

# dataclass(slots=True) needs Python 3.10+; strip it so this also runs on
# older interpreters (e.g. a CI runner pinned to an older Python).
_orig_dataclass = dataclasses.dataclass


def _patched_dataclass(*args, **kwargs):
    kwargs.pop("slots", None)
    return _orig_dataclass(*args, **kwargs)


dataclasses.dataclass = _patched_dataclass


def group_for(station_id: str) -> str:
    if station_id.startswith("on-"):
        return "ON Radio"
    if station_id.startswith("80s80s-"):
        return "80s80s"
    if station_id.startswith("sunshine-live"):
        return "Sunshine Live"
    if station_id.startswith("radio-bob-"):
        return "RADIO BOB!"
    if station_id.startswith("ffh-"):
        return "HIT RADIO FFH"
    if station_id.startswith("absolut-"):
        return "Absolut Radio"
    if station_id.startswith("energy-"):
        return "ENERGY"
    return "Other stations"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: generate.py <path-to-onradio-cover-bridge-checkout> [output-path]", file=sys.stderr)
        sys.exit(1)

    source_root = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("stations.json")

    sys.path.insert(0, str(source_root))
    from app.stations import STATIONS  # type: ignore[import-not-found]

    out = []
    for s in STATIONS:
        d = dataclasses.asdict(s)
        out.append({
            "id": d["id"],
            "name": d["name"],
            "group": group_for(d["id"]),
            "homepageUrl": d["homepage_url"],
            "audioUrl": d["audio_url"],
            "audioMode": d["audio_mode"],
            "metadataUrl": d["metadata_url"],
            "metadataMode": d["metadata_mode"],
            "metadataStationLabel": d["metadata_station_label"],
            "metadataStationAliases": list(d["metadata_station_aliases"]),
            "metadataStationId": d["metadata_station_id"],
        })

    output_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(out)} stations to {output_path}")


if __name__ == "__main__":
    main()
