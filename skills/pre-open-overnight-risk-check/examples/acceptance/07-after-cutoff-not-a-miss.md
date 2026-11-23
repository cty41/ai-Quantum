---
case_id: 07-after-cutoff-not-a-miss
title: 合成示例：截止后才发出的发言不视为该次遗漏
synthetic: true
real_quotes: false
real_news: false
expects_status: 完整
must_contain:
  - 合成
  - 不视为该次遗漏
  - 下一个开盘前窗口
must_not_contain:
  - 本次遗漏
  - 周末定时
  - 文号
---

# 合成示例 07：截止后的发言不是该次遗漏

本页时间线是合成的。截止后的那句发言不回填进截止前的结论，也不写成这次检查漏掉了它。

- 技能：`pre-open-overnight-risk-check`
- 记录版本：synthetic-07
- 原交易假设：合成假设：观察流动性修复，截止前没有新的岗位发言
- 调用方截止时间：合成日 D 09:10 Asia/Shanghai
- 实际交付时间：合成日 D 09:08 Asia/Shanghai
- 回溯窗口：合成日 D-1 本地收盘至合成日 D 09:10 Asia/Shanghai
- 结论：完整

## 必试渠道覆盖审计

截止前，公开发言渠道已取到：合成列表 `https://example.invalid/synthetic/speech-before-7` 在合成日 D 08:55 Asia/Shanghai 打开，窗口内没有新的合成发言。其余必试渠道在本合成例中也已取到，包括北交所公告栏。

## 事实

在合成日 D 09:10 Asia/Shanghai 之前打开的来源里，没有新的合成发言。

## 留给下一窗口

合成日 D 09:40 Asia/Shanghai，一份合成逐字稿才首次公开，原话是：「合成岗位今天才说了这句话。」它晚于本次截止。它不视为该次遗漏。留给下一个开盘前窗口，并在那个窗口核对目标市场是否已经交易过它。本次不新增周末或盘中定时任务。

## 含义

截止前的假设没有被这句截止后的合成原话改写。不把 09:40 的句子写进 09:10 的事实。

## 缺口

无。总结论不包含「检查不完整」。在已打开的来源内、截至合成日 D 09:10 Asia/Shanghai，未见可核验的、会改变当期假设或四条影响链的事项。
