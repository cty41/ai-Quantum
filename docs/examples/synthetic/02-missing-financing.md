---
case_id: 02-missing-financing
title: 合成示例：融资缺失，卖压判断不能完成
synthetic: true
real_quotes: false
real_news: false
frozen_as_of: 合成日 D 09:20 Asia/Shanghai
rule_version: 2026-11-14.2
expects_data: 检查不完整
expects_structure: 本次未评估结构
expects_execution: 检查不完整
expects_overall: 检查不完整
---

# 合成示例 02：融资缺失

本页是合成的，不是行情。冻结 as-of：合成日 D 09:20 Asia/Shanghai。规则版本 `2026-11-14.2`。

收盘形态用的价格来自 `https://example.invalid/synthetic/syn001-close`，会话为合成日 D-1 的常规收盘，单位和复权口径都写了不复权。这段价格只说明 K 线在场，不证明卖压已经结束。

融资条目：

- 来源 URL 或官方页面标识：缺失
- 检索时间：合成日 D 09:16 Asia/Shanghai
- 数据 as-of：不适用，因为没有读到披露
- 会话：不适用
- 单位：不适用
- 复权或公司行为口径：不适用
- 摘录：页面未打开
- 规则版本：`2026-11-14.2`

价格假设依赖「融资净偿还不再大幅加速」。没有这条证据，卖压判断不能完成。这是阻断性缺口。缺数不能支持钝化判断。

板块规则在本卡已填，但卖出可行性依赖尚未完成的卖压判断，所以执行问保持「检查不完整」。

- 数据结论：检查不完整
- 结构结论：本次未评估结构
- 执行结论：检查不完整
- 总结论：检查不完整

受影响的判断：卖压是否减弱；能否把这只合成证券写成继续观察的持有结论。
