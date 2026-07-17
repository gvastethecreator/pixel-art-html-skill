# Project library contract

Managed builds belong to the project where the skill is invoked, or to `--project-root` when supplied:

```text
pixel-art/
├── index.html
├── catalog.json
└── YYYY/MM/NNN-slug/
    ├── iteration.json
    └── artifact files
```

- Treat every chronological folder as one immutable request/iteration.
- Allocate `NNN` from the highest existing number in that month.
- Keep every artifact standalone; never import runtime files from siblings or the hub.
- Store factual title, kind, timestamp, sizes, source kind, entry, and thumbnail in `iteration.json`.
- Preserve `kind: pack` and `source_kind: pack` for same-size asset sets; select the first 32x32 item as thumbnail when present, otherwise the first manifest item.
- Rebuild the root hub from iteration metadata after every managed build.
- Interpret automatic loading as build-time catalog regeneration. Browsers cannot safely enumerate arbitrary `file://` folders.
- Use `hub --project-root <project>` to regenerate after metadata is moved or edited manually.
- Use direct `--output` only when the user explicitly wants an unindexed destination.
