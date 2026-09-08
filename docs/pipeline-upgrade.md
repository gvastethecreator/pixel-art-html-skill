# Pixel art pipeline upgrade

## Goal

Use the local reference collections to improve how an LLM constructs and repairs exact pixel grids. Keep the deterministic compiler and its honest review tiers. Add reusable knowledge and working tools where the current instructions leave the model guessing.

## Plan

- [x] Inspect the skill, repository state, and source collections.
- [x] Index every source file, map all 62 wiki chapters, survey the media, and inspect selected construction examples in detail.
- [x] Turn the evidence into a portable technique library, reference retrieval, construction passes, and local pixel repair tools.
- [x] Exercise construction and repair with original specimens and run the existing checks plus focused coverage for new behavior.
- [x] Review the final diff and record evidence and remaining limits here.
- [x] Expand verification to 24 varied original assets, inspect every final in the browser, and repair observed failures.
- [x] Critique the current pieces before comparing versions, run independent model reviews, and apply the strongest findings to the skill and artwork.
- [x] Run one independent forward test using only the portable skill and repair the workflow friction it exposes.

## Baseline

The worktree was clean. The GitHub repository is public, owned by `gvastethecreator`, with standard Actions enabled. No setting change was needed.

The compiler already supports exact grids, motifs, direction studies, repair provenance, blind proof, and reviewed promotion. The main gap is the bridge from a visual reference to deliberate pixel placement. Current subject guides name desirable outcomes but offer few construction decisions or coordinate-based repairs.

## Source handling

The wiki has 62 chapter directories. Its `README.md`, `reglas.md`, and `prompts.md` are local interpretations, and its `article.html` files are image galleries with source links. They are not archived original article text. Some local rules turn examples into universal restrictions. Check those against the primary article and the visible construction before adopting them.

Keep source images, videos, complete articles, local paths, and generated indexes outside the distributable skill. Bundle original technical synthesis, source attribution, and retrieval tools. Record inventory coverage separately from visual inspection and animation review.

## Resource coverage

The private index covers all files discovered in the three requested roots, excluding symlinks and tool caches. It includes complete text, content hashes, image headers and first-frame decoding, and video metadata. No source files were changed.

| Collection alias | Images, including GIFs | Videos | Text | Total |
|---|---:|---:|---:|---:|
| `wiki` | 902 | 0 | 255 | 1,157 |
| `patreon` | 1,529 | 0 | 28 | 1,557 |
| `pixelart` | 562 | 424 | 0 | 986 |
| Total | 2,993 | 424 | 283 | 3,700 |

The index found 567 exact byte duplicates and no read or probe errors. A survey produced 60 sheets covering 2,851 unique media files with no sampling errors. All ten composite overviews were visually inspected. This is broad visual triage of selected frames, not native-size inspection of every image or full playback of every video.

All 62 chapter titles and topic routes were reviewed. Selected core and subject notes were read in detail. Full text was indexed for retrieval; indexing does not mean every paragraph received a close reading. Four process GIFs were additionally inspected through five recorded frame samples each: deciduous foliage, an isometric house, infantry construction, and a valley. The isometric car breakdown and character-design revision sheet were opened as original local images.

The private evidence remains under `.local/pipeline-upgrade/`: `library.json`, `survey/`, `survey-coverage.json`, and `process-study.png` with its receipt. These files contain source paths or artwork and are ignored by Git.

## What the resources changed

| Resource | Useful evidence | Resulting pipeline decision |
|---|---|---|
| Wiki chapters and galleries | Named methods, original image captions, and source links make construction examples retrievable. | Recover captions in the index; route problems to 18 portable technique cards covering all 62 chapters. |
| Foliage processes | Overlapping crown bundles establish depth before leaf detail. | Plan rear and front masses, reuse original motifs, then inspect and repair their junctions. |
| Isometric construction | Cabin, chassis, wheels, and supporting volumes can be studied separately before assembly. | Name anchors, shared corners, bounds, and paint order before surface detail. |
| Character revisions | Removing costume marks and changing value allocation can clarify a pose. | Protect identifying gaps and test subtraction at native size. |
| Patreon images and GIFs | Process material sits beside finished work, repeated exports, and publishing material. | Select construction frames by evidence; deduplicate bytes and exclude publishing advice from authoring guidance. |
| Pixelart image/video collection | Broad visual examples have mostly opaque social-media filenames. | Provide survey and timestamped sampling tools without pretending filename search understands image content. |

The primary articles on [texture](https://www.slynyrd.com/blog/2018/2/15/pixelblog-2-texture), [basic pixel construction](https://www.slynyrd.com/blog/2018/5/16/pixelblog-5-back-to-basics), and [light and shadow](https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow) were consulted when checking derivative rules. The revised guidance permits deliberate palette-bound antialiasing, simple geometric subjects, and fewer than three value groups. Their suitability depends on the intended read. Numerical examples in secondary notes are not universal quality gates.

## Implemented path

The skill now connects brief, reference decision, part construction, silhouette, planes, material clusters, local repair, browser inspection, and honest review tiers. It preserves the existing deterministic compiler and artifact format.

`reference_library.py` indexes local collections, searches complete text and gallery captions, retrieves bundled techniques, and creates sampled boards with source hashes and frame positions. Ranking precedes deduplication so the most relevant caption is retained. Changed sources require a fresh index.

`pixel_lab.py` reports exact region rows and cluster coordinates, compares canonical grids, and applies patches with a baseline fingerprint, expected colors, protected regions, and a palette budget. It writes a new standard repair draft and leaves the baseline intact. Its coordinate loupe preserves native context, shared color aliases, and an exact before/after receipt. The patch command accepts `--scale 1` for a native PNG. A changed-cell count is evidence of an intervention, not its artistic value.

The evaluation catalog contains six controlled requests, including criticism and repair of a construction plateau. Prior and updated workflows use the same model settings, brief, grid, palette budget, supplied sources, and effort allowance. Shared skill instructions do not select a provider or model. The first closeout had only independent reviews and a forward test; the user then authorized the paired six-case run recorded below.

## What criticism changed

The 24-piece battery spans 8x8 icons, 16x16 items and tiles, 24x24 equipment, 32x32 characters and vegetation, 48x48 buildings and vehicles, and 64x64 scenes. It includes insects, a portrait, a robot, foliage, stone, water, masonry, a valley, and a harbor. All artwork uses original grids. The references supplied construction knowledge, not copied silhouettes, compositions, palettes, or motifs.

The initial 72 direction grids did not all meet the skill's own standard for meaningful alternatives. Rebuilt backpack, courier, and water studies added six distinct grids while retaining the earlier choices. Eight studies still rely too much on width or mark changes. This is recorded as a weakness rather than advertised as 72 strong directions.

Six subjects received deeper construction passes: flask, portrait, cargo mech, oak, cottage, and valley. Anonymous model comparisons preferred five first-round revisions, with a valley tie; the next round preferred all six against their older baselines. A separate current-only critique still found structural defects. The skill now requires that current-only judgment before revealing an older version, because a weak baseline can make an unfinished piece look convincing.

| Observed problem | Repair and reusable instruction | Remaining limit |
|---|---|---|
| The portrait's face planes and highlights competed with its eyes. | Group light around shared face axes; remove competing cells before adding features. | The far brow remains heavy and the intended expression needs a clearer native read. |
| The mech's load, frame, and leg joints formed ambiguous bars. | Trace load to mounts, body, joints, and feet; rebuild continuous support volumes. | One dark leg junction is still compressed. |
| The oak used repeated crown bundles that read as separate pompons. | Give the crown a dominant irregular mass and unequal subordinate groups. | The stronger crown hides part of the branch fork. |
| The backpack read as a face or container. | Preserve object identity with a handle, returning shoulder straps, one fastening, and a lower pocket. | The side strap remains dark. |
| The beetle's legs merged with the dark background and each other. | Raise exposed limb values and separate the far endpoints while protecting the body. | The brighter near legs attract more attention. |
| The flask risked losing its liquid level, and the valley used repetitive banks and foreground marks. | Preserve identity cues during simplification; vary terrain masses and reserve accents for a focal route. | Glass material and local terrain depth remain weaker than recognition. |

An independent model reviewed all 24 current pieces without their intended names, then compared the last backpack, mech, and beetle repairs anonymously. It preferred all three repairs and identified the backpack as a backpack. This is model critique, not a human recognition study or owner acceptance. The public [construction repair examples](../SKILLS/pixel-art-html/examples/construction-repair/README.md) preserve three earlier paired repairs, exact grids, fingerprints, and the tradeoffs noted by the reviewer. They deliberately retain imperfect results as teaching evidence.

The private `demo/quality-depth/critical-review.html` records findings for every battery item and links the corrected drafts. It separates visible defects from reasonable style choices: a geometric pine is not automatically a failure, and an ambiguous tower scale needs context before it can be judged.

## Independent forward test

A separate agent used only the portable skill to construct a new 32x32 swamp courier beetle with a suspended lantern and at most eight colors. It did not use the battery, private corpus, or another drawing. Three directions changed pose, facing, leg placement, and lamp support. Flat construction exposed an antenna/lantern tangency; a later guarded patch changed 16 leg cells with no silhouette change.

The test exposed real workflow friction: the loupe was documented before its command existed, protected-region arrays lacked an example, patch export lacked a native-scale option, and anatomy guidance assumed humanoids. These gaps are now repaired and tested where behavior changed. Lexical technique search also returned an irrelevant stone card; its limits remain explicit.

The parent inspected the direction study and final browser output after the builder finished. The result reads as an insect carrying a suspended light; the courier role and effortless six-leg counting are still uncertain at 1x. It remains a draft. Its source, stages, repair, and builder record are under `demo/forward-test/`, with final fingerprint `f0d4bc9f850f0532626898d23579c3e84cc96e1f965cae309646b2529e2a0df3`.

## Verification on 2026-09-08

- `pnpm run check:full`: passed the package validator and all 52 tests, including 13 image tests, with zero skips. The ten added tests cover observable retrieval, sampling, region inspection, coordinate loupe, and guarded repair behavior in the existing suite. Production code remained unchanged after this run.
- Skill creator `quick_validate.py`: passed.
- `git diff --check`: passed. Final documentation also received structural review.
- The existing compiler validated the initial demonstration, all 24 battery selections and their studies/checkpoints, and the independent forward test. The three later changed battery assets received separate affected-artifact validation. All six public before/after specs were rebuilt and their fingerprints matched the example receipt.
- An original tree demonstration exercised motif construction and an observed repair. Nine competing highlight cells changed; silhouette changes were zero. The original and repaired grids retain separate fingerprints and artifacts.
- All 24 selected pieces were inspected in the same Codex in-app browser at native and integer zoom, including block, plane, silhouette, and value views. CDP compared every native canvas with its canonical RGBA grid: zero mismatched cells, native CSS scale 1, smoothing disabled, and no external requests. The final three repairs were inspected again in color, value, and silhouette, on dark and pale proof surfaces; their three affected native canvases also had zero mismatches. The viewport was 1714x1280 at device pixel ratio 1.
- The independent forward test was inspected at native, 2x, and 4x, plus silhouette and value. Its browser canvas had zero mismatched cells. Water and brick were inspected as 3x3 repeats; mixed tile transitions and motion were not assessed.
- The first demonstration's grid/title controls and keyboard scale adjustment worked, with no warning/error logs reported in that earlier check. Console logs were not separately collected for the final battery; pixel parity does not prove the absence of browser errors.
- Browser screenshots were captured inline in the task. The browser tool did not provide local screenshot paths. `demo/browser-proof.json` and `demo/browser-proof-final.json` record this boundary. The first anonymous all-piece contact sheet cropped part of the harbor's native inset; a corrected sheet preserves it, and the full harbor had already been inspected in the browser.
- The installed skill junction resolves to this repository's skill folder, so the local installation receives these changes directly.

The original demonstration, source specs, checkpoints, patch, delta, and self-review are under `.local/pipeline-upgrade/demo/`. Its final grid fingerprint is `718a2779cae02032b7a9a539c77082297f0bb3e283a3a7b7c587f8d0092347b2`. It remains a draft: the tree reads, but repeated crown motifs and a simple trunk still limit its character.

## Remaining evidence limits

The evidence includes independent model criticism, one paired six-case run, and an independent forward test. It does not include replication, a human recognition study, or proof of general artistic improvement across models. Full video playback, Linux behavior, responsive layouts, and remote CI were not assessed. The 24 battery pieces, evaluation outputs, city scene, and forward-test sprite remain drafts, with named artistic limits and no promotion to owner-reviewed status. Commits were authorized in the follow-up; no push or publication was requested or performed.

## Follow-up: controlled comparison and city scene

The user authorized commits and completion of the comparison, then requested an original city scene with ninjas, knights, and skeletons on a canvas with zoom and pan.

- [x] Commit reference retrieval as `2222feb` and construction/critique as `092f0d3`.
- [x] Finish the six-case paired run from frozen revisions `00abf56` and `092f0d3`. Both builders received the same requests, source fixtures, model settings, 24-minute authoring allowance, and one repair pass per case. The parent reviewed anonymous outputs and recorded outcomes and evidence limits.
- [x] Construct the city from exact native masters with shared projection, palette roles, foot contacts, and deliberate faction silhouettes. Keep original editable sources and a reproducible scene manifest.
- [x] Deliver a standalone canvas viewer with pointer pan, anchored zoom, fit, native scale, and keyboard controls. Check the rendered city and actual controls.
- [x] Add reusable skill changes supported by this scene and validate the changed behavior. Commit the original scene, compositor, viewer, and scene guidance as `45abf9a`; preserve the comparison and closeout evidence in a separate documentation commit.

The scene uses a 480x320 world assembled from masters no larger than 128x128, preserving the existing single-asset compiler contract. A night plaza connects rooftop ambushes, a guarded gate, and a crypt entrance. Faction identity comes from pose, equipment, and silhouette as well as color. This is a still scene; animation and game simulation are outside this request.

### Completed comparison

Both builders completed all six requests, including two repairs in the last request, with seven final masters per arm. The parent recorded preferences before opening the shuffled arm mapping. The parent did not build either arm but did author the skill and repair fixtures. Builder progress messages disclosed some self-reported failure descriptions, so blinding was partial.

| Request | Preferred workflow | Visible reason and remaining limit |
|---|---|---|
| 16x16 storm lighthouse | Prior | Its continuous tower and small gallery read more clearly; the updated output gives too much mass to the lantern. Both storms are generic. |
| Red-scarf source recovery | Updated | The low forward arm and large connected scarf preserve the common source pose more closely. The scarf still looks stiff. |
| 8x8 scout ship recovery | Updated | Nose, cockpit, hull, and two engines remain separate; the other result can read as an arch or badge. |
| 32x32 tree | Prior | A dominant crown reads more coherently; the updated tree splits into bright balls. The preferred lower crown still forms a heavy band. |
| 32x32 isometric carrier | Updated | Crate faces share their corners more clearly. Legs and optical cue remain compressed. |
| Critique and two repairs | Updated, with a tied tree repair | The carrier's platform and leg paths are simpler. Its load slot remains ambiguous, and neither tree repair gives a decisive native gain. |

This is four case preferences for the updated skill and two for the prior workflow. It is not a statistical result or proof that every new instruction helped. Both arms passed their artifact validations; the parent compared all 14 native browser canvases with their embedded grids and found zero mismatched cells, CSS scale 1, and smoothing disabled. All final outputs were seen at native, 2x, 4x, and enlarged color; value/silhouette controls were exercised. Not every study candidate received a separate parent perceptual review.

The prior arm took 1,093.36 seconds through validation. The updated arm took 1,204.34 seconds, then 119.30 seconds for inventory and checkpoint review without art changes. Both had the same 1,440-second allowance. Active per-case intervals overlapped, and token cost was not available. The public [paired result receipt](../SKILLS/pixel-art-html/evals/results/paired-2026-09-08.json) preserves observations, mappings, source hashes, costs, and limits. Raw grids, specs, builder records, and the anonymous browser gallery remain under the private task directory.

### City scene and pipeline changes

The [city example](../SKILLS/pixel-art-html/examples/city-clash/README.md) contains a portable original builder. Its 38 native masters, 56 placements, and 27 colors form a 480x320 world with 12 actors. The script emits editable sources and block/plane checkpoints. The new compositor embeds the native masters, recomposes stable depth order, validates exact PNG/JSON/HTML agreement, and exports a standalone interactive canvas.

The first composition exposed a shield bearer facing away from its attacker, a rooftop actor with feet below the eave, and a skeleton drawn over the crypt roof. Repairs changed world contact positions and depth instead of adding costume detail. Actor shadows now remain separate from subject silhouettes. The new scene reference teaches actor/action/target relationships, contact height, occlusion, shared palette roles, and the limits of mirroring lit sprites.

The live viewport was 1280x720 at DPR 1.5. A real border/content-box mismatch exposed a one-physical-pixel stretch; the viewer now measures the fractional content box and keeps the camera in integer physical pixels. Browser proof found zero mismatches between all 153,600 world cells and the native PNG, and zero mismatches in their full 2x physical-pixel display. Actual drag moved by the expected DPR-adjusted delta and released capture; wheel zoom moved the anchored world point by at most 0.051 source cells from snapping. Native/max zoom, disabled bounds, Home, arrow pan, Tab/Shift+Tab, group visibility, focus points, and value/subject views were exercised. No warning/error logs or external requests were reported.

`pnpm run check:full` passed 54 tests, including the two new scene composition/parity regressions, with all 13 Pillow tests included. Later template-only content-box changes received the affected browser proof above; the unchanged Python suite was not repeated. Scene validation passed with fingerprint `2b489c55ba9844afe7c9dd1bd5775d56b5617799dcbbd59420e23923b7687836`. Screenshots remain inline; the tool supplied no local screenshot path. The city remains a draft with simplified projection, crowded small contacts, repeated human proportions, and stylized mirrored lighting.


## Follow-up: executable construction and staged review

The user approved the proposed improvements on 2026-09-08. Keep the committed city and paired evaluation as baselines. The first implementation connects named parts to exact grids, requires observed stage reviews before refinement, and tests those mechanics on original art.

- [x] Add an editable part source, explicit anchor and visibility constraints, and a native ownership view.
- [x] Bind stage transitions to the reviewed source and grid. Reject stale reviews and structural drift after block review. Preserve rework decisions.
- [x] Use the route on a lighthouse, tree, and three-faction encounter; inspect block before authoring later passes.
- [x] Add original visual lessons with conditional repairs and a separate transfer evaluation. Keep reference pixels private and do not copy them.
- [x] Run the existing suite with focused regressions, inspect the browser output, record actual preferences and limits, and review the diff.

These tools can enforce declared geometry and review order. They cannot authenticate a reviewer or infer artistic acceptance from numeric diagnostics. A stage review is authoring feedback, not promotion.


### Completed executable construction work

`construct.py` now compiles named part masks, parent-relative origins, anchors, paint order and explicit constraints. The report distinguishes attachment distance, visible ownership, protected gaps and support points inside a chosen surface. Hidden paint remains available and counts toward the palette budget. These checks do not recognize anatomy or infer good art.

The new part viewer shows native color, values, actor silhouettes and visible ownership. Selecting a part exposes its world anchors while keeping actual occlusion. Block, planes and material outputs retain the source and bound ancestor reviews. A changed mask, placement, anchor, role, constraint, intent or light returns to block; stale reviews and skipped stages fail validation. Review declarations are not authenticated perception and do not grant promotion.

Original development work used a 16x16 lighthouse, 32x32 wind tree and 96x80 three-faction encounter. Actual inspection rejected the initial lighthouse cap and trunk gap, then two canopy shadow attempts. An independent current-only critique found unsupported skeleton feet and competing diagonal weapons. The encounter returned to block, with a redrawn deck and shorter counterthrust. Its remaining short blade is still difficult to distinguish; the lighthouse shaft remains irregular and some foliage marks remain stepped. All remain drafts.

The [portable examples](../SKILLS/pixel-art-html/examples/part-construction/README.md) reproduce the winning historical lineages, an exact scene export with pan and zoom, and seven original visual lessons. The lessons preserve losing grids, causes, conditional interventions, what to retain and remaining limits. This first set contains seven observed lessons from three studies, not the roughly twenty initially proposed, and does not count them as independent tests. It includes a failed repair, a diagnostic-view change and an explicitly partial repair.

### Separate forward comparison

Two builders received frozen prior/current skill snapshots and the same four fresh briefs: a marsh bird with a tied parcel, a broken stone arch, an owl kitchen timer and a spear encounter on a bridge. Both inherited the active client's model/settings, had a 24-minute allowance, and could make at most one finished repair per case. Reference images, development studies and the other arm were unavailable. The current snapshot tested parts and stage reviews; the later support check, flat-repair guard and lessons were added after this run.

The parent recorded preferences on shuffled labels before opening the mapping. The parent wrote the skill and knew the briefs and agent progress, so blinding was partial. The update was preferred for bird volume/package, owl identity (weak preference), and encounter action. The prior skill was preferred for the clearer broken arch. The update took 1,025.30 seconds; the prior skill took 620.71 seconds. Equal maximum allowance did not produce equal elapsed cost. Token cost was unavailable. One run per arm cannot establish a general effect or reliable win rate.

The updated owl final exposed a real workflow hole: the generic flat patch discarded the editable construction bundle. The skill now routes color repairs through named parts, and the common flat repair compiler rejects constructed exports. Rebuilding the saved five-part owl source preserved exactly the frozen final grid; neither trial arm was changed. The [paired receipt](../SKILLS/pixel-art-html/evals/results/construction-paired-2026-09-08.json) preserves preferences, hashes, costs, snapshot inventory and limitations.

### Verification and retained evidence

`pnpm run check:full` passed 60 tests, including six new construction regressions and all 13 existing Pillow cases. The portable replay built nine stage bundles and checked exact scene-to-construction grid agreement. All eight forward outputs also passed their canonical validators. A later template correction made the background part of the grayscale view and opens large studies at 4x; the affected browser checks passed without repeating unchanged Python tests.

At 1280x720 in the Codex browser, all three final study canvases, all eight trial grids at CSS 1x/2x/4x, and all fourteen lesson grids at CSS 1x/4x matched their embedded cells. The 96x80 encounter export had zero native mismatches and zero display mismatches across the full 5x view at DPR 1. Zoom, fit and faction visibility were exercised. The unchanged scene camera's earlier drag/wheel/keyboard proof remains the pan evidence; an attempted new keyboard check was not captured because the browser adapter did not expose the suggested key-input API. No new pan result is claimed. The corrected values view had zero non-gray cells, including the background. Screenshots were inspected inline; no local screenshot file was returned.

The final local hub is `.local/pipeline-upgrade/demo/construction-lab/index.html`; `release/` is the portable replay, `transfer/` is the anonymous comparison and `owl-provenance-repair/` preserves the same owl pixels with editable parts. Original stages and rejected reviews remain alongside them. The prior city and committed comparison are unchanged. The loopback server on port 8769 was restored in a hidden process after the previous server stopped. Temporary interpreter caches and one incomplete early build remain ignored private scratch; no source cleanup was needed.
