# Huajiao Finance Writer

一个中文财经写作 Skill。

它不是通用爆款文案 prompt，也不是“帮我润色一下”的套话工具。

这是我用自己的约 2 万条历史推文蒸馏 voice，再经过 35+ 轮真实文章改写、手改、反向学习沉淀出来的 finance writer。

目标很简单：

把财经、市场、公司、宏观、新闻稿、研报、个人观点这些原始材料，改写成更像一个真实人在说话的长社交文案。

保留事实。

去掉 AI 味。

留下判断。

别把人写没。

## 它解决什么问题

大多数 AI 写财经文案有几个毛病：

- 太像研报。
- 太像新闻稿。
- 太爱总结。
- 太会写漂亮废话。
- 太喜欢“不是 A，而是 B”。
- 太容易把长材料压成 280 字摘要。
- 太喜欢补背景、补原因、补一个看起来懂行的判断。
- 越润色越不像人。

这个 Skill 反过来做。

它不是让文章更工整。

它是让文章更像你真的看完材料后，坐在屏幕前，用自己的语气讲出来。

## 核心链路

```text
原文
-> DeepSeek 仿写花椒 voice
-> 一次 cleanup：anti-ai + say-it-human + renwei-writing
-> 你手改
-> learner 从 before/after 学规则
-> 下一轮更像你
```

注意：cleanup 不是三次 API 调用。

它是一次 DeepSeek cleanup，但会同时读取三层本地规则：

1. `rules/anti-ai.md`
2. `vendor/say-it-human`
3. `vendor/renwei-writing`

这样更省、更稳，也不容易把文案洗成 AI 编辑部。

## 这个 Skill 的写作口味

它更偏向：

- 先判断，再解释。
- 短段。
- 允许毛边。
- 允许半句梗。
- 允许口语粘连。
- 少做平衡分析。
- 少写漂亮收尾。
- 财经观点要敢站队。
- 长文不要硬压成一句话。
- 读起来像社交平台上的人，不像机构周报。

比如它会更倾向于：

```text
涨价才是好事啊。
不涨价，他的利润，你的股票增值，谁来买单？
```

而不是：

```text
需要注意的是，价格上涨能否持续传导至下游仍有待观察。
```

## 它不做什么

不做评分器。

不做 dashboard。

不做向量库。

不做 agent swarm。

不做自动发布。

不假装这是模型微调。

它只是一个很朴素的写作 harness：

每次写完，你改。

每次改完，它学。

学到的是规则，不是神秘玄学。

## 文件结构

```text
huajiao-finance-writer/
├── SKILL.md
├── agents/openai.yaml
├── rules/
│   ├── voice.md          # 从个人推文蒸馏出的 voice
│   ├── writer.md         # 稳定写作规则
│   ├── constraints.md    # 硬约束，不许再犯的错
│   ├── anti-ai.md        # 去 AI 味清洗规则
│   └── learned.md        # 35+ 轮手改沉淀规则
├── scripts/
│   ├── deepseek_generate.py
│   ├── distill_voice.py
│   ├── learn_diff.py
│   └── self_check.py
└── vendor/
    ├── say-it-human/
    └── renwei-writing/
```

## 使用方式

准备 DeepSeek key。

不要写进仓库。

推荐放到本地文件：

```bash
echo "你的 deepseek key" > ~/.codex/secrets/deepseek_api_key.txt
```

运行：

```bash
DEEPSEEK_API_KEY_FILE=~/.codex/secrets/deepseek_api_key.txt \
VOICE_OUTPUT_MODE=long-social \
python3 scripts/deepseek_generate.py source.md out.md
```

输出：

```text
out-raw.md   # 第一轮仿写
out.md       # 清洗后的可手改版本
```

## 输出模式

`long-social`：默认，长社交文案。

`thread`：拆成 3-6 条连续帖子。

`short`：280 字以内短帖。只有你明确要短帖时才用。

```bash
VOICE_OUTPUT_MODE=thread python3 scripts/deepseek_generate.py source.md out.md
```

## 自我迭代

你改完 `out.md`，另存为 `after.md`。

然后跑：

```bash
python3 scripts/learn_diff.py out.md after.md
```

它会把具体可复用规则追加到：

```text
rules/learned.md
```

下一轮生成会自动读取。

## 两层学习

`learned.md` 负责越来越像你。

比如：

- 少写安全尾巴。
- 别强行总结。
- 可以保留粗糙连接。
- 可以用真实散户体感。
- 财经判断要更直接。

`constraints.md` 负责越来越少犯蠢。

比如：

- 不许编事实。
- 不许补不存在的行业背景。
- 不许泄露 API key。
- 长文断流时不要加新框架。

## 为什么用 DeepSeek

因为这个 Skill 的定位不是“模型崇拜”，而是稳定可复现的写作链路。

同一套规则、同一个 API、同一个 before/after 学习方式，比到处换模型更重要。

Prompt 决定它怎么开始。

规则决定它怎么收敛。

你的手改决定它怎么进化。

## 适合的材料

- 雪球长文
- 财经新闻稿
- A 股 / 美股评论
- 公司财报摘要
- 券商研报要点
- 宏观政策声明
- 产业链材料
- 个人财经观点

## 不适合的材料

- 需要严肃合规审查的投顾内容
- 需要实时行情验证的交易建议
- 需要法律、税务、医疗结论的高风险文本
- 不允许改写或转载的受版权保护全文

## 重要提醒

这个 Skill 是写作工具，不是投资建议工具。

它会努力保留来源事实，但不会替你验证事实真假。

如果要发布涉及行情、财报、政策、公司公告的内容，自己再查一次原始来源。

## Credits

本项目整合了以下开源/公开 Skill 思路：

- `taxueseek/say-it-human`
- `orange2ai/renwei-writing`

相关文件已放在 `vendor/` 下，并保留各自 license。

## License

见 [LICENSE.md](./LICENSE.md)。

本仓库中我的脚本与规则以 MIT 发布。

`vendor/renwei-writing` 适用其原始双许可：开源/个人用途免费，闭源商业用途需商业授权。

`vendor/say-it-human` 适用 MIT License。
