#!/usr/bin/env python3
from __future__ import annotations

import difflib
import sys
from datetime import datetime, timezone
from pathlib import Path


def lines(path: Path) -> list[str]:
    return [line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()]


def extract_rules(before: list[str], after: list[str]) -> list[str]:
    removed: list[str] = []
    added: list[str] = []
    for line in difflib.ndiff(before, after):
        text = line[2:].strip()
        if not text or text.startswith("#"):
            continue
        if line.startswith("- "):
            removed.append(text)
        elif line.startswith("+ "):
            added.append(text)

    rules: list[str] = []
    joined_removed = "\n".join(removed)
    joined_added = "\n".join(added)

    if "说白了" in joined_removed and "别先看" in joined_added:
        rules.append("开头少用解释口吻的 `说白了`，优先直接给动作判断，比如 `别先看...先看...`。")
    if any("三个东西" in x or "：" in x for x in added):
        rules.append("列关键因素时可以直接拆成短行，不必塞在一个长句里。")
    if "体感" in joined_added:
        rules.append("遇到市场结构变化，优先写人的体感，再写抽象概念。")
    if any(x in joined_added for x in ["没有故事。", "没有一夜翻倍。"]):
        rules.append("反人性/不刺激这类判断后，用连续短句补画面，比解释更像用户。")
    if "就是赚点零花钱" in joined_added:
        rules.append("把泛泛的 `赚点小钱` 改成更口语的具体说法，如 `赚点零花钱`。")
    if any("三个判断" in x or "收尾" in x for x in removed):
        rules.append("不要为了完整感强行写总结段，用户会删掉这类 `三个判断，收尾`。")
    if any("说到底" in x or "最难的从来不是" in x for x in removed):
        rules.append("少写金句式升华，尤其是 `说到底...最难的是...` 这种模型收束。")
    if any("别急。先看。" in x for x in removed):
        rules.append("结尾不要硬落一句漂亮短句；如果正文已经讲完，可以直接停。")
    if any("别急着" in x or "没人能拍胸脯" in x for x in removed):
        rules.append("风险提醒要短，不要连续铺垫和补免责声明。")
    if any("重点不是" in x or "你怎么应对" in x for x in removed):
        rules.append("删掉过渡型设问和论文式转场，直接给应对方法。")
    if any("不是概念，是命令" in x for x in removed):
        rules.append("少写口号式二段 punch；如果下一段已有硬信息，直接进入信息。")
    if any("冷清得让我意外" in x or "静默就是暴风雨前" in x for x in removed):
        rules.append("删除解释情绪的漂亮句，保留具体对比数据和一句真实反应即可。")
    if any("这不是概念，是长期订单" in x for x in removed):
        rules.append("同一个判断不要重复包装；前文已经说明订单逻辑时，删掉补强句。")
    if any("填补真空" in x or "价值重估" in x or "时代红利" in x for x in removed):
        rules.append("删掉宏大叙事词，如 `价值重估`、`时代红利`、`填补真空`，除非原文必须保留。")
    if any("别被短期情绪" in x or "产业趋势至少延续" in x or "涨五倍八倍十倍" in x for x in removed):
        rules.append("策略段不要写成劝买小作文；保留主线和标的方向，删掉情绪管理和收益想象。")
    if any("硬科技IPO的钱" in x or "不是炒完就散" in x for x in removed):
        rules.append("删掉看似聪明的政策/资金流升华句，保留产业事实。")
    if any("惊吓似的" in x for x in removed) and any("韭菜" in x for x in added):
        rules.append("市场波动段可以写真实散户体感，比如 `给韭菜们吓死了`，比 `短暂惊吓` 更有人味。")
    if any("触发点很简单" in x for x in removed) and any("因为" in x and "带着" in x for x in added):
        rules.append("原因句可以直接写成 `因为某人/某公司带着某东西来了`，不要写成新闻解释句。")
    if any("商业化意图极其清晰" in x or "更多开发者" in x for x in removed):
        rules.append("删除公司公告式商业化复述；保留能支撑股价反应的关键事实即可。")
    if any("每个问题都没有确定性答案" in x for x in removed) and any("你在做什么" in x for x in added):
        rules.append("业务主线不清时，用直接质问代替长串不确定性分析，如 `你在做什么？你的客户群体到底有没有清晰？`。")
    if any("简单说就是" in x for x in removed):
        rules.append("少用 `简单说就是` 做总结，能删就删。")
    if any("这不是一个" in x or "估值重构" in x or "更长时间的财务数据" in x for x in removed):
        rules.append("新闻稿结尾不要补平衡免责声明；保留市场正在追问什么即可。")

    if not rules:
        rules.append("本轮编辑较轻：保持短段、直接判断、少解释桥。")

    return rules


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: learn_diff.py BEFORE.md AFTER.md", file=sys.stderr)
        return 2

    before_path = Path(argv[0])
    after_path = Path(argv[1])
    learned_path = Path(__file__).resolve().parents[1] / "rules" / "learned.md"

    rules = extract_rules(lines(before_path), lines(after_path))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    block = "\n".join([f"\n## Learned {stamp} from {before_path.name} -> {after_path.name}", *[f"- {r}" for r in rules], ""])
    with learned_path.open("a", encoding="utf-8") as handle:
        handle.write(block)
    print("\n".join(rules))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
