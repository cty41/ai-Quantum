---
case_id: 04-old-news-duplicate-rumor
title: 合成示例：旧闻、转载合并与未核实传闻
synthetic: true
real_quotes: false
real_news: false
expects_status: 完整
must_contain:
  - 合成
  - 旧闻剔除
  - 转载合并
  - 线索待核实
  - 事实
  - 未核实线索
  - 含义
  - 不能证明
must_not_contain:
  - 结论：无风险
  - 结论：无重大新闻
---

# 合成示例 04：旧闻、转载合并与未核实传闻

本页的稿件、人物和价格都是合成的。不涉及已核实的历史事件，也不对应任何真实个人。

- 技能：`pre-open-overnight-risk-check`
- 记录版本：synthetic-04
- 持有窗口：合成窗口，从合成日 D-2 到合成日 D
- 原交易假设：合成假设：观察修复，同时排除窗口内的突发重大负面
- 当次观察名单：合成公司甲
- 显示对照：Asia/Shanghai
- 调用方截止时间：合成日 D 09:10 Asia/Shanghai
- 实际交付时间：合成日 D 09:02 Asia/Shanghai
- 名义开始时间：合成日 D 08:30 Asia/Shanghai
- 结论：完整

## 日历与上一完整海外时段

- 本地市场合成日 D 开市。合成日历直接页面已打开
- 海外上一完整常规时段是合成日 D-1，无假日
- America/New_York 标准时。常规收盘 16:00 对照 Asia/Shanghai 为合成日 D 05:00

## 行情

| 名称 | 会话 | 比较基准 | 原始时间与时区 | Asia/Shanghai | 数值 | 来源 | 直接页面或已授权源 | 检索时间 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 合成公司甲的海外相关标的 | 常规收盘 | 再前一完整常规收盘 合成 50 | 合成日 D-1 16:00 America/New_York | 合成日 D 05:00 | 合成 47 | 合成直接行情页 | 是 | 合成日 D 08:45 Asia/Shanghai | 合成下跌。下跌不是新闻 |

盘后与期货本次有直接页面，数值分别为相对同日常规收盘的合成 46.5，以及合成合约相对前结算的合成 46。它们只说明会话不同，不映射为本地开盘。

## 新闻与线索

| 去重键 | 事件发生 | 首次发布 | 文章更新 | 检索时间 | 截止 | 实际交付 | 原始链接 | 独立来源数 | 处理 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic-old-1 | 合成日 D-14 | 合成日 D-14 09:00 America/New_York | 无。今晨转载未改写首次发布 | 合成日 D 08:47 Asia/Shanghai | 合成日 D 09:10 Asia/Shanghai | 合成日 D 09:02 Asia/Shanghai | https://example.invalid/synthetic/old-release | 1 | 旧闻剔除 |
| synthetic-wire-1 | 页面未载明 | 合成日 D-1 15:00 America/New_York（对照合成日 D 04:00 Asia/Shanghai） | 无 | 合成日 D 08:49 Asia/Shanghai | 合成日 D 09:10 Asia/Shanghai | 合成日 D 09:02 Asia/Shanghai | https://example.invalid/synthetic/wire-original | 1 | 转载合并 |
| synthetic-social-1 | 页面未载明 | 合成日 D 08:20 Asia/Shanghai 的帖子时间 | 无 | 合成日 D 08:52 Asia/Shanghai | 合成日 D 09:10 Asia/Shanghai | 合成日 D 09:02 Asia/Shanghai | https://example.invalid/synthetic/social-post | 0 | 线索待核实 |

`synthetic-wire-1` 同时出现在 `https://example.invalid/synthetic/wire-copy-a` 和 `https://example.invalid/synthetic/wire-copy-b`。两页是同一合成电讯的转载，合并为一条，独立来源数是 1，不是 2。

截止之后才出现的任何补充，都不写入上表。

## 事实

1. 合成旧稿首次发布于窗口开始之前。今晨的转载页面被看见，并按旧闻剔除。
2. 合成电讯的原文直接页在截止前打开。两个转载站不增加独立来源数。该合成电讯的正文是例行市场综述，没有公司正式发布的突发重大负面。
3. 合成直接行情页显示，相关标的常规收盘从合成 50 到合成 47。这是价格事实，比较基准是再前一完整常规收盘。

在已打开的公司合成新闻室、合成电讯原文和合成行情直接页内，截至合成日 D 09:10 Asia/Shanghai，没有看到需要列入本次窗口的重大负面。

## 未核实线索

合成社交帖称「合成人物 P」涉及不利事项。帖子不是原始文件，也没有第二份独立采写。价格从合成 50 到合成 47 不能证明该说法，也不能把下跌解释成针对这个合成人物或合成公司甲的已核实事件。

## 含义

原假设没有从这些合成材料里获得新的突发负面事实。社交帖保持为线索。若要它变成事实，需要在之后的另一次检查中打开原始来源，并且不能把那次之后的结果改写进本记录。

下跌不换算成合成公司甲的本地开盘幅度。

## 与卖压、同业和承接的关系

- 卖压：本次未评估
- 同业是否一致：本次未评估
- 价格承接：本次未评估

电讯和帖子没有代替这三项。

## 缺口

无核心缺口。转载和旧闻已处理，不列为缺口。

## 去重与证据索引

| 去重键或行情条目 | 地址 | 检索时间 | 访问结果 |
| --- | --- | --- | --- |
| synthetic-old-1 | https://example.invalid/synthetic/old-release | 合成日 D 08:47 Asia/Shanghai | 打开。首次发布早于窗口 |
| synthetic-old-1 转载 | https://example.invalid/synthetic/old-reprint | 合成日 D 08:48 Asia/Shanghai | 打开。不新开事实 |
| synthetic-wire-1 | https://example.invalid/synthetic/wire-original | 合成日 D 08:49 Asia/Shanghai | 打开原文 |
| synthetic-wire-1 转载 | https://example.invalid/synthetic/wire-copy-a | 合成日 D 08:49 Asia/Shanghai | 同一电讯 |
| synthetic-wire-1 转载 | https://example.invalid/synthetic/wire-copy-b | 合成日 D 08:50 Asia/Shanghai | 同一电讯 |
| synthetic-social-1 | https://example.invalid/synthetic/social-post | 合成日 D 08:52 Asia/Shanghai | 打开帖子，保持未核实 |
| 行情 | https://example.invalid/synthetic/quote-direct | 合成日 D 08:45 Asia/Shanghai | 打开直接页面 |

## 用词核对

- 是否避免「无风险」：是
- 「没有看到重大负面」是否限定了已查来源和截止时间：是
- 是否把截止后才知道的内容写进了当时的结论：否
- 是否出现下单或仓位：否
