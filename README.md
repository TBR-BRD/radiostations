# Radio Stations

The canonical catalog of internet radio stations behind two apps:

- [onradio-cover-bridge](https://github.com/TBR-BRD/onradio-cover-bridge) -
  the Raspberry Pi radio/display project.
- [googletv-musicplayer](https://github.com/TBR-BRD/googletv-musicplayer) -
  the standalone Google TV / Android TV app.

Both fetch `stations.json` from this repo at startup (each keeping its own
cached/bundled copy as an offline fallback if this repo is unreachable).
Neither one defines the station list itself anymore - **this repo is the
single source of truth**.

## Editing the station list

Edit [`stations_source.py`](stations_source.py) - a plain Python file
defining `Station` entries (and the helper functions that generate the
large per-provider families like RADIO BOB!, 80s80s, ENERGY, etc. from
compact tuples, rather than repeating near-identical station defintions by
hand). Then either:

- push to `main` - the GitHub Action below regenerates `stations.json`
  automatically, or
- run `python3 generate.py` locally and commit the result yourself.

## How it stays up to date

`.github/workflows/update-stations.yml` regenerates `stations.json` from
`stations_source.py` on every push that touches `stations_source.py` or
`generate.py`, plus a monthly safety-net run (1st of the month, 04:00 UTC)
and a manual trigger (Actions tab -> "Update station catalog" -> "Run
workflow") in case a push-triggered run was ever missed. It commits
`stations.json` only if it actually changed, using the default
`GITHUB_TOKEN` - no secrets needed.

## Consuming this data

```
https://raw.githubusercontent.com/TBR-BRD/radiostations/main/stations.json
```

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

`group` is derived from the station `id`'s prefix (see `group_for()` in
`generate.py`) and used by the TV app's category picker.

## Regenerating manually

```bash
git clone https://github.com/TBR-BRD/radiostations.git
cd radiostations
python3 generate.py
```

Standard library only, no dependencies to install.

## History

This catalog originally lived in `onradio-cover-bridge`'s
`app/stations.py` and this repo just mirrored it. It was moved here to be
the actual source, with `onradio-cover-bridge` switched to fetching from
here instead (with its own local cache/fallback) - see that project's
`app/stations.py` for the consumer side.
