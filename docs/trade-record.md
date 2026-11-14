# 交易记录

- 文档版本：`2026-11-14.3`。下面的共享字段自 `2026-11-14.2` 起没有改集合；新记录填写当次使用的文档版本。
- 用途：同一笔观察从盘前、入场或观察、持有或退出，到复盘，共用这一份记录
- 性质：人工研究记录。不是自动交易，不是实况新闻监听，也不是已经验证的优势

空白计划见 [交易计划卡](templates/trade-plan.md)。盘前填写见 [盘前输出模板](../skills/pre-open-overnight-risk-check/output-template.md)。收盘、入场或观察、持有或退出、复盘的检查正文见 [流动性修复输出模板](../skills/liquidity-repair/output-template.md)。证据字段的总约定见 [证据约定](evidence-contract.md)。合成走查见 [examples/synthetic/README.md](examples/synthetic/README.md)。

## 一份记录，多次追加

一次观察只有一份交易记录。每次检查在末尾追加一节，写明自己的截止时间。追加不改写已经写下的判断，也不用后来的价格或新闻替换当时的句子。

每份记录至少带这些共享字段。不适用就写「不适用」，不要留空。

| 字段 | 含义 |
| --- | --- |
| 记录编号 | 这一笔自己的编号。不写账户或券商 |
| 持有窗口 | 数个交易日至数周中的这一次 |
| 价格假设 | 当次要检验的那句话 |
| 证据截止（as-of） | 这次检查允许使用的最晚证据时间。保留原始时区，并给出 Asia/Shanghai 对照 |
| 当前可卖数量 | 按当时规则还能卖出的数量。未知就写未知，不编造 |
| 保护参考及其依据 | 当前值、旧值、确认它的已完成结构，以及证据时间。没有则写「尚未建立」 |
| 未关闭缺口 | 分开阻断性缺口和非阻断缺口 |
| 规则版本 | 写这份记录时生效的文档版本。仓库当前文档版本是 `2026-11-14.3` |

保护参考是结构风险提示。它不是保证能够成交的价格，也不是必须守到才可以考虑退出的价位。

## 三个问题分开回答

每一次检查都分开回答下面三问，不并成一次通过或一次失败。

| 问题 | 可用结论 | English |
| --- | --- | --- |
| 数据是否足够、仍新、口径是否一致 | 数据足够、仍新且口径一致；或「检查不完整」 | data are sufficient, fresh, and consistent in basis; or "check incomplete" |
| 结构是否仍支持假设 | 结构尚可，可继续观察；结构转弱；结构破坏；本次未评估结构；尚不可上移保护参考 | structure still supports continued observation; structure has weakened; structure has failed; structure not assessed this check; protection reference must not be raised yet |
| 计划按现行规则能否执行 | 按现行规则可以执行所写计划；计划按现行规则不可执行；或因规则未填而「检查不完整」 | the written plan is executable under current rules; plan not executable under current rules; or "check incomplete" |

总结论可以同时包含多句。数据缺失、过期、冲突，或某项判断所需口径仍未解决时，总结论必须包含「检查不完整」，列出受影响的判断，不得写成风险已经排除。阻断性缺口存在时，不得写成新买入已经通过，也不得把总结论写成「按现行规则可以执行所写计划」。

板块涨跌幅限制或最小申报单位没有填写时，卖出可行性是「检查不完整」，不得写成计划可以执行。已经写明规则，并且跳空或跌停使保护参考价不能被假设成交时，执行结论是「计划按现行规则不可执行」。

复权口径空白时，成交均价和价格的比较是「检查不完整」。两种复权口径混在同一次比较里，同样是「检查不完整」。

### 阻断与非阻断

阻断性缺口使依赖它的那一问不能得出放行结论。例子：核心价格缺失或过期、来源冲突、比较所需要的复权口径空白或互相冲突、用仍未解决的近 20 日窗口算出倍数、判断卖出可行性时没有填写板块涨跌幅或最小申报单位、把保护参考写成已经成交的卖出价。

非阻断缺口要写明，但不单独否定其他已经完成的判断。例子：本次声明不对照指数、一条已标明剔除的旧闻、某个明确写了「不适用」且本问并不依赖的字段。

## 每条证据

每条核心证据写全这些字段。不适用就写「不适用」。

- 来源 URL，或官方页面标识
- 检索时间
- 数据 as-of 时间
- 会话：常规收盘、盘后、期货、休市报价，或其他写明的会话
- 单位
- 复权或公司行为口径
- 保留的摘录或数据片段
- 规则版本

只有摘要、缓存，或页面没有打开：来源状态写明，相关判断进入「检查不完整」。

## 计划快照不改

[交易计划卡](templates/trade-plan.md) 一旦作为某个规则版本的快照写下，就不再修改。后来的规则变化写成新版本，保留旧快照。检查只追加证据和当时的三问答案。

复盘对三件事分开写，见 [复盘卡](templates/review.md)：

1. 价差相对当时写下的成本和成交。费用或利息未知，就不要写成已审计净盈亏。
2. 当时有效的规则有没有被遵守。
3. 规则本身要不要改。若要改，那是新版本的提议，不是回头改旧快照，也不是用后来的价格或新闻重写当时的结论。

## 持有与现在卖出的情景比较

需要比较继续持有和现在卖出时，在同一份记录末尾追加一节，不另建记录，也不改计划快照。字段、费用口径和两结果限度见 [情景比较](hold-sell-compare.md)。这一节仍然分开写证据、结构和执行。盈亏平衡门槛不是已测得的概率。真实期望不能估计时写「无法估计」，总结论包含「检查不完整」。

## 盘前的外部或隔夜事件

盘前可以追加「外部或隔夜事件观察」。只记录已经取得的来源和时点。知道隔夜下跌，不等于当时能够在高点卖出，也不等于这只证券必须在开盘卖出。这不是新闻监听，也不另建技能。

## 怎么在仓库里走一遍

1. 读 [纪律](strategy.md) 的范围：A 股、数个交易日至数周的流动性修复。
2. 另存一份私人 [交易计划卡](templates/trade-plan.md)。填市场、板块、规则来源、可卖数量和申报约束。未知留未知。
3. 盘前用 [盘前模板](../skills/pre-open-overnight-risk-check/output-template.md) 追加一节，回答三问。
4. 入场或观察、已有仓位的持有或退出、复盘，分别用 [流动性修复输出模板](../skills/liquidity-repair/output-template.md) 的对应章节追加。三者不混成一段。
5. 对照 [合成走查 01](examples/synthetic/01-complete-walkthrough.md)。再看 [02](examples/synthetic/02-missing-financing.md) 到 [06](examples/synthetic/06-gap-limit-down.md)。这些页都是合成的，不是行情或新闻。

## 已有的一笔过程

[300308 过程记录](cases/300308-2026-11.md) 是这一份模板写入之前的历史说明。不要把它改写成当时已经使用了 `2026-11-14.2` 的字段。其中约 6.94% 的自述价差，以及讨论里的 567.89 元高点，不是已验证优势，也不是保证能够成交的价格。

## English labels

The canonical text of this file is Chinese. English pages use these equivalents: "check incomplete"; "structure still supports continued observation"; "plan not executable under current rules"; "protection reference must not be raised yet". A protective reference is not a guaranteed fill and is not a price that must be reached before an exit may be considered.
