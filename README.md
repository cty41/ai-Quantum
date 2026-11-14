# ai-Quantum

[English](README.en.md)

<a id="purpose"></a>

## 目的

这是一套 A 股、数个交易日至数周的流动性修复研究工具：观察纪律，加上一份开盘前的隔夜风险检查。正文说明如何核对数据时段、只用已完成的价格会话，并把卖压是否减弱、同业是否一致、价格承接和已标记的历史交易区域放在一起看。入场、继续持有和退出分开写。已有仓位的保护参考，只在确认出更高的有效回踩低点之后才上移。

它不是已经验证的优势，不是实况数据产品，不会自动交易，也不是其他市场的通用短线框架。其他市场没有在这里检验。境外证券若出现，只作为当次写明的外部锚或同业。

规则以 [docs/strategy.md](docs/strategy.md) 为准。本页只作入口，不重复全文。变更见 [CHANGELOG.md](CHANGELOG.md)，当前文档版本是 `2026-11-14.2`。

<a id="naming"></a>

## 命名

仓库名 `ai-Quantum` 来自对索罗斯量子基金这一名称的联想。这只是命名。本仓库与该基金没有隶属关系，不构成背书，做法、杠杆、组织或业绩都不可比。

<a id="status"></a>

## 成熟度

- 已有的是 Markdown 纪律、空白模板，以及放在本仓库 `skills/` 里的两份检查技能。在完整克隆中阅读它们。单股收盘形态提醒，和 2026-11-13 起预期的每日三只收盘量能对照，是两件不同的事。后者没有部署成程序。
- 这不是已经验证能够盈利的策略，这里也没有回测结果。一次结果不能证明统计优势。
- 没有可运行的程序，没有实时行情或新闻集成，没有调度器，也不会自动下单。分析技能与日后可能另写的数据适配分开；现在没有适配器。
- 许可证是仓库根目录的 [MIT](LICENSE)。版权人 Frank Cheng，年份 2026。

<a id="quick-start"></a>

## 快速开始

本仓库没有安装命令、测试命令或启动命令。支持的用法是克隆整个仓库，在这份完整克隆里阅读和使用。

1. 阅读 [短线观察纪律](docs/strategy.md)。
2. 做一次观察前，把 [交易计划卡](docs/templates/trade-plan.md) 另存到私人位置再填写。填好的卡片不要提交回本仓库。
3. 结束后用 [复盘卡](docs/templates/review.md)，同样只留在私人位置。
4. 收盘、融资、同业和成交均价按 [流动性修复技能](skills/liquidity-repair/SKILL.md) 做。[指标字典](skills/liquidity-repair/indicators.md) 定义字段。[易中天示例](skills/liquidity-repair/examples/yizhongtian.md) 只说明 300308、300502、300394 怎么套用，不含价位。
5. 开盘前检查按 [技能说明](skills/pre-open-overnight-risk-check/SKILL.md) 填写 [输出模板](skills/pre-open-overnight-risk-check/output-template.md)。[示例配置](skills/pre-open-overnight-risk-check/examples/config.example.yaml) 只演示字段，不是持仓，也不是已经启用的任务。
6. `skills/liquidity-repair/SKILL.md` 和 `skills/pre-open-overnight-risk-check/SKILL.md` 留在仓库里的原位置使用。普通的 Cursor 或其他代理不会因为仓库里有这些文件就自动安装它们。[llms.txt](llms.txt) 只是导航，不会自动加载文件，也不授予权限。不要把 `skills/` 或其中依赖 `../../docs` 的技能目录复制到私人技能文件夹当作安装；那样相对链接会失效。

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

通用规则不写死证券、价位、数量或仓位门槛。观察名单、持有窗口、截止时间、证据存放处和接收人由当次调用方提供。

<a id="data"></a>

## 数据与来源

核对要求写在纪律正文、[流动性指标](skills/liquidity-repair/indicators.md) 和 [盘前来源指南](skills/pre-open-overnight-risk-check/sources.md) 里。入口只保留这些边界：

- 分开常规收盘、盘后、期货和休市报价。每条价格带原始时区，并给出 Asia/Shanghai 对照。日历包含假日和夏令时，公历工作日不等于开市。
- 搜索摘要和缓存不是最新价格。候选页面不是已经接通的接口；本仓库写入时没有做实况抓取。
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
| [CHANGELOG.md](CHANGELOG.md) | 文档变更。当前版本 `2026-11-14.2` |
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
