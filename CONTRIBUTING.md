# Contributing

Keep changes focused on the existing exact-grid and review contracts. Public documentation uses American English.

## Check a change

Use the pnpm version declared in `package.json`. Run one sufficient gate from the repository root:

- `pnpm run check:core`: dependency-free Python behavior and package validation.
- `pnpm run check:full`: the complete gate, including Pillow-dependent conversion, packing, and reference media checks. Install `pillow==12.3.0` first.
- `pnpm run validate`: package structure and local documentation links, suitable for prose-only changes.

The [VS Code tasks](.vscode/tasks.json) run these commands with the workspace root as their working directory. They do not install dependencies. Add a focused regression only for a meaningful failure that existing coverage does not protect.

When source classification or image packing changes, run the existing deterministic benchmark separately:

```powershell
python ./SKILLS/pixel-art-html/scripts/benchmark_small_grids.py --output ./.scratch/small-grid-benchmark
```

Pillow must already be installed. Benchmark measurements establish reconstruction behavior, not artistic quality. Do not start model evaluations as an incidental check.

## Preserve the contracts

- Keep dimensions, palette limits, exact RGBA parity, editable sources, and provenance intact.
- Preserve the one-pass default. Variants require an explicit request; an artistic repair is one requested bounded intervention.
- Stage reviews must record actual inspection. Failed advancement means an incomplete draft, not an invented approval.
- Promotion to `representative` requires a non-builder review of the exact final grid. `production-candidate` requires the owner's review.
- Keep private reference corpora, full articles, sampled boards, generated drafts, and experiment logs outside the public tree.

Shipped examples and evaluation fixtures are reproducible historical evidence. Preserve their pixels and verdicts. Changes to artistic guidance need source evidence or an observed workflow result; passing tests cannot establish better art.

## Navigate the source

The generated [code map](docs/codemap/codemap.md) links modules, direct calls, and related tests. Its [interactive view](docs/codemap/codemap.html) exposes the same source evidence and unresolved references. Static reachability does not prove runtime behavior or test coverage. The analyzer leaves some member calls unresolved and can label sibling Python imports as external modules. Use the source for those relationships.

When module boundaries or dependencies change, refresh `codemap.json`, `codemap.md`, `codemap.html`, and `codemap.lock` together with the `maintain-code-map` tool. Keep review/staging files ignored. The map is contributor documentation; it is not part of the installable skill or the product test gate.
