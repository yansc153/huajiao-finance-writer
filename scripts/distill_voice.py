#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TWEETS = Path("/Users/oxjames/Documents/我的所有历史推文/data/tweets.js")
API_URL = "https://api.deepseek.com/chat/completions"
BLOCK = re.compile(r"BTC|ETH|RGB|SBF|runes|bitcoin|airdrop|积分|空投|铭文|web3|币|链|加密|DeFi|NFT|合约|交易所|CZ|Binance|meme|庄|盘", re.I)


def secret() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    key_file = os.environ.get("DEEPSEEK_API_KEY_FILE", "").strip()
    if key_file:
        return Path(key_file).read_text(encoding="utf-8").strip()
    raise SystemExit("DEEPSEEK_API_KEY or DEEPSEEK_API_KEY_FILE is required")


def load_samples(limit: int = 80) -> list[str]:
    raw = TWEETS.read_text(encoding="utf-8")
    data = json.loads(raw[raw.index("["):])
    rows: list[tuple[int, str]] = []
    for item in data:
        tw = item.get("tweet", {})
        text = re.sub(r"https://t\.co/\S+", "", tw.get("full_text", "")).strip()
        text = re.sub(r"^@\S+\s*", "", text).strip()
        if not text or BLOCK.search(text) or not re.search(r"[\u4e00-\u9fff]", text):
            continue
        if 12 <= len(text) <= 280:
            score = int(tw.get("favorite_count", 0)) + 2 * int(tw.get("retweet_count", 0))
            rows.append((score, text))
    top = [x for _, x in sorted(rows, reverse=True)[: limit // 2]]
    recent = [x for _, x in rows[: limit // 2]]
    return list(dict.fromkeys(top + recent))[:limit]


def ask(prompt: str) -> str:
    body = json.dumps({
        "model": os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {secret()}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip() + "\n"


def main() -> int:
    samples = load_samples()
    prompt = """You are distilling a reusable Chinese writing voice guide from tweet samples.

Use samples for form only: cadence, sentence movement, paragraphing, stance, compression, openings, endings, omissions.
Do not copy topics, claims, Web3/crypto/盘学/trading content, or private references.

Hard ban: do not output domain vocabulary or examples from finance, Web3, crypto, trading, AI tools, or 盘学. No words such as 标的, 赛道, 流动性, 黑奴, 白嫖, 内幕, 庄, 币, 链, token, GPU. If a pattern needs examples, use neutral placeholders like `X`, `这件事`, `一个产品`, `一个公司`.

Write a Markdown voice guide with:
- Core voice in 5 bullets
- Sentence rhythm rules
- Paragraph structure rules
- Opening patterns
- Ending patterns
- Neutral phrase shapes to prefer
- Neutral phrase shapes to avoid
- 8 concrete do/don't transformation rules

Every rule must be behavior-level, not vague adjectives. Focus on reusable syntax, not content.

Samples:
""" + "\n\n---\n\n".join(samples)
    out = ROOT / "rules" / "voice.md"
    out.write_text(ask(prompt), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
