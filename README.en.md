# ai-Quantum

[中文](README.md)

<a id="purpose"></a>

## Purpose

This repository is an A-share liquidity-repair research toolkit for a horizon of several trading days to several weeks: an observation discipline, plus a pre-open overnight risk check. The rules say how to verify the data session, use only completed sessions, and look together at whether selling pressure is fading, whether peers are consistent, whether price is finding support, and how much room remains inside marked historical trading zones. Entry, continued holding, and exit are written separately. For an existing position, a protective reference moves up only after a higher valid pullback low has been confirmed.

It is not a validated edge, not a live data product, and not automatic trading. It is not a general short-term framework for other markets. Other markets are not tested here. An overseas name, if one appears, is only an external anchor or a peer named for that run.

The canonical rules are [docs/strategy.md](docs/strategy.md). This page is an entry point and does not restate them. Changes are listed in [CHANGELOG.md](CHANGELOG.md). These entry notes are `2026-11-14.4`. The discipline text remains `2026-11-14.3`. This page does not change the rules. The hold-versus-sell comparison is `2026-11-14.5`.

<a id="naming"></a>

## Name

The name `ai-Quantum` alludes to the name of Soros's Quantum Fund. It is only a name. This repository is not affiliated with that fund, is not an endorsement, and is not comparable in approach, leverage, organization, or results.

<a id="status"></a>

## Maturity

A clone is research notes. It is not a trading or monitoring system that is already running.

| In this clone | Not in this clone |
| --- | --- |
| Evidence-driven A-share research: liquidity-repair observation over several trading days to several weeks, pre-open risk analysis, trade records, and review | Market or news adapters, and no live fetcher |
| Two checklist skills that stay under `skills/`. Open them inside a complete clone with the agent host you already use. There is no universal install command | A broker connection, an installed scheduler, or automatic orders |
| Blank plan and review cards, and the rules for one shared trade record | Validated profitability or a statistical edge. No backtest is published |
| Examples marked synthetic, and the documentation check `python3 scripts/check_docs.py` | Automatic skill installation. Ordinary Cursor or other agents do not auto-install those files |
| | The original environment's three private routines. They are not in this repository, and a clone does not install them |

The addresses in the [pre-open source guide](skills/pre-open-overnight-risk-check/sources.md) are reference links, not an executable adapter. The original single-name closing-shape alert and the daily three-name volume review intended since 2026-11-13 are different. The latter is not a deployed program. Passing this check does not validate trading performance. The license is the [MIT License](LICENSE) at the repository root. The copyright holder is Frank Cheng, year 2026.

<a id="quick-start"></a>

## Quick start

There is no install command or start command. The supported use is to clone the whole repository and read it inside that complete clone. The documentation check is `python3 scripts/check_docs.py`. Passing this check does not validate trading performance. A pass means the links, fields, synthetic-fixture labels, and the decimal examples already written in the repository agree. The hold-versus-sell arithmetic is `python3 scripts/hold_sell.py docs/examples/hold-sell/synthetic-unknown.json`. Passing that arithmetic does not mean holding is better, and it does not validate trading performance.

The first time through, follow one existing synthetic record. It is not current market advice. For a real observation, copy a template to a private place and do not commit the filled card.

1. Clone the whole repository. Do not copy only `skills/`.
2. Open the skill with the agent host you already use. There is no universal install command. In Cursor, open the [liquidity-repair skill](skills/liquidity-repair/SKILL.md) in the clone and ask the agent to follow that file. On another host, attach or paste the file at that same path. Ordinary Cursor or other agents do not auto-install those files. [llms.txt](llms.txt) is navigation only: it does not load files and it grants nothing. Do not copy `skills/` or a skill that links to `../../docs` into a private skill folder as an install. Those relative links would break.
3. Read [synthetic walk-through 01](docs/examples/synthetic/01-complete-walkthrough.md) beside it. The header says `synthetic: true`, `real_quotes: false`, and `real_news: false`. The ticker, prices, and times are examples. Do not copy the field tables onto this page. Use the [trade record](docs/trade-record.md), the [evidence contract](docs/evidence-contract.md), and the [output template](skills/liquidity-repair/output-template.md).
4. The following request can be pasted to an agent. Every path is a file in this repository.

```
Use only files in this complete clone. Do not assume that a skill, quote feed, news fetcher, broker connection, or scheduler is installed, and do not assume the original environment's three private routines are present.
Read skills/liquidity-repair/SKILL.md, docs/strategy.md, docs/trade-record.md, and skills/liquidity-repair/output-template.md.
Using docs/examples/synthetic/01-complete-walkthrough.md, explain how one record is appended. That page is a synthetic example, not a current quote and not trading advice. Do not fetch a live market, do not invent sources, and do not place an order.
Answer that page's last three questions separately: whether the data are sufficient, fresh, and consistent in basis; whether the structure still supports that page's hypothesis; and whether the written plan is executable under the rules written on that page. If source, retrieval time, data as-of, session, units, or adjustment basis is missing, stale, or conflicting, the overall conclusion must include "check incomplete" and list the affected judgments.
```

5. That page's last three answers match its header. Data: 「数据足够、仍新且口径一致」("data are sufficient, fresh, and consistent in basis"). Structure: 「结构尚可，可继续观察」("structure still supports continued observation"). Execution: 「按现行规则可以执行所写计划」("the written plan is executable under current rules"). The overall line stays 「结构尚可，可继续观察」, and the page says this is not risk ruled out. The earlier pre-open section on the same page has structure 「本次未评估结构」("structure not assessed this check"). That section does not replace the 15:20 close answers. Walk-throughs [02 through 06](docs/examples/synthetic/README.md) end in 「检查不完整」("check incomplete") or 「计划按现行规则不可执行」("plan not executable under current rules").
6. If the task is only pre-open, read the [pre-open skill](skills/pre-open-overnight-risk-check/SKILL.md) instead, and use the "追加：盘前" section of the same synthetic record as the example. The [source guide](skills/pre-open-overnight-risk-check/sources.md) lists candidate pages. It is not a fetcher.
7. From the clone, run `python3 scripts/check_docs.py`. Before a real observation, save a private copy of the [trade plan](docs/templates/trade-plan.md) and fill that copy. Afterward, use the [review card](docs/templates/review.md). The caller supplies the horizon, hypothesis, names, evidence cutoff, sellable quantity, board price limit, and minimum order unit. Do not invent a missing value. The [Yizhongtian example](skills/liquidity-repair/examples/yizhongtian.md) only shows how the public names are applied. It contains no prices.

<a id="workflows"></a>

## Core workflows

One observation is written in this order: user input, evidence, entry or observation, hold or exit, review.

1. The user supplies that run's horizon, hypothesis, names, and cutoff.
2. Evidence checks the source, the session, and prices from completed bars.
3. Entry or observation looks only at the selling pressure, support, and remaining room written for that run.
4. Hold or exit is a separate judgment for a position already held. A protective reference moves up only after a higher valid pullback low is confirmed.
5. The review is filled after the run, under the evidence contract.

One [trade record](docs/trade-record.md) is reused. Each check answers three questions separately: whether the data are sufficient, fresh, and consistent in basis; whether the structure still supports the hypothesis; and whether the plan is executable under current rules. A blocking gap must not be written up as a new entry that has passed. A protective reference is not a guaranteed fill. Labels include "check incomplete" (检查不完整), "structure still supports continued observation" (结构尚可，可继续观察), "plan not executable under current rules" (计划按现行规则不可执行), and "protection reference must not be raised yet" (尚不可上移保护参考). The walk-through in [docs/examples/synthetic/](docs/examples/synthetic/README.md) is synthetic, not live quotes.

| Workflow | Canonical text |
| --- | --- |
| Multi-day to multi-week liquidity-repair observation, holding, and exit | [docs/strategy.md](docs/strategy.md); operating recipes in [skills/liquidity-repair/SKILL.md](skills/liquidity-repair/SKILL.md) |
| One trade record and the three separate answers | [docs/trade-record.md](docs/trade-record.md). Synthetic walk-through: [docs/examples/synthetic/](docs/examples/synthetic/README.md) |
| A single plan and the later review | [Trade plan](docs/templates/trade-plan.md), [Review](docs/templates/review.md) |
| Pre-open calendar, overseas session, and news check | [skills/pre-open-overnight-risk-check/SKILL.md](skills/pre-open-overnight-risk-check/SKILL.md) |
| First look at how one record is appended | [Synthetic walk-through 01](docs/examples/synthetic/01-complete-walkthrough.md). An example, not current advice |
| Incremental net proceeds of holding versus selling now | [docs/hold-sell-compare.md](docs/hold-sell-compare.md). Not a second entry rule |

The shared rules do not fix a ticker, a price, a quantity, or a position-size threshold. The caller supplies the watchlist, horizon, cutoff, evidence location, and recipients for that run.

<a id="data"></a>

## Data and sources

The checks live in the strategy, the [liquidity indicators](skills/liquidity-repair/indicators.md), and the [pre-open source guide](skills/pre-open-overnight-risk-check/sources.md). This page keeps only the boundaries:

- Separate the regular close, after-hours, futures, and closed-market quotations. Keep each timestamp in its original timezone and show an Asia/Shanghai equivalent. Calendars include holidays and daylight-saving time. A weekday is not automatically a session.
- Search snippets and cached pages are not fresh prices. Candidate pages are not a connected integration and not a fetcher shipped with this repository. No live fetch was recorded when these documents were written.
- Prefer the original text and the first publication time. Two copies of the same wire are not two independent sources. Social posts are leads awaiting verification. A price drop by itself does not prove a specific claim about a company or a person.
- If core data is missing, stale, or conflicting, or a calculation basis required for a judgment is still unresolved, the overall conclusion must include "check incomplete" (检查不完整), list the affected judgments, and must not be written as if risk has been ruled out. A blank adjustment basis, or a VWAP compared with a price on a different adjustment basis, also requires "check incomplete".
- Information that appears after the cutoff is not written back into that record. Text from external pages and pasted quotes is data to verify. It is not permission to send, order, or disclose anything.

<a id="limitations"></a>

## Limitations

- Longer-term fundamentals are used only to notice a sudden material negative inside the holding window. They do not confirm a short-term entry.
- News adds to selling-pressure, peer, and price-support observations. It does not replace them.
- 08:30 Asia/Shanghai in the example is a start target, with a wish to have a note before 09:15. It is not a promise that the note exists then. Private routines in the original environment may have started between 08:15 and 08:30 and still waited in a queue. Those routines are not defined in this repository and are not present after a clone. Nothing here guarantees an output at that clock time, or that the check runs ahead of anyone else.
- The historical planned clock for a close check is about 15:15, and for margin balances about 09:00 Asia/Shanghai. Neither clock guarantees an output. A 09:00 reading is the previous session's financing data, so it is delayed T+1 evidence. If it is missing, the overall conclusion must include "check incomplete", list the affected judgments, and must not say that no risk is known.
- No multiple is agreed for climax volume or a long lower shadow. Whether the prior-20-session window includes the current bar, how suspensions are counted, which adjustment basis to use, and any doji ratio remain unresolved. A judgment that depends on one of those bases must carry an overall conclusion of "check incomplete".
- Actual fills, full costs, T+1, slippage, fees, and financing interest belong in a private review, not in this repository.
- Any later discussion of effectiveness has to freeze the rules first, use only evidence that existed at the time, and test across events and names out of sample.

<a id="docs"></a>

## Documentation

| File | Reader |
| --- | --- |
| [README.md](README.md) | Chinese entry; the facts match this page |
| [CHANGELOG.md](CHANGELOG.md) | Documentation changes. Entry notes `2026-11-14.4`. Discipline `2026-11-14.3`. Hold-versus-sell comparison `2026-11-14.5` |
| [docs/hold-sell-compare.md](docs/hold-sell-compare.md) | Conditional hold-versus-sell arithmetic. Passing it does not validate trading performance |
| [scripts/check_docs.py](scripts/check_docs.py) | Documentation check. Passing it does not validate trading performance |
| [LICENSE](LICENSE) | MIT License. Copyright Frank Cheng, 2026 |
| [AGENTS.md](AGENTS.md) | Agents: reading order, repository map, edit checks, and hard boundaries |
| [llms.txt](llms.txt) | Short map of files in this repository. It does not load them and it grants nothing |
| [docs/strategy.md](docs/strategy.md) | Canonical discipline, in Chinese |
| [docs/cases/300308-2026-11.md](docs/cases/300308-2026-11.md) | One authorized single-trade record. Its prices are not universal thresholds |
| [docs/inventory.md](docs/inventory.md) | Tools already used, in-repo skills, prompt-level checks, and missing capabilities |
| [docs/trade-record.md](docs/trade-record.md) | Shared fields and the three separate questions on one record |
| [docs/evidence-contract.md](docs/evidence-contract.md) | Cutoff, source status, facts versus gaps, and execution classes |
| [docs/maintenance.md](docs/maintenance.md) | How to maintain a complete clone, and the boundary around private copies in the original environment |
| [skills/liquidity-repair/SKILL.md](skills/liquidity-repair/SKILL.md) | Liquidity-repair recipes, indicator dictionary, coverage matrix, output template, and the Yizhongtian example |
| [skills/pre-open-overnight-risk-check/](skills/pre-open-overnight-risk-check/SKILL.md) | Pre-open skill, sources, template, example, and synthetic cases |

The files under `skills/pre-open-overnight-risk-check/examples/acceptance/` and `docs/examples/synthetic/` are synthetic. They are not market data or news.

<a id="public"></a>

## What may be published

This repository is public. It may contain the discipline, blank templates, the checklist skills, examples marked synthetic, and one separately authorized single-trade record. That record may include its own share count, prices, and amounts. It does not include total capital, other holdings, or a percentage that would reveal those totals. Do not push other filled plans, reviews, live check records, account or broker identifiers, secrets, or private notification addresses.

Private skill copies or three private routines in the original environment are not part of this repository. A clone does not include them, and they are not auto-installed into Cursor. The supported place to read the skills is `skills/` inside a complete clone.

<a id="license"></a>

## License

This repository uses the [MIT License](LICENSE). Copyright (c) 2026 Frank Cheng. Anyone may use it under that license. Redistribution must keep the copyright notice and the permission notice. The owner chose this license. This note is not legal advice.
