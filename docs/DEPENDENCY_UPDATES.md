# Dependency review — 2026-08-12

- Migrated package scripts to pnpm 11.21.0 and created the package lock; no Bun runtime was found.
- Updated the optional image-test dependency from Pillow 11.0.0 to 12.3.0 in CI, local commands,
  error messages, and skill references. Pillow 12.3.0 is the current PyPI release at review time.
- Pillow is isolated behind `uv run --with` or an explicit pip install; the core suite remains
  dependency-free. Review upstream changes before a future major update: <https://pillow.readthedocs.io/en/stable/releasenotes/index.html>.
