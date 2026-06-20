---
name: huajiao-finance-writer
description: >
  Rewrite Chinese finance, market, company, macro, or news source material into
  花椒 voice using DeepSeek, then support a self-improving before/after learning
  loop. Use when the user asks to 改写财经文章, 仿写但保留事实, 去 AI 味,
  输出可手改文案, 学习用户修改, 更新 learned.md, or run the chain:
  source to DeepSeek draft to anti-AI/say-it-human/renwei cleanup to user edit
  to learned rules.
---

# Huajiao Finance Writer

Use this skill to turn finance/news source material into a long social post in
花椒 voice, then learn from the user's edits.

## Chain

```text
source
-> DeepSeek imitation pass using rules/voice.md + writer.md + constraints.md + learned.md
-> one DeepSeek cleanup pass using anti-ai.md + local say-it-human + local renwei-writing
-> user edits final draft
-> learner appends concrete rules to learned.md
```

Do not add scoring, visual panels, vector stores, or multi-agent loops.

## Rules

- Use DeepSeek for generation.
- Read the API key from `DEEPSEEK_API_KEY` or `DEEPSEEK_API_KEY_FILE`.
- Never store or print API keys.
- Use the tweet corpus only for rhythm, structure, paragraphing, and sentence movement.
- Do not copy Web3, crypto, 盘学, old calls, or old topics from the tweet corpus.
- Preserve source facts, dates, numbers, names, and attribution.
- Do not invent background, causes, market moves, or extra examples.
- Default output is `long-social`, not a 280-character summary.
- Keep roughness when it is human. Do not polish away the speaker.

## Run

Save source text to a file, then run:

```bash
DEEPSEEK_API_KEY_FILE=/path/to/deepseek_api_key.txt \
VOICE_OUTPUT_MODE=long-social \
python3 /Users/oxjames/.codex/skills/huajiao-finance-writer/scripts/deepseek_generate.py source.md out.md
```

Output:

- `out-raw.md`: first DeepSeek imitation draft
- `out.md`: cleaned draft for the user to edit

Modes:

- `long-social`: normal long post
- `thread`: 3-6 connected posts
- `short`: one short post under 280 Chinese characters

## Learn

After the user edits `out.md` into `after.md`, run:

```bash
python3 /Users/oxjames/.codex/skills/huajiao-finance-writer/scripts/learn_diff.py out.md after.md
```

Only learn concrete before/after rules. Put style preferences in
`rules/learned.md`. Put never-repeat mistakes in `rules/constraints.md`.

## Resources

- `rules/voice.md`: distilled 花椒 voice.
- `rules/writer.md`: stable writing rules.
- `rules/constraints.md`: hard constraints.
- `rules/anti-ai.md`: local cleanup summary.
- `rules/learned.md`: append-only learned rules.
- `vendor/say-it-human/`: local cleanup skill files.
- `vendor/renwei-writing/`: local human-presence skill files.
