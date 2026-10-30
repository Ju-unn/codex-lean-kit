"""Static and install checks for codex-lean-kit. Run from anywhere: python tests/check_kit.py"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_MODELS = {"gpt-6.1-sol", "gpt-6-sol", "gpt-5.6-terra", "gpt-6-luna"}
ALLOWED_EFFORT = {"low", "medium", "high"}
TEXT_SUFFIXES = {".md", ".toml", ".sh", ".py"}
MODEL_PATTERNS = [
    re.compile(r'(?<![\w])(?:default_subagent_)?model\s*=\s*\\?"([\w.\-]+)'),  # TOML values and -c 'model=<slug>'
    re.compile(r'codex\b[^\n`]*?\s(?:-m|--model)\s+"?([\w.\-]+)'),
]
CODEX_VALIDATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
failures = []


def check(ok, label):
    print(("PASS " if ok else "FAIL ") + label)
    if not ok:
        failures.append(label)


def text_files(root):
    return [p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES and ".git" not in p.parts]


def bad_models(root):
    found = []
    for p in text_files(root):
        text = p.read_text(encoding="utf-8")
        for pattern in MODEL_PATTERNS:
            found += [(p.relative_to(root), m) for m in pattern.findall(text) if m not in ALLOWED_MODELS]
    return found


def frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    return dict(re.findall(r"(?m)^(\w[\w-]*):\s*(.+)$", m.group(1))) if m else {}


def lines(path):
    return len(path.read_text(encoding="utf-8").splitlines())


# 1. Model allowlist, plus a self-test proving the check catches a forbidden value.
check(not bad_models(ROOT), f"model values within allowlist {bad_models(ROOT) or ''}")
with tempfile.TemporaryDirectory() as tmp:
    forbidden = "gpt-6-" + "astra"  # split so this file does not trip its own scan
    Path(tmp, "x.toml").write_text(f'model = "{forbidden}"\n', encoding="utf-8")
    check(bool(bad_models(Path(tmp))), "self-test: a forbidden model value is detected")

# 2. Agent roles.
roles = sorted((ROOT / ".codex/agents").glob("*.toml"))
check(len(roles) == 3, f"3 agent roles ({[r.stem for r in roles]})")
for role in roles:
    data = tomllib.loads(role.read_text(encoding="utf-8"))
    missing = {"name", "description", "developer_instructions", "model", "model_reasoning_effort"} - data.keys()
    check(not missing and data["name"] == role.stem, f"role {role.stem}: required keys, name matches file {missing or ''}")
    check(data.get("model_reasoning_effort") in ALLOWED_EFFORT, f"role {role.stem}: effort {data.get('model_reasoning_effort')}")

# 3. Skills: frontmatter, links, Codex's own validator when available.
skills = sorted(p.parent for p in (ROOT / ".agents/skills").glob("*/SKILL.md"))
check(len(skills) == 9, f"9 skills ({[s.name for s in skills]})")
for skill in skills:
    fm = frontmatter(skill / "SKILL.md")
    desc = fm.get("description", "")
    check(fm.get("name") == skill.name, f"skill {skill.name}: name matches folder")
    check(desc.startswith("Use when") and len(desc) <= 1024 and not re.search(r"[<>]", desc),
          f"skill {skill.name}: description starts with 'Use when', <=1024 chars, no angle brackets")
    body = (skill / "SKILL.md").read_text(encoding="utf-8")
    links = re.findall(r"(?<![\w/.])((?:references|assets)/[\w.\-]+\.md)", body)
    links += [str(Path("..", "..", "..", l)) for l in re.findall(r"(\.agents/skills/[\w\-]+/[\w\-]+/[\w.\-]+\.md)", body)]
    broken = [l for l in links if not (skill / l).resolve().exists()]
    check(not broken, f"skill {skill.name}: linked files exist {broken or ''}")
    if CODEX_VALIDATOR.exists():
        # -X utf8: the validator reads with the locale encoding, which is cp949 on Korean Windows.
        r = subprocess.run([sys.executable, "-X", "utf8", str(CODEX_VALIDATOR), str(skill)], capture_output=True, text=True)
        check(r.returncode == 0, f"skill {skill.name}: Codex quick_validate ({r.stdout.strip() or r.stderr.strip()})")

# 4. Size budgets and line endings.
# AGENTS.md loads every turn, so it stays small; skills and references load only when used.
budgets = [(ROOT / "AGENTS.md", 120)] + [(s / "SKILL.md", 200) for s in skills]
# ui-design/references/quick-reference.md is the upstream file unchanged (256 lines).
budgets += [(p, 260) for p in (ROOT / ".agents/skills").glob("*/references/*.md")]
for path, limit in budgets:
    check(lines(path) <= limit, f"size {path.relative_to(ROOT)}: {lines(path)} <= {limit} lines")
crlf = [str(p.relative_to(ROOT)) for p in text_files(ROOT) if b"\r\n" in p.read_bytes()]
check(not crlf, f"LF line endings {crlf or ''}")

# 5. install.sh: empty workspace and a workspace with its own AGENTS.md and skill, each installed twice.
sh = shutil.which("sh")
if not sh:
    check(False, "install.sh: NOT_RUN (no sh on PATH)")
else:
    with tempfile.TemporaryDirectory() as empty, tempfile.TemporaryDirectory() as busy_root:
        busy = str(Path(busy_root, "해커톤 작업 공간"))  # spaces and Korean, like real workspace names
        own_skill = Path(busy, ".agents/skills/handoff/SKILL.md")
        own_skill.parent.mkdir(parents=True)
        own_skill.write_text("mine\n", encoding="utf-8")
        Path(busy, "AGENTS.md").write_text("# Platform rules\n", encoding="utf-8")
        for ws in (empty, busy):
            runs = [subprocess.run([sh, str(ROOT / "install.sh")], cwd=ws, capture_output=True, text=True) for _ in range(2)]
            agents = Path(ws, "AGENTS.md").read_text(encoding="utf-8")
            check(all(r.returncode == 0 for r in runs), f"install.sh exit 0 twice in {'empty' if ws == empty else 'busy'} workspace")
            check(agents.count("<!-- codex-lean-kit -->") == 1, "install.sh: kit section present exactly once")
            check("files copied: 0" in runs[1].stdout, "install.sh: second run copies nothing")
            check(len(list(Path(ws, ".codex/agents").glob("*.toml"))) == 3, "install.sh: 3 roles installed")
        check(Path(busy, "AGENTS.md").read_text(encoding="utf-8").startswith("# Platform rules"), "install.sh: existing AGENTS.md content kept on top")
        check(own_skill.read_text(encoding="utf-8") == "mine\n", "install.sh: existing skill file not overwritten")

print(f"\n{len(failures)} failure(s)" if failures else "\nall checks passed")
sys.exit(1 if failures else 0)
