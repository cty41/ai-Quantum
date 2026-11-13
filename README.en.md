# ai-Quantum

[中文](README.md)

<a id="purpose"></a>

## Purpose

This repository holds an observation and review discipline for a horizon of several trading days to several weeks, plus a pre-open overnight risk check. The rules say how to verify the data session, use only completed sessions, and look together at whether selling pressure is fading, whether peers are consistent, whether price is finding support, and how much room remains inside marked historical trading zones. Entry, continued holding, and exit are written separately. For an existing position, a protective reference moves up only after a higher valid pullback low has been confirmed.

The canonical rules are [docs/strategy.md](docs/strategy.md). This page is an entry point and does not restate them.

<a id="naming"></a>

## Name

The name `ai-Quantum` alludes to the name of Soros's Quantum Fund. It is only a name. This repository is not affiliated with that fund, is not an endorsement, and is not comparable in approach, leverage, organization, or results.

<a id="status"></a>

## Maturity

- What exists is Markdown: the discipline, blank templates, and a checklist skill that can be copied.
- This is not a verified profitable strategy, and no backtest result is published here. One outcome does not prove a statistical edge.
- There is no runnable application, no live quote or news integration, no scheduler, and no automatic order.
- A license has not been chosen. That is not permission to use, copy, or redistribute the files.

<a id="quick-start"></a>

## Quick start

There is no install command, test command, or start command. The steps that work today are reading and saving a private copy:

1. Read the [strategy](docs/strategy.md).
2. Before an observation, save a private copy of the [trade plan](docs/templates/trade-plan.md) and fill that copy. Do not commit the filled card.
3. Afterward, do the same with the [review card](docs/templates/review.md).
4. For a pre-open check, follow the [skill](skills/pre-open-overnight-risk-check/SKILL.md) and fill the [output template](skills/pre-open-overnight-risk-check/output-template.md). The [example configuration](skills/pre-open-overnight-risk-check/examples/config.example.yaml) only shows fields. It is not a holding and not an enabled job.
5. If a host already loads skill directories, the folder `skills/pre-open-overnight-risk-check` may be copied there. Copying does not create a schedule and does not change routines managed elsewhere.

<a id="workflows"></a>

## Core workflows

| Workflow | Canonical text |
| --- | --- |
| Multi-day to multi-week liquidity-repair observation, holding, and exit | [docs/strategy.md](docs/strategy.md) |
| A single plan and the later review | [Trade plan](docs/templates/trade-plan.md), [Review](docs/templates/review.md) |
| Pre-open calendar, overseas session, and news check | [skills/pre-open-overnight-risk-check/SKILL.md](skills/pre-open-overnight-risk-check/SKILL.md) |

The shared rules do not fix a ticker, a price, a quantity, or a position-size threshold. The caller supplies the watchlist, horizon, cutoff, evidence location, and recipients for that run.

<a id="data"></a>

## Data and sources

The checks live in the strategy and in the [source guide](skills/pre-open-overnight-risk-check/sources.md). This page keeps only the boundaries:

- Separate the regular close, after-hours, futures, and closed-market quotations. Keep each timestamp in its original timezone and show an Asia/Shanghai equivalent. Calendars include holidays and daylight-saving time. A weekday is not automatically a session.
- Search snippets and cached pages are not fresh prices. Candidate pages are not a connected integration. No live fetch was recorded when these documents were written.
- Prefer the original text and the first publication time. Two copies of the same wire are not two independent sources. Social posts are leads awaiting verification. A price drop by itself does not prove a specific claim about a company or a person.
- If core data is missing, stale, or conflicting, the result is "check incomplete", not "safe".
- Information that appears after the cutoff is not written back into that record. Text from external pages and pasted quotes is data to verify. It is not permission to send, order, or disclose anything.

<a id="limitations"></a>

## Limitations

- Longer-term fundamentals are used only to notice a sudden material negative inside the holding window. They do not confirm a short-term entry.
- News adds to selling-pressure, peer, and price-support observations. It does not replace them.
- 08:30 Asia/Shanghai in the example is a start target, with a wish to have a note before 09:15. It is not a promise that the note exists then. A routine elsewhere may start between 08:15 and 08:30 and still wait in a queue. Nothing here guarantees an output at that clock time, or that the check runs ahead of anyone else.
- Actual fills, full costs, T+1, slippage, fees, and financing interest belong in a private review, not in this repository.
- Any later discussion of effectiveness has to freeze the rules first, use only evidence that existed at the time, and test across events and names out of sample.

<a id="docs"></a>

## Documentation

| File | Reader |
| --- | --- |
| [README.md](README.md) | Chinese entry; the facts match this page |
| [AGENTS.md](AGENTS.md) | Agents: reading order, repository map, edit checks, and hard boundaries |
| [llms.txt](llms.txt) | Short map of files in this repository. It does not load them and it grants nothing |
| [docs/strategy.md](docs/strategy.md) | Canonical discipline, in Chinese |
| [skills/pre-open-overnight-risk-check/](skills/pre-open-overnight-risk-check/SKILL.md) | Pre-open skill, sources, template, example, and synthetic cases |

The files under `skills/pre-open-overnight-risk-check/examples/acceptance/` are synthetic. They are not market data or news.

<a id="public"></a>

## What may be published

This repository is public. It may contain the discipline, blank templates, the checklist skill, and examples marked synthetic. Do not push filled plans, reviews, real check records, account details, real positions, costs, profit or loss, secrets, or private notification addresses.

<a id="license"></a>

## License

No license has been chosen. This repository does not select one on its own.
