import fs from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const skill = path.join(root, "SKILLS", "pixel-art-html");
const required = [
  ".gitignore",
  "LICENSE",
  "README.md",
  "SECURITY.md",
  "skills.sh.json",
  "SKILLS/README.md",
  "SKILLS/pixel-art-html/SKILL.md",
  "SKILLS/pixel-art-html/agents/openai.yaml",
  "SKILLS/pixel-art-html/assets/pixel-art-template.html",
  "SKILLS/pixel-art-html/assets/pixel-art-collection-template.html",
  "SKILLS/pixel-art-html/assets/pixel-art-study-template.html",
  "SKILLS/pixel-art-html/assets/pixel-art-project-hub-template.html",
  "SKILLS/pixel-art-html/assets/visual-review-template.md",
  "SKILLS/pixel-art-html/assets/visual-review-input.json",
  "SKILLS/pixel-art-html/examples/cursed-salvage/README.md",
  "SKILLS/pixel-art-html/examples/cursed-salvage/visual-review.md",
  "SKILLS/pixel-art-html/examples/cursed-salvage/specs/potion.json",
  "SKILLS/pixel-art-html/examples/cursed-salvage/specs/key.json",
  "SKILLS/pixel-art-html/examples/cursed-salvage/specs/shield.json",
  "SKILLS/pixel-art-html/examples/cursed-salvage/specs/crystal.json",
  "SKILLS/pixel-art-html/examples/cursed-salvage/previews/potion.png",
  "SKILLS/pixel-art-html/examples/cursed-salvage/previews/key.png",
  "SKILLS/pixel-art-html/examples/cursed-salvage/previews/shield.png",
  "SKILLS/pixel-art-html/examples/cursed-salvage/previews/crystal.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/README.md",
  "SKILLS/pixel-art-html/examples/small-grid-repair/visual-review.md",
  "SKILLS/pixel-art-html/examples/small-grid-repair/baselines/8x8.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/baselines/16x16.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/directions/a-bound-flask.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/directions/b-signal-vial.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/directions/c-heart-reliquary.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/repairs/potion-8.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/repairs/potion-16.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/previews/automatic-8.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/previews/automatic-16.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/previews/authored-8.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/previews/authored-16.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/previews/direction-a.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/previews/direction-b.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/previews/direction-c.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/sources/character-32.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/sources/ship-32.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/baselines/character-8.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/baselines/ship-8.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/repairs/character-8.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/repairs/ship-8.json",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/previews/character-source.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/previews/character-automatic.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/previews/character-authored.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/previews/ship-source.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/previews/ship-automatic.png",
  "SKILLS/pixel-art-html/examples/small-grid-repair/transfer/previews/ship-authored.png",
  "SKILLS/pixel-art-html/references/artifact-schema.md",
  "SKILLS/pixel-art-html/references/command-reference.md",
  "SKILLS/pixel-art-html/references/craft-workflow.md",
  "SKILLS/pixel-art-html/references/image-source-brief.md",
  "SKILLS/pixel-art-html/references/project-library.md",
  "SKILLS/pixel-art-html/references/quality-contract.md",
  "SKILLS/pixel-art-html/references/source-recovery.md",
  "SKILLS/pixel-art-html/references/subject-recipes.md",
  "SKILLS/pixel-art-html/references/subjects/characters-creatures.md",
  "SKILLS/pixel-art-html/references/subjects/props-ui.md",
  "SKILLS/pixel-art-html/references/subjects/vehicles-architecture.md",
  "SKILLS/pixel-art-html/references/subjects/environments-tiles.md",
  "SKILLS/pixel-art-html/references/visual-review.md",
  "SKILLS/pixel-art-html/evals/evals.json",
  "SKILLS/pixel-art-html/evals/trigger_queries.json",
  "SKILLS/pixel-art-html/scripts/build_pixel_art.py",
  "SKILLS/pixel-art-html/scripts/benchmark_small_grids.py",
  "SKILLS/pixel-art-html/scripts/test_build_pixel_art.py",
  "scripts/run-pixel-art-tests.py"
];
const errors = [];

for (const file of required) {
  const stat = await fs.stat(path.join(root, file)).catch(() => null);
  if (!stat?.isFile()) errors.push(`missing required file: ${file}`);
}

for (const file of [skill, ...(await walk(skill))]) {
  const stat = await fs.lstat(file).catch(() => null);
  if (stat?.isSymbolicLink()) errors.push(`linked path is not portable: ${relative(file)}`);
}

const skillText = await fs.readFile(path.join(skill, "SKILL.md"), "utf8").catch(() => "");
const frontmatter = skillText.match(/^---\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/)?.[1] ?? "";
if (!/^name:\s*pixel-art-html\s*$/m.test(frontmatter)) errors.push("SKILL.md needs name: pixel-art-html");
if (!/^description:\s*".+"\s*$/m.test(frontmatter)) errors.push("SKILL.md needs a quoted description");
if (!/\bstudy\b/.test(skillText) || !/\bpromote\b/.test(skillText)) errors.push("SKILL.md must route through study and promote");

for (const file of (await walk(root)).filter(file => /\.(md|json|ya?ml|mjs|js|css|html|py|txt)$/i.test(file))) {
  if (relative(file).startsWith(".git/")) continue;
  const text = await fs.readFile(file, "utf8").catch(() => "");
  const localPath = new RegExp("\\b[A-Z]:\\\\(?:Users|" + "DEV)\\\\", "i");
  const matrixName = new RegExp("agents-" + "matrix\\b", "i");
  if (localPath.test(text) || matrixName.test(text)) errors.push(`possible local path leak: ${relative(file)}`);
}

for (const template of ["pixel-art-template.html", "pixel-art-collection-template.html", "pixel-art-study-template.html", "pixel-art-project-hub-template.html"]) {
  const text = await fs.readFile(path.join(skill, "assets", template), "utf8").catch(() => "");
  if (/https?:\/\//i.test(text)) errors.push(`remote URL in standalone template: ${template}`);
}

JSON.parse(await fs.readFile(path.join(root, "skills.sh.json"), "utf8"));

const evals = JSON.parse(await fs.readFile(path.join(skill, "evals", "evals.json"), "utf8"));
if (evals.schema_version !== 2 || evals.skill_name !== "pixel-art-html") errors.push("evals.json must use the pixel-art-html v2 contract");
if (!Array.isArray(evals.evals) || evals.evals.length !== 3) {
  errors.push("evals.json must contain exactly three controlled workflow cases");
} else {
  const ids = new Set();
  for (const item of evals.evals) {
    if (!item?.id || ids.has(item.id)) errors.push(`invalid or duplicate eval id: ${item?.id ?? "<missing>"}`);
    ids.add(item?.id);
    for (const field of ["required_evidence", "mechanical_assertions", "perceptual_questions"]) {
      if (!Array.isArray(item?.[field]) || item[field].length < 3) errors.push(`eval ${item?.id ?? "<missing>"} needs ${field}`);
    }
    for (const file of item?.files ?? []) {
      const stat = await fs.stat(path.join(skill, file)).catch(() => null);
      if (!stat?.isFile()) errors.push(`eval ${item?.id ?? "<missing>"} references a missing file: ${file}`);
    }
  }
}

const sourceFixtureText = await fs.readFile(path.join(skill, "evals", "fixtures", "character-source.ppm"), "utf8");
const sourceFixtureTokens = sourceFixtureText
  .split(/\r?\n/)
  .filter(line => !line.trimStart().startsWith("#"))
  .join(" ")
  .trim()
  .split(/\s+/);
if (sourceFixtureTokens[0] !== "P3" || Number(sourceFixtureTokens[1]) < 16 || Number(sourceFixtureTokens[2]) < 16) {
  errors.push("character-source.ppm must remain a meaningful P3 fixture of at least 16x16");
}

const reviewInput = JSON.parse(await fs.readFile(path.join(skill, "assets", "visual-review-input.json"), "utf8"));
if (reviewInput.decision === "accept" || Object.values(reviewInput.gates ?? {}).every(value => value === "passed")) {
  errors.push("visual-review-input.json must fail closed until a real reviewer edits it");
}

const triggers = JSON.parse(await fs.readFile(path.join(skill, "evals", "trigger_queries.json"), "utf8"));
if (!Array.isArray(triggers) || triggers.filter(item => item?.should_trigger === true).length < 10 || triggers.filter(item => item?.should_trigger === false).length < 8) {
  errors.push("trigger_queries.json needs at least 10 positive and 8 negative cases");
}

for (const file of (await walk(path.join(skill, "examples"))).filter(file => file.endsWith(".json"))) {
  const value = JSON.parse(await fs.readFile(file, "utf8"));
  if (["representative", "production-candidate"].includes(value?.evidence_tier)) {
    errors.push(`published source fixture self-assigns a promoted tier: ${relative(file)}`);
  }
}

if (errors.length) {
  errors.forEach(error => console.error(`- ${error}`));
  process.exitCode = 1;
} else {
  console.log("pixel-art-html-skill validation ok");
}

async function walk(dir, output = []) {
  const entries = await fs.readdir(dir, { withFileTypes: true }).catch(() => []);
  for (const entry of entries) {
    if ([".git", ".local", ".scratch", ".vscode", "node_modules"].includes(entry.name)) continue;
    const absolute = path.join(dir, entry.name);
    output.push(absolute);
    if (entry.isDirectory()) await walk(absolute, output);
  }
  return output;
}

function relative(file) {
  return path.relative(root, file).replace(/\\/g, "/");
}
