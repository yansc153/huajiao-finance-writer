<div align="center">

# Huajiao Finance Writer

### 2 万条个人推文蒸馏  
### 35+ 轮手改自修  
### 一个专门写中文财经长文的 Codex Skill

![Codex Skill](https://img.shields.io/badge/Codex-Skill-black)
![DeepSeek](https://img.shields.io/badge/Model-DeepSeek-4c6fff)
![Chinese Finance](https://img.shields.io/badge/Writing-Chinese%20Finance-red)
![Self Improving](https://img.shields.io/badge/Loop-Self--Improving-00a67e)
![No Slop](https://img.shields.io/badge/AI%20味-滚-orange)
![License](https://img.shields.io/badge/License-MIT%20%2B%20Vendor%20Terms-blue)

</div>

---

这不是一个通用 prompt

也不是“帮我润色一下”

这是一个财经写作 harness

原文进去

DeepSeek 写第一稿

三层去 AI 味

你手改

它学习

下一轮更像你

## 它怎么来的

我拿自己的约 2 万条历史推文蒸馏 voice

只学节奏、句式、断句、转折、语气

然后拿真实财经文章跑了 35+ 轮

每一轮都是：

```text
原文
→ DeepSeek 仿写花椒 voice
→ anti-ai + say-it-human + renwei-writing
→ 人手改
→ learner 学 before/after
→ learned.md 变厚
```

这就是现在这个版本

finance writer 究极版

当然，究极不是不会错

究极是错了能学

## 它写出来像什么

它不追求工整

它追求像人

比如它更愿意写：

```text
涨价才是好事啊
不涨价，他的利润，你的股票增值，谁来买单？
```

而不是：

```text
需要注意的是，价格上涨能否持续传导至下游仍有待观察
```

## 核心链路

```text
source.md
  ↓
DeepSeek imitation pass
  rules/voice.md
  rules/writer.md
  rules/constraints.md
  rules/learned.md
  ↓
out-raw.md
  ↓
one cleanup pass
  rules/anti-ai.md
  vendor/say-it-human
  vendor/renwei-writing
  ↓
out.md
  ↓
you edit
  ↓
after.md
  ↓
learn_diff.py
  ↓
rules/learned.md grows
```

## 安装

```bash
git clone https://github.com/yansc153/huajiao-finance-writer.git
cd huajiao-finance-writer
```

准备 DeepSeek key

不要写进仓库

```bash
mkdir -p ~/.codex/secrets
echo "你的 deepseek key" > ~/.codex/secrets/deepseek_api_key.txt
```

## 使用

```bash
DEEPSEEK_API_KEY_FILE=~/.codex/secrets/deepseek_api_key.txt \
VOICE_OUTPUT_MODE=long-social \
python3 scripts/deepseek_generate.py source.md out.md
```

输出两个文件：

```text
out-raw.md   第一轮仿写
out.md       清洗后的可手改版本
```

## 模式

```bash
VOICE_OUTPUT_MODE=long-social   # 默认，长社交文案
VOICE_OUTPUT_MODE=thread        # 3-6 条连续帖子
VOICE_OUTPUT_MODE=short         # 280 字以内短帖
```

默认不要 short

财经长文压成 280 字

很多时候就是把信息杀了

## 自我迭代

你改完 `out.md`

保存成 `after.md`

然后：

```bash
python3 scripts/learn_diff.py out.md after.md
```

它会把具体规则写进：

```text
rules/learned.md
```

下一次自动读取

这不是训练模型

这是训练你的写作系统

## 两个文件最重要

`rules/learned.md`

负责越来越像你

比如：

- 别强行总结
- 少写安全尾巴
- 允许粗糙连接
- 财经判断要直接
- 可以有真实散户体感

`rules/constraints.md`

负责越来越少犯蠢

比如：

- 不许编事实
- 不许泄露 key
- 不许补不存在的行业背景
- 不许把长文默认压成短帖

## 文件结构

```text
huajiao-finance-writer/
├── SKILL.md
├── rules/
│   ├── voice.md
│   ├── writer.md
│   ├── constraints.md
│   ├── anti-ai.md
│   └── learned.md
├── scripts/
│   ├── deepseek_generate.py
│   ├── distill_voice.py
│   ├── learn_diff.py
│   └── self_check.py
└── vendor/
    ├── say-it-human/
    └── renwei-writing/
```

## 适合

- 雪球长文
- 财经新闻
- A 股观点
- 美股观点
- 公司财报
- 券商研报
- 宏观政策
- 产业链材料
- 个人财经评论

## 不适合

- 投顾合规稿
- 实时交易建议
- 法律税务医疗结论
- 不能转载的版权全文
- 需要事实核验但你不打算核验的内容

## 重要提醒

这是写作工具

不是投资建议

它会尽量保留来源事实

但不会替你验证事实真假

发布前自己查原始来源

别偷懒

## Credits

本项目整合并本地 vendored：

- [`taxueseek/say-it-human`](https://github.com/taxueseek/say-it-human)
- [`orange2ai/renwei-writing`](https://github.com/orange2ai/renwei-writing)

感谢这两个项目

人味儿这件事

不是玄学

是少动一点

别装一点

## License

见 [LICENSE.md](./LICENSE.md)

我的脚本和本地规则 MIT

`vendor/say-it-human` 走 MIT

`vendor/renwei-writing` 保留原始双许可

闭源商业用途请看它自己的 license
