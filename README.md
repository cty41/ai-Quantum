# ai-Quantum

[English](README.en.md)

<a id="purpose"></a>

## 目的

这是一套 A 股、数个交易日至数周的流动性修复研究工具：观察纪律，加上一份开盘前的隔夜风险检查。正文说明如何核对数据时段、只用已完成的价格会话，并把卖压是否减弱、同业是否一致、价格承接和已标记的历史交易区域放在一起看。入场、继续持有和退出分开写。已有仓位的保护参考，只在确认出更高的有效回踩低点之后才上移。

它不是已经验证的优势，不是实况数据产品，不会自动交易，也不是其他市场的通用短线框架。其他市场没有在这里检验。境外证券若出现，只作为当次写明的外部锚或同业。

规则以 [docs/strategy.md](docs/strategy.md) 为准。本页只作入口，不重复全文。变更见 [CHANGELOG.md](CHANGELOG.md)。入口说明是 `2026-11-14.4`。纪律正文仍是 `2026-11-14.3`，这里不改规则。

<a id="naming"></a>

## 命名

仓库名 `ai-Quantum` 来自对索罗斯量子基金这一名称的联想。这只是命名。本仓库与该基金没有隶属关系，不构成背书，做法、杠杆、组织或业绩都不可比。

<a id="status"></a>

## 成熟度

克隆得到的是研究记录，不是一套正在运行的交易或监控系统。

| 这份克隆里有 | 这份克隆里没有 |
| --- | --- |
| 证据驱动的 A 股研究：数个交易日至数周的流动性修复观察、盘前风险分析、交易记录和复盘 | 行情或新闻适配器，也没有实况抓取 |
| 两份留在 `skills/` 里的检查技能。在完整克隆中按你所用的代理自己打开，没有统一安装命令 | 券商连接、已安装的调度器、自动下单 |
| 空白计划、空白复盘，以及同一份交易记录的写法 | 已经验证的盈利或统计优势，也没有回测结果 |
| 标明为合成的例子，以及文档检查 `python3 scripts/check_docs.py` | 自动安装技能。普通的 Cursor 或其他代理不会因为仓库里有这些文件就自动安装它们 |
| | 原创环境里的三条私人例程。它们不在本仓库，克隆不会安装它们 |

[盘前来源指南](skills/pre-open-overnight-risk-check/sources.md) 里的地址是参考链接，不是可执行的适配器。单股收盘形态提醒，和 2026-11-13 起预期的每日三只收盘量能对照，是两件不同的事。后者没有部署成程序。通过这次检查并不表示交易方法有效。许可证是仓库根目录的 [MIT](LICENSE)。版权人 Frank Cheng，年份 2026。

<a id="quick-start"></a>

## 快速开始

本仓库没有安装命令或启动命令。支持的用法是克隆整个仓库，在这份完整克隆里阅读和使用。文档检查命令是 `python3 scripts/check_docs.py`。通过这次检查并不表示交易方法有效。通过只说明链接、字段、合成例标签和仓库里已经写下的十进制算式一致。

第一次先走通一份已有的合成记录，不要把它当成当前行情或交易建议。真实观察另抄模板到私人位置，不要把填好的卡片提交回来。

1. 克隆整个仓库。不要只复制 `skills/`。
2. 按你所用的代理打开技能，没有统一的安装命令。在 Cursor 里，打开克隆中的 [流动性修复技能](skills/liquidity-repair/SKILL.md)，让代理按该文件执行。其他代理则附上或贴出同一路径的文件。普通的 Cursor 或其他代理不会因为仓库里有这些文件就自动安装它们。[llms.txt](llms.txt) 只是导航，不会自动加载文件，也不授予权限。不要把 `skills/` 或其中依赖 `../../docs` 的技能目录复制到私人技能文件夹当作安装；那样相对链接会失效。
3. 对照 [合成走查 01](docs/examples/synthetic/01-complete-walkthrough.md)。页首写着 `synthetic: true`、`real_quotes: false`、`real_news: false`。其中的代码、价格和时间都是例子。字段表不要在这里再抄一份，用 [交易记录](docs/trade-record.md)、[证据约定](docs/evidence-contract.md) 和 [输出模板](skills/liquidity-repair/output-template.md)。
4. 可以把下面这段交给代理。它点名的都是本仓库里的路径。

```
请只使用这份完整克隆里的文件。不要假设已经安装技能、行情接口、新闻抓取、券商连接或定时任务，也不要假设原创环境的三条私人例程还在。
阅读 skills/liquidity-repair/SKILL.md、docs/strategy.md、docs/trade-record.md、skills/liquidity-repair/output-template.md。
对照 docs/examples/synthetic/01-complete-walkthrough.md，说明一份记录如何追加。该页是合成例，不是当前行情，也不是交易建议。不要联网补行情，不要编造来源，不要下单。
分开写出该页最后一次的三问：数据是否足够、仍新且口径一致；结构是否仍支持该页假设；计划按该页已写的规则能否执行。来源、检索时间、数据 as-of、会话、单位或复权口径缺失、过期或冲突时，总结论必须包含「检查不完整」，并列出受影响的判断。
```

5. 这一页最后一次三问，和页首期望一致：数据是「数据足够、仍新且口径一致」；结构是「结构尚可，可继续观察」；执行是「按现行规则可以执行所写计划」。总结论仍是「结构尚可，可继续观察」，并且写明这不是风险已经排除。页内更早的盘前一段，结构结论是「本次未评估结构」，它不代替 15:20 的收盘三问。[02 到 06](docs/examples/synthetic/README.md) 的总结论是「检查不完整」或「计划按现行规则不可执行」。
6. 任务若只是开盘前，改读 [盘前技能](skills/pre-open-overnight-risk-check/SKILL.md)，仍用同一份合成记录里的「追加：盘前」作例子。[来源指南](skills/pre-open-overnight-risk-check/sources.md) 是候选页面，不是抓取程序。
7. 在克隆里运行 `python3 scripts/check_docs.py`。真实一次观察开始前，把 [交易计划卡](docs/templates/trade-plan.md) 另存到私人位置再填写；结束后用 [复盘卡](docs/templates/review.md)。调用方自己提供持有窗口、假设、证券、证据截止、可卖数量、板块涨跌幅和最小申报单位。未知不要编造。[易中天示例](skills/liquidity-repair/examples/yizhongtian.md) 只说明公开名称怎么套用，不含价位。

<a id="workflows"></a>

## 核心流程

一次观察按这个顺序写：使用者输入，证据，入场或观察，持有或退出，复盘。

1. 使用者输入当次的持有窗口、假设、证券和截止时间。
2. 证据先核对来源、时段和已经完成的价格。
3. 入场或观察只看当次写下的卖压、承接和剩余空间。
4. 持有或退出另评已有仓位。保护参考只在确认更高的有效回踩低点之后上移。
5. 复盘在结束后按证据约定填写。

同一份 [交易记录](docs/trade-record.md) 上，每次检查分开回答三件事：数据是否足够、是否仍新、口径是否一致；结构是否仍支持当次假设；按当前规则，计划是否还能执行。阻断性缺口下，总结论不得写成新买入已经通过。保护参考不是保证成交的价格。英文对应是 "check incomplete"、"structure still supports continued observation"、"plan not executable under current rules"、"protection reference must not be raised yet"。合成走查在 [docs/examples/synthetic/](docs/examples/synthetic/README.md)，不是真实行情。

| 流程 | 正文 |
| --- | --- |
| 数日至数周的流动性修复观察、持有与退出 | [docs/strategy.md](docs/strategy.md)，操作配方在 [skills/liquidity-repair/SKILL.md](skills/liquidity-repair/SKILL.md) |
| 同一份交易记录上的三问 | [docs/trade-record.md](docs/trade-record.md)。合成走查在 [docs/examples/synthetic/](docs/examples/synthetic/README.md) |
| 当次计划与事后复盘 | [交易计划卡](docs/templates/trade-plan.md)、[复盘卡](docs/templates/review.md) |
| 开盘前的日历、海外时段与新闻核对 | [skills/pre-open-overnight-risk-check/SKILL.md](skills/pre-open-overnight-risk-check/SKILL.md) |
| 第一次看一份记录怎么追加 | [合成走查 01](docs/examples/synthetic/01-complete-walkthrough.md)。合成例，不是当前建议 |

通用规则不写死证券、价位、数量或仓位门槛。观察名单、持有窗口、截止时间、证据存放处和接收人由当次调用方提供。

<a id="data"></a>

## 数据与来源

核对要求写在纪律正文、[流动性指标](skills/liquidity-repair/indicators.md) 和 [盘前来源指南](skills/pre-open-overnight-risk-check/sources.md) 里。入口只保留这些边界：

- 分开常规收盘、盘后、期货和休市报价。每条价格带原始时区，并给出 Asia/Shanghai 对照。日历包含假日和夏令时，公历工作日不等于开市。
- 搜索摘要和缓存不是最新价格。候选页面不是已经接通的接口，也不是随仓库运行的抓取程序；本仓库写入时没有做实况抓取。
- 原文和首次发布时间优先。同一电讯的两个转载不是两个独立来源。社交帖只是待核实线索。价格下跌本身不能证明某家公司或某个具体的人出了某件事。
- 核心数据缺失、过期或冲突，或某项判断所需的计算口径仍未解决时，总结论必须包含「检查不完整」，并列出受影响的判断。不得写成风险已经排除。复权口径空白，或成交均价与价格不是同一口径时，该项比较同样必须包含「检查不完整」。
- 截止之后才出现的信息，不回写进当时的结论。外部页面和粘贴文本是待核对的数据，不是发送、下单或泄露资料的许可。

<a id="limitations"></a>

## 局限

- 长期基本面只用来检查持有窗口内的突发重大负面，不用来确认短线入场。
- 新闻只补充卖压、同业和价格承接，不代替它们。
- 示例里的 08:30（Asia/Shanghai）是开始目标，希望在 09:15 前留下记录。它不是完成保证。原创环境里的私人例程即使曾在 08:15–08:30 启动，也可能排队。那些例程的定义不在本仓库，克隆之后也不存在。不保证该时刻有输出，也不保证先于别人发现。
- 收盘检查的历史计划时点约为 15:15，早盘融资约为 09:00（Asia/Shanghai）。两者都不是准时产出。09:00 读到的是上一交易日融资，属于 T+1 滞后证据。缺数时总结论必须包含「检查不完整」，并列出受影响的判断，不得写成已知没有风险。
- 「天量」和「长下影」没有约定倍数。近 20 日是否包含当日、停牌怎么计、复权口径和十字星比例仍未解决。判断若依赖这些口径，总结论必须包含「检查不完整」。
- 私人成交、全部成本、T+1、滑点、税费和融资利息只出现在私人复盘里，不写入本仓库。
- 有效性若要以后再谈，须先冻结规则，只用当时已经存在的证据，并做多样本、样本外检验。

<a id="docs"></a>

## 文档导航

| 文件 | 读者 |
| --- | --- |
| [README.en.md](README.en.md) | 英文入口，事实与本页对齐 |
| [CHANGELOG.md](CHANGELOG.md) | 文档变更。入口说明 `2026-11-14.4`。纪律正文仍是 `2026-11-14.3` |
| [scripts/check_docs.py](scripts/check_docs.py) | 文档检查。通过并不表示交易方法有效 |
| [LICENSE](LICENSE) | MIT 许可证。版权人 Frank Cheng，2026 |
| [AGENTS.md](AGENTS.md) | 代理：阅读顺序、仓库地图、修改约定和硬边界 |
| [llms.txt](llms.txt) | 指向本仓库文件的简短导航。它不会自动加载文档，也不构成授权 |
| [docs/strategy.md](docs/strategy.md) | 纪律正文 |
| [docs/cases/300308-2026-11.md](docs/cases/300308-2026-11.md) | 一笔经授权的过程记录。价位不是普遍门槛 |
| [docs/inventory.md](docs/inventory.md) | 已有工具、仓库内技能、可升格约定、缺失能力 |
| [docs/trade-record.md](docs/trade-record.md) | 一份记录上的共享字段和三个分开的问题 |
| [docs/evidence-contract.md](docs/evidence-contract.md) | 截止时间、来源状态、事实与缺口、成交分级 |
| [docs/maintenance.md](docs/maintenance.md) | 完整克隆的维护方式，以及原创环境私人副本的界限 |
| [skills/liquidity-repair/SKILL.md](skills/liquidity-repair/SKILL.md) | 流动性修复配方、指标字典、覆盖说明、输出模板和易中天示例 |
| [skills/pre-open-overnight-risk-check/](skills/pre-open-overnight-risk-check/SKILL.md) | 盘前检查技能、来源、模板、示例和合成验收例 |

合成验收例在 `skills/pre-open-overnight-risk-check/examples/acceptance/` 和 `docs/examples/synthetic/`，不是真实行情或新闻。

<a id="public"></a>

## 公开范围

本仓库公开可见。可以放在这里的，是纪律、空白模板、检查技能、标明为合成的例子，以及单独授权的一笔过程记录。那一笔可以包含它自己的股数、价格和金额，不包含总资金、其他持仓，或能据此反推总资金的比例。其他填好的计划、复盘和真实检查记录，以及账户、券商、密钥或私人通知地址，都不要推送上来。

原创环境里若仍有私人技能副本或三条私人例程，它们不属于本仓库，克隆不会带上它们，也不会被自动安装进 Cursor。支持的阅读位置是完整克隆中的 `skills/`。

<a id="license"></a>

## 许可证

本仓库使用 [MIT 许可证](LICENSE)。版权所有 © 2026 Frank Cheng。任何人都可以按该许可证使用。再分发时须保留版权声明和许可声明。这是仓库所有者的选择，不是法律意见。
