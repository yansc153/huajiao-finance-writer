#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://api.deepseek.com/chat/completions"


def secret() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    key_file = os.environ.get("DEEPSEEK_API_KEY_FILE", "").strip()
    if key_file:
        return Path(key_file).read_text(encoding="utf-8").strip()
    raise SystemExit("DEEPSEEK_API_KEY or DEEPSEEK_API_KEY_FILE is required")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8") if not path.startswith("/") else Path(path).read_text(encoding="utf-8")


def ask_deepseek(prompt: str, temperature: float = 0.7) -> str:
    body = json.dumps({
        "model": os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={"Authorization": f"Bearer {secret()}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: deepseek_generate.py ARTICLE.md OUT.md", file=sys.stderr)
        return 2

    article_path, out_path_arg = argv
    out = ROOT / out_path_arg if not out_path_arg.startswith("/") else Path(out_path_arg)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_name(out.stem + "-raw" + out.suffix)

    mode = os.environ.get("VOICE_OUTPUT_MODE", "long-social")
    mode_rules = {
        "long-social": "Default mode. Preserve the article's main argument, structure, examples, and useful details. Target 800-1500 Chinese characters for 1500-3000 character sources. Do not make a 280-character summary.",
        "thread": "Turn the article into 3-6 connected X posts. Each post should stand alone but preserve the article's flow.",
        "short": "Make one short X post under 280 Chinese characters. Use only when explicitly requested.",
    }.get(mode, mode)

    imitation_prompt = "\n\n".join([
        read("rules/voice.md"),
        read("rules/writer.md"),
        read("rules/constraints.md"),
        read("rules/learned.md"),
        f"Output mode: {mode_rules}",
        "Task: rewrite the source material in 花椒 voice. This is style transfer, not summary unless mode says short. Use ONLY facts explicitly present in the source packet / Fact Spine. Do not add company examples, numbers, background events, causes, or market moves that are not in the packet. Output drafts only. Do not explain.",
        read(article_path),
    ])
    raw_text = ask_deepseek(imitation_prompt, temperature=0.75)
    raw.write_text(raw_text, encoding="utf-8")

    cleanup_prompt = "\n\n".join([
        read("rules/anti-ai.md"),
        read("rules/constraints.md"),
        read("vendor/say-it-human/skills/humanize-ai/SKILL.md"),
        read("vendor/say-it-human/skills/editor-revisor/SKILL.md"),
        read("vendor/renwei-writing/SKILL.md"),
        read("vendor/renwei-writing/references/post-edit-checklist.md"),
        "Source packet / Fact Spine. The final copy may use ONLY these facts:",
        read(article_path),
        "Task: rewrite the draft below once. Apply the cleanup layers in this order inside this single pass: anti-AI cleanup, say-it-human checks, then renwei-writing preservation. Preserve 花椒 voice and every source fact. Delete any fact, number, company example, background event, cause, or market move that is not explicitly present in the source packet above. Remove polished report voice, repeated transitions, and generic prompt smell, but do not over-polish or erase rough handprint. Keep it short. Output final copy only. Do not explain.",
        raw_text,
    ])
    out.write_text(ask_deepseek(cleanup_prompt, temperature=0.45), encoding="utf-8")
    print(f"raw: {raw}")
    print(f"final: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
