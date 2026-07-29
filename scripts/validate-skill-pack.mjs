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
  "SKILLS/pixel-art-html/assets/pixel-art-project-hub-template.html",
  "SKILLS/pixel-art-html/assets/visual-review-template.md",
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

for (const file of (await walk(root)).filter(file => /\.(md|json|ya?ml|mjs|js|css|html|py|txt)$/i.test(file))) {
  if (relative(file).startsWith(".git/")) continue;
  const text = await fs.readFile(file, "utf8").catch(() => "");
  const localPath = new RegExp("\\b[A-Z]:\\\\(?:Users|" + "DEV)\\\\", "i");
  const matrixName = new RegExp("agents-" + "matrix\\b", "i");
  if (localPath.test(text) || matrixName.test(text)) errors.push(`possible local path leak: ${relative(file)}`);
}

for (const template of ["pixel-art-template.html", "pixel-art-collection-template.html", "pixel-art-project-hub-template.html"]) {
  const text = await fs.readFile(path.join(skill, "assets", template), "utf8").catch(() => "");
  if (/https?:\/\//i.test(text)) errors.push(`remote URL in standalone template: ${template}`);
}

JSON.parse(await fs.readFile(path.join(root, "skills.sh.json"), "utf8"));

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
