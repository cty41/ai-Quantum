---
case_id: 05-mixed-adjustment-vwap
title: 合成示例：成交均价与价格的复权口径不一致
synthetic: true
real_quotes: false
real_news: false
frozen_as_of: 合成日 D 10:30 Asia/Shanghai
rule_version: 2026-11-14.2
expects_data: 检查不完整
expects_structure: 本次未评估结构
expects_execution: 检查不完整
expects_overall: 检查不完整
---

# 合成示例 05：复权口径不能混比

本页是合成的，不是行情。冻结 as-of：合成日 D 10:30 Asia/Shanghai。规则版本 `2026-11-14.2`。

两条都已打开，单位都是元和股，会话都是当日尚未走完的连续竞价，因此价格本身也只能预警，不能当作已完成 K 线的确认。这里要单独拒绝的是口径。

成交均价证据：`https://example.invalid/synthetic/vwap`，检索时间合成日 D 10:28，数据 as-of 合成日 D 10:25，摘录为按成交额除以股数得到 10.00。复权或公司行为口径：不复权。

最新价证据：`https://example.invalid/synthetic/last`，检索时间合成日 D 10:28，数据 as-of 合成日 D 10:25，摘录 10.40。复权或公司行为口径：前复权。

不复权的成交均价不能和前复权的价格比高低。若其中一条口径空白，比较同样不能做。本页两条都填了，但是彼此冲突，仍然是阻断性缺口。

- 数据结论：检查不完整
- 结构结论：本次未评估结构
- 执行结论：检查不完整
- 总结论：检查不完整

受影响的判断：现价在成交均价之上还是之下，以及任何依赖这个比较的持有或退出。
