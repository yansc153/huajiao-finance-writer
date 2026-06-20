# Anti-AI Rules

Local source:

- `/Users/oxjames/.codex/skills/humanizer-zh/SKILL.md`
- `/Users/oxjames/.codex/skills/human-text-prior/SKILL.md`
- `vendor/say-it-human/skills/humanize-ai/SKILL.md`: use its AI-smell checks.
- `vendor/say-it-human/skills/editor-revisor/SKILL.md`: use its delete-the-slop posture.
- `vendor/renwei-writing/SKILL.md`: preserve the person behind the text; edit less, keep handprint, avoid turning plain observation into polished copywriting.
- `vendor/renwei-writing/references/post-edit-checklist.md`: check only edited lines for AI-smell patterns.

Use their rules as a cleanup layer.

## Renwei Layer

Use this only after the first draft exists.

- Do not make the draft prettier just because it can be prettier.
- Treat roughness, repeated words, odd pauses, and half-jokes as possible handprint first, not defects.
- If a sentence is plain but works, keep it plain.
- Do not replace the user's concrete wording with your own prettier image.
- Do not add fake scene anchors, fake details, or invented numbers to create presence.
- Do not write gold sentences. If a line sounds like it belongs on a poster, cut it.
- The best cleanup is often invisible: remove the stumble, keep the speaker.

## Remove

- `此外`
- `值得注意的是`
- `总而言之`
- `综上所述`
- `这不仅仅是...而是...`
- `标志着`
- `彰显`
- `赋能`
- `生态`
- `格局`
- `深度`
- `复杂性`
- `关键时刻`
- `更广泛的趋势`

## Fix

- Summary voice -> stance voice.
- Analyst report paragraphs -> social post paragraphs.
- Three balanced points -> one or two sharp points.
- Abstract transition -> concrete turn.
- Perfect symmetry -> uneven human pacing.
- Concept -> scene.
- Trend -> timeline.
- Slogan -> specific sentence.
- Over-complete paragraph -> keep the few lines with a real person inside.
- If the draft is human-ish but buried in stock phrases, act as editor-revisor: cut the stock phrases, do not decorate them.

## Say-It-Human Checks

Use these as the final cleanup checklist:

- Structure too symmetrical: break equal-length paragraphs, delete repeated summary sentences.
- Too much abstraction: replace `趋势/格局/意义/确定性` with what happened, who it affects, or what changed.
- Empty emotion: delete `令人深思/值得关注/很重要` unless a concrete detail makes the feeling happen.
- Sentences too neat: allow rough joins and short fragments.
- Missing detail: keep source numbers, names, dates, and examples instead of vague authority.
- Fake authority: remove teacherly claims that sound true anywhere.
- Over-lift: do not call small things `历史性/里程碑/分水岭`.
- Negative slogan pattern: delete `不是 A，而是 B` when it is just a pose.
- Fake range: delete `从 X 到 Y` if it is only decorative.
- Translation voice: use active, direct Chinese.
- Platform template: do not copy 小红书/抖音套话.
- RLHF smoothness: remove perfect flow when it makes the piece feel generated.

## Keep

- Names.
- Numbers.
- Dates.
- Causal claims from the source.
- Uncertainty when the source is uncertain.
