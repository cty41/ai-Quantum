# 持有与卖出比较的例子

这些文件供 `python3 scripts/hold_sell.py` 读取。合成文件不是行情。回顾教学不是券商核验模型，也不是普遍门槛。算法见 [持有与现在卖出的情景比较](../../hold-sell-compare.md)。

| 文件 | 要看的结果 |
| --- | --- |
| [synthetic-unknown.json](synthetic-unknown.json) | 零成本教学。概率省略。门槛可算，真实期望是「无法估计」 |
| [synthetic-positive.json](synthetic-positive.json) | 假设概率 0.8 时条件增量为正。仍然不是持有指令 |
| [synthetic-negative.json](synthetic-negative.json) | 假设概率 0.2 时条件增量为负。仍然不是卖出指令 |
| [synthetic-costs-sensitivity.json](synthetic-costs-sensitivity.json) | 显式假设费用，并改 p、上沿和滑点。费率不是交易所现行表 |
| [zhongji-2026-11-12-teaching.json](zhongji-2026-11-12-teaching.json) | 回顾教学。截止 2026-11-12 10:59:30 Asia/Shanghai。P0=546.62，上沿 553，下沿 544、541、537，100 股，忽略额外成本。门槛展示为 29.1%、46.8%、60.1%，不是测得概率 |
| [invalid-probability.json](invalid-probability.json) | 概率 1.2。命令拒绝，不截断 |
| [invalid-nan.json](invalid-nan.json) | NaN。命令拒绝 |
| [invalid-quantity.json](invalid-quantity.json) | 数量 0。命令拒绝 |

回顾教学不把后来自述的 547.50 元卖出放进输入。精确成交时间未知。当时的兑现建议来自 553 未能收回和同业转弱的讨论，不是一条已经证明的更高卖出期望。价位说明见 [300308 过程记录](../../cases/300308-2026-11.md)。
