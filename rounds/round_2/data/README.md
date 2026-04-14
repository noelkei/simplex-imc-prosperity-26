# Round 2 Data

No data artifacts have been added yet.

Store only round-local data artifacts here. Do not treat data observations as official rules; use `docs/prosperity_wiki/` for facts.

## Folders

- `raw/`: unmodified platform, sample, or run files. Treat this as append-only; do not clean or edit files in place.
- `processed/`: derived or cleaned data created from named sources. Each artifact must link or state its source and processing method.
- `external/`: teammate-provided or non-platform context. These artifacts are non-authoritative and must not be treated as official Prosperity facts.

## Naming

- `raw/`: `<source>_<day_or_run>_<description>.<ext>`
- `processed/`: `derived_<source>_<purpose>.<ext>`
- `external/`: `external_<source>_<description>.<ext>`

## Update Rules

- Link any data used by EDA from `workspace/01_eda/` or `workspace/phase_01_eda_context.md`.
- When processed data changes, update the EDA summary or phase context with the source and method.
- If data contradicts wiki facts, keep the wiki as authoritative and record the data issue as a caveat.
