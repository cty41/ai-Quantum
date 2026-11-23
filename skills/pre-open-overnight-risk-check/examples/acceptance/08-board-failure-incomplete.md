---
case_id: 08-board-failure-incomplete
title: 合成示例：必试官方公告栏取数失败时结论为检查不完整
synthetic: true
real_quotes: false
real_news: false
expects_status: 检查不完整
must_contain:
  - 合成
  - 检查不完整
  - 未取到
must_not_contain:
  - 未见风险
  - 没有这件事
  - 结论：无风险
  - 结论：无重大新闻
  - 文号
---

# 合成示例 08：公告栏未取到

本页的失败是合成的。打不开页面不能写成「未见风险」或「没有这件事」。已经取到的合成海外收盘仍要报告。

- 技能：`pre-open-overnight-risk-check`
- 记录版本：synthetic-08
- 原交易假设：合成假设：观察流动性修复
- 当次观察名单：合成标的甲（本地市场）、合成锚乙（海外）
- 调用方截止时间：合成日 D 09:10 Asia/Shanghai
- 实际交付时间：合成日 D 09:10 Asia/Shanghai
- 结论：检查不完整

## 必试渠道覆盖审计

| 渠道 | 结果 | 来源与时点 | 备注 |
| --- | --- | --- | --- |
| 上交所通知公告栏 | 已取到 | https://example.invalid/synthetic/sse-ok-8 合成日 D 08:40 Asia/Shanghai | 窗口内无新增合成规则 |
| 深交所通知公告栏 | 未取到 | https://example.invalid/synthetic/szse-fail-8 合成日 D 08:41 Asia/Shanghai | 直接页面没有打开 |
| 北交所通知公告栏 | 未取到 | https://example.invalid/synthetic/bse-fail-8 合成日 D 08:42 Asia/Shanghai | 每次必试。直接页面没有打开 |
| 证监会通知公告栏 | 已取到 | https://example.invalid/synthetic/csrc-ok-8 合成日 D 08:43 Asia/Shanghai | 窗口内无新增合成规则 |
| 观察公司及指定同业公告、停复牌、投资者关系 | 已取到 | https://example.invalid/synthetic/ir-8 | 无停复牌 |
| 指定海外核心公司正常时段收盘 | 已取到 | 合成已授权行情源 | 合成 101，对照前收合成 100 |
| 指定海外核心公司已公布盘后 | 已取到 | 同上 | 合成 102，比较基准是同日常规收盘 |
| 至少一家独立电讯发现源（财联社 / 上证报 / 新华财经） | 已取到 | https://example.invalid/synthetic/wire-8 | 没有被用来填补未打开的公告栏 |
| 与当期岗位和事件相关的公开发言 | 已取到 | https://example.invalid/synthetic/speech-none-8 | 窗口内无合成发言 |

深交所和北交所两栏未取到。窗口内换过一次候选地址，截止到达后停止重试。

## 事实

合成锚乙的常规收盘和盘后已经分开记下。这不能代替没有打开的公告栏。

## 未核实线索

无。

## 含义

已取到的海外价格不换算成 A 股开盘涨跌。公告栏未取到，所以不能判断窗口内有没有正式规则。

## 缺口

深交所通知公告栏、北交所通知公告栏未取到。受影响的判断：市场交易与两融制度、以及其他只会出现在这两栏的正式规则，本次不能下结论。

总结论必须包含「检查不完整」。不得写成「未见风险」，也不得写成「没有这件事」。
