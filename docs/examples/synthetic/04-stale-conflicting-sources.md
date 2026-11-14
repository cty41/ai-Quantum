---
case_id: 04-stale-conflicting-sources
title: 合成示例：来源过期并且互相冲突
synthetic: true
real_quotes: false
real_news: false
frozen_as_of: 合成日 D 15:20 Asia/Shanghai
rule_version: 2026-11-14.2
expects_data: 检查不完整
expects_structure: 本次未评估结构
expects_execution: 检查不完整
expects_overall: 检查不完整
---

# 合成示例 04：过期与冲突

本页是合成的，不是行情。冻结 as-of：合成日 D 15:20 Asia/Shanghai。调用方写下的数据最长龄期是 30 分钟。规则版本 `2026-11-14.2`。

两条收盘价不能并成一个价格。

第一条：`https://example.invalid/synthetic/close-a`，检索时间合成日 D 15:19，数据 as-of 合成日 D 常规收盘，摘录收盘 10.50，单位元，复权口径不复权。

第二条：`https://example.invalid/synthetic/close-b`，检索时间合成日 D 15:19，数据 as-of 合成日 D-2 常规收盘，摘录收盘 8.10，单位元，复权口径不复权。它旧于调用方写下的龄期。两个已打开页面的收盘价也不一致。

不得挑选对自己有利的一条继续写结构。冲突和过期都是阻断性缺口。

- 数据结论：检查不完整
- 结构结论：本次未评估结构
- 执行结论：检查不完整
- 总结论：检查不完整

受影响的判断：收盘价取哪一个，以及依赖该收盘价的持有或退出。
