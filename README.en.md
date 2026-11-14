# ai-Quantum

[中文](README.md)

<a id="purpose"></a>

## Purpose

This repository is an A-share liquidity-repair research toolkit for a horizon of several trading days to several weeks: an observation discipline, plus a pre-open overnight risk check. The rules say how to verify the data session, use only completed sessions, and look together at whether selling pressure is fading, whether peers are consistent, whether price is finding support, and how much room remains inside marked historical trading zones. Entry, continued holding, and exit are written separately. For an existing position, a protective reference moves up only after a higher valid pullback low has been confirmed.

It is not a validated edge, not a live data product, and not automatic trading. It is not a general short-term framework for other markets. Other markets are not tested here. An overseas name, if one appears, is only an external anchor or a peer named for that run.

The canonical rules are [docs/strategy.md](docs/strategy.md). This page is an entry point and does not restate them. Changes are listed in [CHANGELOG.md](CHANGELOG.md). The current documentation version is `2026-11-14.2`.

<a id="naming"></a>

## Name

The name `ai-Quantum` alludes to the name of Soros's Quantum Fund. It is only a name. This repository is not affiliated with that fund, is not an endorsement, and is not comparable in approach, leverage, organization, or results.

<a id="status"></a>

## Maturity

- What exists is Markdown: the discipline, blank templates, and two checklist skills under `skills/` in this repository. Read them inside a complete clone. The original single-name closing-shape alert and the daily three-name volume review intended since 2026-11-13 are different. The latter is not a deployed program.
- This is not a verified profitable strategy, and no backtest result is published here. One outcome does not prove a statistical edge.
- There is no runnable application, no live quote or news integration, no scheduler, and no automatic order. Analysis skills stay separate from any future data adapter. None is included now.
- The license is the [MIT License](LICENSE) at the repository root. The copyright holder is Frank Cheng, year 2026.

<a id="quick-start"></a>

## Quick start

There is no install command, test command, or start command. The supported use is to clone the whole repository and read it inside that complete clone.

1. Read the [strategy](docs/strategy.md).
2. Before an observation, save a private copy of the [trade plan](docs/templates/trade-plan.md) and fill that copy. Do not commit the filled card.
3. Afterward, do the same with the [review card](docs/templates/review.md).
4. For the close, margin balance, peers, and VWAP, follow the [liquidity-repair skill](skills/liquidity-repair/SKILL.md). Field definitions are in the [indicator dictionary](skills/liquidity-repair/indicators.md). The [Yizhongtian example](skills/liquidity-repair/examples/yizhongtian.md) only shows how 300308, 300502, and 300394 are used. It contains no prices.
5. For a pre-open check, follow the [skill](skills/pre-open-overnight-risk-check/SKILL.md) and fill the [output template](skills/pre-open-overnight-risk-check/output-template.md). The [example configuration](skills/pre-open-overnight-risk-check/examples/config.example.yaml) only shows fields. It is not a holding and not an enabled job.
6. Use `skills/liquidity-repair/SKILL.md` and `skills/pre-open-overnight-risk-check/SKILL.md` where they sit in the clone. Ordinary Cursor or other agents do not auto-install those files. [llms.txt](llms.txt) is navigation only: it does not load files and it grants nothing. Do not copy `skills/` or a skill that links to `../../docs` into a private skill folder as an install. Those relative links would break.

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

The shared rules do not fix a ticker, a price, a quantity, or a position-size threshold. The caller supplies the watchlist, horizon, cutoff, evidence location, and recipients for that run.

<a id="data"></a>

## Data and sources

The checks live in the strategy, the [liquidity indicators](skills/liquidity-repair/indicators.md), and the [pre-open source guide](skills/pre-open-overnight-risk-check/sources.md). This page keeps only the boundaries:

- Separate the regular close, after-hours, futures, and closed-market quotations. Keep each timestamp in its original timezone and show an Asia/Shanghai equivalent. Calendars include holidays and daylight-saving time. A weekday is not automatically a session.
- Search snippets and cached pages are not fresh prices. Candidate pages are not a connected integration. No live fetch was recorded when these documents were written.
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
| [CHANGELOG.md](CHANGELOG.md) | Documentation changes. Current version `2026-11-14.2` |
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
