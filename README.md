# Radio Stations

Auto-updated JSON catalog of internet radio stations, generated from
[onradio-cover-bridge](https://github.com/TBR-BRD/onradio-cover-bridge)'s
`app/stations.py` (the canonical source of truth - this repo never edits
stations by hand).

## Why this repo exists

Two independent apps need the same station list:

- [onradio-cover-bridge](https://github.com/TBR-BRD/onradio-cover-bridge) -
  the Raspberry Pi radio/display project. It already has `stations.py`
  locally and does **not** need to fetch this file; it's the source, not a
  consumer.
- [googletv-musicplayer](https://github.com/TBR-BRD/googletv-musicplayer) -
  the standalone Google TV / Android TV app. It has no Python backend of its
  own, so it fetches `stations.json` from this repo at startup (with a
  bundled snapshot as an offline fallback).

Keeping the catalog here means the TV app picks up new or changed stations
automatically, without needing an app update.

## How it stays up to date

`.github/workflows/update-stations.yml` runs on the **1st of every month**
(the closest reliable approximation of "every 4 weeks" that plain cron
syntax supports) and on manual trigger (Actions tab -> "Update station
catalog" -> "Run workflow"). It checks out `onradio-cover-bridge`, re-runs
`generate.py` against its current `app/stations.py`, and commits
`stations.json` here only if it actually changed. No secrets or
cross-repo tokens are needed - the workflow only ever reads the other
(public) repo and writes to its own, using the default `GITHUB_TOKEN`.

## Consuming this data

```
https://raw.githubusercontent.com/TBR-BRD/radiostations/main/stations.json
```

Each entry mirrors the fields of `onradio-cover-bridge`'s `Station`
dataclass, plus a derived `group` field (used for the TV app's
category picker):

```json
{
  "id": "on-radio",
  "name": "ON Radio",
  "group": "ON Radio",
  "homepageUrl": "https://onradio.de/",
  "audioUrl": "https://0n-radio.radionetz.de/0n-radio.mp3",
  "audioMode": "direct",
  "metadataUrl": "https://www.0nradio.com/now_playing/0n-radio.json",
  "metadataMode": "0nradio_json",
  "metadataStationLabel": null,
  "metadataStationAliases": [],
  "metadataStationId": null
}
```

## Regenerating manually

```bash
git clone https://github.com/TBR-BRD/onradio-cover-bridge.git
python3 generate.py onradio-cover-bridge stations.json
```

Standard library only - no dependency on `onradio-cover-bridge`'s own
requirements (FastAPI, pychromecast, ...), since `stations.py` itself only
uses stdlib.
