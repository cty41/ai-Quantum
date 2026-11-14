---
case_id: 03-unresolved-window-multiple
title: 合成示例：20 日窗口未解决，仍去计算倍数
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

# 合成示例 03：未解决的窗口不能产出倍数

本页是合成的，不是行情。冻结 as-of：合成日 D 15:20 Asia/Shanghai。规则版本 `2026-11-14.2`。

计划快照把近 20 日是否含当日、停牌怎么计，都留成未解决。复权口径写了不复权，但这不能补上窗口选择。

有人仍写出「成交量是近 20 日均量的 2.4 倍」。该算式被拒绝，不能用来支持放量判断。窗口未解决时不计算相对均量的倍数。被拒绝的数字只留在这里，说明错误发生过，不进入事实。

证据摘录只保留：成交量数值来自 `https://example.invalid/synthetic/syn001-volume`，检索时间合成日 D 15:18，会话为常规收盘，单位为股。倍数一栏写「因口径未解决而未计算」。

这是阻断性缺口。依赖倍数的放量判断不能完成。

- 数据结论：检查不完整
- 结构结论：本次未评估结构
- 执行结论：检查不完整
- 总结论：检查不完整

受影响的判断：阶段放量是否成立，以及任何把该倍数当作入场或持有理由的句子。
