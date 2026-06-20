#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md",
    "rules/writer.md",
    "rules/voice.md",
    "rules/anti-ai.md",
    "rules/constraints.md",
    "rules/learned.md",
    "scripts/learn_diff.py",
    "scripts/deepseek_generate.py",
    "scripts/distill_voice.py",
    "vendor/renwei-writing/SKILL.md",
    "vendor/renwei-writing/references/post-edit-checklist.md",
    "vendor/say-it-human/skills/humanize-ai/SKILL.md",
    "vendor/say-it-human/skills/editor-revisor/SKILL.md",
]
missing = [p for p in required if not (root / p).exists()]
assert not missing, missing

text = (root / "rules/learned.md").read_text(encoding="utf-8")
learned_blocks = "\n".join(line for line in text.splitlines() if line.startswith("- "))
assert "更犀利" not in learned_blocks and "更自然" not in learned_blocks
assert "开头少用解释口吻" in text or "Append rules here" in text

skill = (root / "SKILL.md").read_text(encoding="utf-8")
for banned in ["评分器", "dashboard", "向量库"]:
    assert banned not in skill
assert "DeepSeek" in skill and "learned.md" in skill
text_files = []
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    try:
        text_files.append(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        continue
all_text = "\n".join(text_files)
assert not re.search(r"sk-[A-Za-z0-9]{20,}", all_text)

print("ok")
