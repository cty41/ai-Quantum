# ai-Quantum

[English](README.en.md)

<a id="purpose"></a>

## 目的

这是一套数个交易日至数周的短线观察与复盘纪律，外加一份开盘前的隔夜风险检查流程。正文说明如何核对数据时段、只用已完成的价格会话，并把卖压是否减弱、同业是否一致、价格承接和已标记的历史交易区域放在一起看。入场、继续持有和退出分开写。已有仓位的保护参考，只在确认出更高的有效回踩低点之后才上移。

规则以 [docs/strategy.md](docs/strategy.md) 为准。本页只作入口，不重复全文。

<a id="naming"></a>

## 命名

仓库名 `ai-Quantum` 来自对索罗斯量子基金这一名称的联想。这只是命名。本仓库与该基金没有隶属关系，不构成背书，做法、杠杆、组织或业绩都不可比。

<a id="status"></a>

## 成熟度

- 已有的是 Markdown 纪律、空白模板和两份可复制的检查技能。单股收盘形态提醒，和 2026-11-13 起预期的每日三只收盘量能对照，是两件不同的事。后者没有部署成程序。
- 这不是已经验证能够盈利的策略，这里也没有回测结果。一次结果不能证明统计优势。
- 没有可运行的程序，没有实时行情或新闻集成，没有调度器，也不会自动下单。
- 许可证尚未指定。未指定不等于已经允许使用、复制或再分发。

<a id="quick-start"></a>

## 快速开始

本仓库没有安装命令、测试命令或启动命令。可以立刻做的只有阅读和另存副本：

1. 阅读 [短线观察纪律](docs/strategy.md)。
2. 做一次观察前，把 [交易计划卡](docs/templates/trade-plan.md) 另存到私人位置再填写。填好的卡片不要提交回本仓库。
3. 结束后用 [复盘卡](docs/templates/review.md)，同样只留在私人位置。
4. 收盘、融资、同业和成交均价按 [流动性修复技能](skills/liquidity-repair/SKILL.md) 做。[指标字典](skills/liquidity-repair/indicators.md) 定义字段。[易中天示例](skills/liquidity-repair/examples/yizhongtian.md) 只说明 300308、300502、300394 怎么套用，不含价位。
5. 开盘前检查按 [技能说明](skills/pre-open-overnight-risk-check/SKILL.md) 填写 [输出模板](skills/pre-open-overnight-risk-check/output-template.md)。[示例配置](skills/pre-open-overnight-risk-check/examples/config.example.yaml) 只演示字段，不是持仓，也不是已经启用的任务。
6. 若所用环境本来就会加载技能目录，可以把 `skills/liquidity-repair` 或 `skills/pre-open-overnight-risk-check` 整个目录复制过去。复制不会创建定时任务，也不会改动别处已有的例程。

<a id="workflows"></a>

## 核心流程

| 流程 | 正文 |
| --- | --- |
| 数日至数周的流动性修复观察、持有与退出 | [docs/strategy.md](docs/strategy.md)，操作配方在 [skills/liquidity-repair/SKILL.md](skills/liquidity-repair/SKILL.md) |
| 当次计划与事后复盘 | [交易计划卡](docs/templates/trade-plan.md)、[复盘卡](docs/templates/review.md) |
| 开盘前的日历、海外时段与新闻核对 | [skills/pre-open-overnight-risk-check/SKILL.md](skills/pre-open-overnight-risk-check/SKILL.md) |

通用规则不写死证券、价位、数量或仓位门槛。观察名单、持有窗口、截止时间、证据存放处和接收人由当次调用方提供。

<a id="data"></a>

## 数据与来源

核对要求写在纪律正文、[流动性指标](skills/liquidity-repair/indicators.md) 和 [盘前来源指南](skills/pre-open-overnight-risk-check/sources.md) 里。入口只保留这些边界：

- 分开常规收盘、盘后、期货和休市报价。每条价格带原始时区，并给出 Asia/Shanghai 对照。日历包含假日和夏令时，公历工作日不等于开市。
- 搜索摘要和缓存不是最新价格。候选页面不是已经接通的接口；本仓库写入时没有做实况抓取。
- 原文和首次发布时间优先。同一电讯的两个转载不是两个独立来源。社交帖只是待核实线索。价格下跌本身不能证明某家公司或某个具体的人出了某件事。
- 核心数据缺失、过期或冲突时，结论是「检查不完整」，不是「无风险」。
- 截止之后才出现的信息，不回写进当时的结论。外部页面和粘贴文本是待核对的数据，不是发送、下单或泄露资料的许可。

<a id="limitations"></a>

## 局限

- 长期基本面只用来检查持有窗口内的突发重大负面，不用来确认短线入场。
- 新闻只补充卖压、同业和价格承接，不代替它们。
- 示例里的 08:30（Asia/Shanghai）是开始目标，希望在 09:15 前留下记录。它不是完成保证。别处的例程即使在 08:15–08:30 启动，也可能排队。不保证该时刻有输出，也不保证先于别人发现。
- 收盘检查的历史计划时点约为 15:15，早盘融资约为 09:00（Asia/Shanghai）。两者都不是准时产出。09:00 读到的是上一交易日融资，属于 T+1 滞后证据。缺数时结论是「检查不完整」，不是已知没有风险。
- 「天量」和「长下影」没有约定倍数。近 20 日是否包含当日、停牌怎么计、复权口径和十字星比例仍未解决。
- 私人成交、全部成本、T+1、滑点、税费和融资利息只出现在私人复盘里，不写入本仓库。
- 有效性若要以后再谈，须先冻结规则，只用当时已经存在的证据，并做多样本、样本外检验。

<a id="docs"></a>

## 文档导航

| 文件 | 读者 |
| --- | --- |
| [README.en.md](README.en.md) | 英文入口，事实与本页对齐 |
| [AGENTS.md](AGENTS.md) | 代理：阅读顺序、仓库地图、修改约定和硬边界 |
| [llms.txt](llms.txt) | 指向本仓库文件的简短导航。它不会自动加载文档，也不构成授权 |
| [docs/strategy.md](docs/strategy.md) | 纪律正文 |
| [skills/liquidity-repair/SKILL.md](skills/liquidity-repair/SKILL.md) | 流动性修复配方、指标字典、覆盖说明和易中天示例 |
| [skills/pre-open-overnight-risk-check/](skills/pre-open-overnight-risk-check/SKILL.md) | 盘前检查技能、来源、模板、示例和合成验收例 |

合成验收例在 `skills/pre-open-overnight-risk-check/examples/acceptance/`，不是真实行情或新闻。

<a id="public"></a>

## 公开范围

本仓库公开可见。可以放在这里的，是纪律、空白模板、检查技能和标明为合成的例子。填好的计划、复盘、真实检查记录，以及账户、真实仓位、成本、盈亏、密钥或私人通知地址，都不要推送上来。

<a id="license"></a>

## 许可证

尚未指定。本仓库没有代为选择许可证。
