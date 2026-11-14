#!/usr/bin/env python3
"""Compare incremental net proceeds of holding with selling now.

The benchmark is a timestamped executable-price assumption, not historical
buy cost and not paper profit. Arithmetic uses decimal.Decimal. A result is
not an order and not evidence that a trading method works.

    python3 scripts/hold_sell.py docs/examples/hold-sell/synthetic-unknown.json
    python3 scripts/hold_sell.py --text docs/examples/hold-sell/synthetic-unknown.json
    python3 scripts/test_hold_sell.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


PRICE_KINDS = {"sourced_observation", "user_assumption", "hypothetical_stress"}
PROBABILITY_KINDS = PRICE_KINDS | {"empirically_estimated"}
OVERALL_INCOMPLETE = "检查不完整"
CANNOT_ESTIMATE = "无法估计"
STRUCTURE_NOT_ASSESSED = "本次未评估结构"
EXEC_INCOMPLETE = "检查不完整"
EXEC_BLOCKED = "计划按现行规则不可执行"
EXEC_OK = "按现行规则可以执行所写计划"
EVIDENCE_OK = "数据足够、仍新且口径一致"
EVIDENCE_INCOMPLETE = "检查不完整"


class InputError(Exception):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("; ".join(errors))


def parse_document(text: str):
    if re.search(r"(?<![A-Za-z])[+-]?(?:NaN|Infinity|Inf)(?![A-Za-z])", text):
        raise InputError(["数字不是有限值：拒绝 NaN 和 Infinity，不把它们改成 0"])
    try:
        return json.loads(text, parse_float=Decimal, parse_int=Decimal)
    except json.JSONDecodeError as exc:
        raise InputError([f"JSON 无法解析：{exc}"]) from exc


def as_decimal(value, path: str) -> Decimal:
    if isinstance(value, bool) or value is None:
        raise InputError([f"{path} 不是有限数字"])
    if isinstance(value, Decimal):
        number = value
    elif isinstance(value, int):
        number = Decimal(value)
    elif isinstance(value, str):
        token = value.strip()
        if token.lower() in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity", "snan"}:
            raise InputError([f"{path} 不是有限数字"])
        try:
            number = Decimal(token)
        except InvalidOperation as exc:
            raise InputError([f"{path} 不是有限数字"]) from exc
    else:
        raise InputError([f"{path} 不是有限数字"])
    if not number.is_finite():
        raise InputError([f"{path} 不是有限数字"])
    return number


def require_text(value, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError([f"{path} 必须是非空字符串"])
    return value.strip()


def money(number: Decimal) -> str:
    text = format(number, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text if text else "0"


def percent_1(number: Decimal) -> str:
    quantized = (number * Decimal(100)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return format(quantized, "f")


def load_cost_block(raw, path: str, teaching: bool) -> dict[str, Decimal]:
    if not isinstance(raw, dict):
        raise InputError([f"{path} 必须写明佣金费率、最低佣金、税率和每股滑点"])
    keys = ("commission_rate", "commission_minimum", "tax_rate", "slippage_per_share")
    parsed: dict[str, Decimal] = {}
    for key in keys:
        if key not in raw:
            raise InputError([f"{path}.{key} 缺失。缺失的成本不会被当成 0"])
        parsed[key] = as_decimal(raw[key], f"{path}.{key}")
        if parsed[key] < 0:
            raise InputError([f"{path}.{key} 不能为负。更好的成交价应写在价格里，而不是负滑点"])
    if parsed["commission_rate"] > 1 or parsed["tax_rate"] > 1:
        raise InputError([f"{path} 的费率必须是不超过 1 的比例，不能写成百分数 5 这种未换算的数"])
    if teaching and any(parsed[key] != 0 for key in keys):
        raise InputError([f"{path} 在零成本教学模式下必须显式写成 0，不能另带费用"])
    return parsed


def sale_cash(price: Decimal, quantity: Decimal, cost: dict[str, Decimal]) -> dict[str, Decimal]:
    fill = price - cost["slippage_per_share"]
    if fill <= 0:
        raise InputError(["滑点之后的成交价必须大于 0"])
    gross = fill * quantity
    variable_commission = cost["commission_rate"] * gross
    commission = variable_commission if variable_commission > cost["commission_minimum"] else cost["commission_minimum"]
    tax = cost["tax_rate"] * gross
    net = gross - commission - tax
    return {
        "quoted_price": price,
        "fill_price": fill,
        "quoted_amount": price * quantity,
        "slippage_amount": cost["slippage_per_share"] * quantity,
        "gross_amount": gross,
        "commission": commission,
        "tax": tax,
        "net_cash": net,
    }


def price_record(raw, path: str) -> dict:
    if not isinstance(raw, dict):
        raise InputError([f"{path} 必须是带价格和出处类别的对象"])
    kind = raw.get("kind")
    if kind not in PRICE_KINDS:
        raise InputError([f"{path}.kind 必须是 sourced_observation、user_assumption 或 hypothetical_stress"])
    price = as_decimal(raw.get("price"), f"{path}.price")
    if price <= 0:
        raise InputError([f"{path}.price 必须大于 0"])
    units = require_text(raw.get("units"), f"{path}.units")
    adjustment = require_text(raw.get("adjustment"), f"{path}.adjustment")
    note = require_text(raw.get("note"), f"{path}.note")
    meta = {
        "source": raw.get("source", ""),
        "retrieved_at": raw.get("retrieved_at", ""),
        "as_of": raw.get("as_of", ""),
        "session": raw.get("session", ""),
    }
    sourced_gaps = []
    if kind == "sourced_observation":
        for key, value in meta.items():
            if not isinstance(value, str) or not value.strip() or value.strip() == "不适用":
                sourced_gaps.append(f"{path}.{key} 在已观察来源下不能空着或写成不适用")
        if adjustment == "不适用":
            sourced_gaps.append(f"{path}.adjustment 在已观察来源下不能写成不适用")
    return {
        "price": price,
        "kind": kind,
        "units": units,
        "adjustment": adjustment,
        "note": note,
        "meta": meta,
        "sourced_gaps": sourced_gaps,
    }


def probability_record(raw) -> dict | None:
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise InputError(["probability_up 必须是 null，或带 value 与 kind 的对象。不会把缺失概率当成 0"])
    if "value" not in raw:
        raise InputError(["probability_up.value 缺失"])
    value = as_decimal(raw.get("value"), "probability_up.value")
    if value < 0 or value > 1:
        raise InputError([f"probability_up.value 为 {money(value)}，不在 [0,1]。不截断，也不改写成边界值"])
    kind = raw.get("kind")
    if kind not in PROBABILITY_KINDS:
        raise InputError(["probability_up.kind 必须标明 user_assumption、hypothetical_stress、empirically_estimated 或 sourced_observation"])
    note = require_text(raw.get("note"), "probability_up.note")
    if kind == "sourced_observation":
        for key in ("source", "retrieved_at", "as_of"):
            text = raw.get(key)
            if not isinstance(text, str) or not text.strip() or text.strip() == "不适用":
                raise InputError([f"probability_up.{key} 在来源观察下不能空着"])
    return {"value": value, "kind": kind, "note": note, "is_measured_win_rate": False}


def breakeven(gain_up: Decimal, gain_down: Decimal) -> dict:
    spread = gain_up - gain_down
    if spread == 0:
        if gain_up == 0:
            status = "indifferent"
            note = "两边增量同为 0，门槛无定义。这不是胜率。"
        elif gain_up > 0:
            status = "always_positive"
            note = "两边增量相同且为正。任何概率下条件增量都为正。门槛无定义，不截断到 0 或 1。"
        else:
            status = "always_negative"
            note = "两边增量相同且为负。任何概率下条件增量都为负。门槛无定义。"
        return {
            "breakeven_probability": None,
            "breakeven_percent_display": None,
            "breakeven_status": status,
            "breakeven_is_probability_estimate": False,
            "ev_increases_with_p": None,
            "note": note,
        }
    threshold = -gain_down / spread
    if threshold < 0 or threshold > 1:
        status = "outside_unit_interval"
    elif threshold == 0 or threshold == 1:
        status = "boundary"
    else:
        status = "inside_unit_interval"
    if gain_up > 0 and gain_down > 0:
        note = "上涨和下跌两边的增量都为正。门槛若落在 [0,1] 之外，原样报告，不截断。这不能读成继续持有已经更划算。"
    elif gain_up < 0 and gain_down < 0:
        note = "两边增量都为负。门槛原样报告，不截断。这不是卖出指令。"
    elif gain_up <= gain_down:
        note = "上涨结果的增量并不高于下跌结果。p 变大不会使条件增量变好。门槛不是胜率。"
    else:
        note = "仅在两结果模型内，条件增量为零的 p 是这个门槛。它不是已测得的成功概率。"
    return {
        "breakeven_probability": money(threshold),
        "breakeven_percent_display": percent_1(threshold),
        "breakeven_status": status,
        "breakeven_is_probability_estimate": False,
        "ev_increases_with_p": gain_up > gain_down,
        "note": note,
    }


def cash_view(sale: dict[str, Decimal], financing: Decimal) -> dict[str, str]:
    net_after_financing = sale["net_cash"] - financing
    return {
        "quoted_price": money(sale["quoted_price"]),
        "fill_price": money(sale["fill_price"]),
        "quoted_amount": money(sale["quoted_amount"]),
        "slippage_amount": money(sale["slippage_amount"]),
        "gross_amount": money(sale["gross_amount"]),
        "commission": money(sale["commission"]),
        "tax": money(sale["tax"]),
        "financing_deducted": money(financing),
        "net_cash": money(net_after_financing),
    }


def evaluate(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise InputError(["情景必须是对象"])
    if raw.get("model", "two_outcome_first_hit") != "two_outcome_first_hit":
        raise InputError(["只实现 two_outcome_first_hit。不把别的模型悄悄换成两结果"])
    for key in ("neither_boundary_by_horizon", "both_hit_ordering"):
        if key in raw and raw[key] != "unresolved":
            raise InputError([f"{key} 只能是 unresolved。写别的值也不会使窗口内未触及或先后顺序变成已经解决"])

    label = require_text(raw.get("label"), "label")
    quantity = as_decimal(raw.get("quantity"), "quantity")
    if quantity != quantity.to_integral_value() or quantity <= 0:
        raise InputError(["quantity 必须是正整数股。0、负数和非整数都不换算成可交易数量"])
    if raw.get("quantity_unit") != "shares":
        raise InputError(["quantity_unit 必须是 shares。手不会在这里乘以 100"])

    now = price_record(raw.get("executable_now"), "executable_now")
    up = price_record(raw.get("up"), "up")
    down = price_record(raw.get("down"), "down")
    if up["price"] < down["price"]:
        raise InputError(["up.price 低于 down.price。顺序错误时不交换两边，也不计算门槛"])

    costs_raw = raw.get("costs")
    if not isinstance(costs_raw, dict) or costs_raw.get("mode") not in {"explicit", "zero_cost_teaching"}:
        raise InputError(["costs.mode 必须是 explicit 或 zero_cost_teaching"])
    teaching = costs_raw["mode"] == "zero_cost_teaching"
    sell_now_cost = load_cost_block(costs_raw.get("sell_now"), "costs.sell_now", teaching)
    sell_later_cost = load_cost_block(costs_raw.get("sell_later"), "costs.sell_later", teaching)
    if "incremental_financing_interest" not in costs_raw:
        raise InputError(["costs.incremental_financing_interest 缺失。缺失的融资利息不会被当成 0"])
    financing = as_decimal(costs_raw.get("incremental_financing_interest"), "costs.incremental_financing_interest")
    if financing < 0:
        raise InputError(["增量融资利息不能为负"])
    if teaching and financing != 0:
        raise InputError(["零成本教学模式下增量融资利息必须显式为 0"])

    probability = probability_record(raw.get("probability_up"))
    now_sale = sale_cash(now["price"], quantity, sell_now_cost)
    up_sale = sale_cash(up["price"], quantity, sell_later_cost)
    down_sale = sale_cash(down["price"], quantity, sell_later_cost)
    gain_up = up_sale["net_cash"] - financing - now_sale["net_cash"]
    gain_down = down_sale["net_cash"] - financing - now_sale["net_cash"]
    threshold = breakeven(gain_up, gain_down)

    explicit_zero = (
        not teaching
        and all(sell_now_cost[key] == 0 and sell_later_cost[key] == 0 for key in sell_now_cost)
        and financing == 0
    )

    gaps: list[str] = []
    for field in ("horizon", "hypothesis", "evidence_cutoff", "as_of", "plan_snapshot_id", "revision_id"):
        if not isinstance(raw.get(field), str) or not raw.get(field).strip():
            gaps.append(f"缺少 {field}")
    gaps.extend(now["sourced_gaps"])
    gaps.extend(up["sourced_gaps"])
    gaps.extend(down["sourced_gaps"])
    assumption_names = [
        name
        for name, item in (("现在卖出价", now), ("上涨情景", up), ("下跌情景", down))
        if item["kind"] != "sourced_observation"
    ]
    if assumption_names:
        gaps.append("、".join(assumption_names) + "不是已核对的观察")
    if teaching:
        gaps.append("显式零成本教学演算，不是观察到的费用为零")
    if explicit_zero:
        gaps.append("成本是显式零，但没有标明零成本教学")
    if probability is None:
        gaps.append("没有给出上涨概率，真实条件期望无法估计")
    else:
        gaps.append("所给上涨概率只供条件演算，不是已测得胜率")
    gaps.append("两结果模型没有包含窗口结束仍未触及任一边界")
    gaps.append("两边都可能碰到时的先后顺序未解决")

    constraints = raw.get("constraints")
    execution, execution_gaps = execution_label(constraints, quantity, now["kind"])
    gaps.extend(execution_gaps)

    evidence_ready = (
        not gaps_blocking_evidence(gaps)
        and now["kind"] == "sourced_observation"
        and up["kind"] == "sourced_observation"
        and down["kind"] == "sourced_observation"
        and not teaching
    )
    evidence = EVIDENCE_OK if evidence_ready else EVIDENCE_INCOMPLETE
    conditional = None
    if probability is not None:
        expected = probability["value"] * gain_up + (Decimal(1) - probability["value"]) * gain_down
        conditional = {
            "probability": money(probability["value"]),
            "probability_kind": probability["kind"],
            "probability_note": probability["note"],
            "is_measured_win_rate": False,
            "increment_per_share": money(expected / quantity),
            "increment_amount": money(expected),
        }

    statements = [
        "比较的是继续持有相对于现在卖出的增量净额，不是买入成本，也不是已经形成的账面价差。",
        "买入费用是沉没成本，不计入这次增量。现在卖和以后卖的佣金、最低佣金、税率、滑点各自扣一次，增量融资利息只从持有路径扣除。",
        "盈亏平衡门槛不是已测得的概率。把目标抬高或把退出放宽，改变的是假设，不是继续持有变得更划算的证明。",
        "两结果先触及模型是条件演算。窗口内没有碰到边界，或两边先后未解决时，真实分析是检查不完整。",
        "算术正负、证据是否够、结构是否支持、以及现在能否按所写价格卖出，是四件分开的事。正的条件增量不会变成继续持有的指令。",
        "本输出不评估结构。",
    ]
    if teaching:
        statements.insert(0, "这是显式的零成本教学演算，不是观察到的费用为零。")
    if explicit_zero:
        statements.insert(0, "各项成本写成了显式零，但没有标明零成本教学。不要把它读成已经核验的费率。")

    overall_parts = [OVERALL_INCOMPLETE, CANNOT_ESTIMATE]
    if execution == EXEC_BLOCKED:
        overall_parts.append(EXEC_BLOCKED)
    overall = "。".join(overall_parts)
    if EXEC_OK in overall:
        raise RuntimeError("overall must not copy an execution pass")

    sensitivity = sensitivity_rows(raw.get("sensitivity"), now, up, down, sell_now_cost, sell_later_cost, financing, quantity, probability)

    return {
        "label": label,
        "ok": True,
        "maps_to_hold_recommendation": False,
        "compare_basis": "incremental_net_versus_sell_now",
        "synthetic": bool(raw.get("synthetic", False)),
        "retrospective_teaching": bool(raw.get("retrospective_teaching", False)),
        "not_broker_verified": True,
        "not_a_universal_default": True,
        "zero_cost_teaching": teaching,
        "explicit_zero_costs_without_teaching_flag": explicit_zero,
        "model": {
            "name": "two_outcome_first_hit",
            "pedagogical": True,
            "neither_boundary_by_horizon": "unresolved",
            "both_hit_ordering": "unresolved",
            "real_analysis": OVERALL_INCOMPLETE,
        },
        "arithmetic": {
            "sell_now": cash_view(now_sale, Decimal(0)),
            "hold_up": cash_view(up_sale, financing),
            "hold_down": cash_view(down_sale, financing),
            "gross_price_increment_per_share": {
                "up": money(up["price"] - now["price"]),
                "down": money(down["price"] - now["price"]),
            },
            "net_increment_per_share": {
                "up": money(gain_up / quantity),
                "down": money(gain_down / quantity),
            },
            "net_increment_amount": {
                "up": money(gain_up),
                "down": money(gain_down),
            },
            "breakeven": threshold,
            "conditional_expected_increment": conditional,
        },
        "sensitivity": sensitivity,
        "evidence": evidence,
        "structure": STRUCTURE_NOT_ASSESSED,
        "execution": execution,
        "expectancy": CANNOT_ESTIMATE,
        "overall": overall,
        "gaps": gaps,
        "statements": statements,
    }


def gaps_blocking_evidence(gaps: list[str]) -> bool:
    markers = ("缺少 ", "不能空着", "不是已核对的观察", "零成本教学", "显式零")
    return any(any(marker in gap for marker in markers) for gap in gaps)


def execution_label(constraints, quantity: Decimal, now_kind: str) -> tuple[str, list[str]]:
    gaps = []
    if not isinstance(constraints, dict):
        return EXEC_INCOMPLETE, ["执行约束对象缺失，卖出可行性是检查不完整"]
    required = ("sellable_quantity", "lot_size", "board_limit_known", "t_plus_one_blocks_sell_now", "gap_or_limit_blocks_assumed_fill")
    if any(key not in constraints for key in required):
        return EXEC_INCOMPLETE, ["板块、手数或能否成交的约束没有写全，不默认可以卖出"]
    try:
        sellable = as_decimal(constraints.get("sellable_quantity"), "constraints.sellable_quantity")
        lot = as_decimal(constraints.get("lot_size"), "constraints.lot_size")
    except InputError as exc:
        return EXEC_INCOMPLETE, exc.errors
    board = constraints.get("board_limit_known")
    blocked_now = constraints.get("t_plus_one_blocks_sell_now")
    gap_block = constraints.get("gap_or_limit_blocks_assumed_fill")
    if not isinstance(board, bool) or not isinstance(blocked_now, bool) or not isinstance(gap_block, bool):
        return EXEC_INCOMPLETE, ["成交约束必须是 JSON 布尔值，不能用字符串代替"]
    reasons = []
    if blocked_now:
        reasons.append("T+1 使现在不能卖出")
    if gap_block:
        reasons.append("跳空或涨跌停使所写价格不能被假设成交")
    if sellable < quantity:
        reasons.append("可卖数量小于这次比较的股数")
    if lot <= 0 or quantity % lot != 0:
        reasons.append("股数不是最小申报单位的整数倍")
    if board is False:
        return EXEC_INCOMPLETE, ["板块涨跌幅限制没有写明，卖出可行性是检查不完整", *reasons]
    if now_kind != "sourced_observation":
        return EXEC_INCOMPLETE, ["现在卖出价格不是已核对观察，不能写成按现行规则可以执行", *reasons]
    if reasons:
        return EXEC_BLOCKED, reasons
    return EXEC_OK, []


def sensitivity_rows(raw, now, up, down, sell_now_cost, sell_later_cost, financing, quantity, probability) -> list[dict]:
    if raw is None:
        return []
    if not isinstance(raw, dict):
        raise InputError(["sensitivity 必须是对象"])
    rows = []
    for value in raw.get("hypothetical_probabilities", []):
        try:
            probability_value = as_decimal(value, "sensitivity.hypothetical_probabilities")
        except InputError as exc:
            rows.append({"kind": "hypothetical_probability", "changed": str(value), "error": exc.errors[0]})
            continue
        if probability_value < 0 or probability_value > 1:
            rows.append({
                "kind": "hypothetical_probability",
                "changed": money(probability_value),
                "error": "敏感性概率不在 [0,1]，不截断",
            })
            continue
        gain_up, gain_down = up_gain(now, up, down, sell_now_cost, sell_later_cost, financing, quantity)
        expected = probability_value * gain_up + (Decimal(1) - probability_value) * gain_down
        rows.append({
            "kind": "hypothetical_probability",
            "changed": money(probability_value),
            "conditional_expected_increment_amount": money(expected),
            "is_measured_win_rate": False,
            "note": "这是假设的 p，不是补上的真实胜率。",
        })
    for value in raw.get("alternate_up_prices", []):
        rows.append(perturbed_row("alternate_up_price", value, now, up, down, sell_now_cost, sell_later_cost, financing, quantity, probability, "up"))
    for value in raw.get("alternate_later_slippage_per_share", []):
        rows.append(perturbed_row("alternate_later_slippage", value, now, up, down, sell_now_cost, sell_later_cost, financing, quantity, probability, "slip"))
    if rows:
        rows.append({
            "kind": "interpretation",
            "note": "敏感性只改假设。门槛变低不是继续持有变得更划算的证明。",
        })
    return rows


def up_gain(now, up, down, sell_now_cost, sell_later_cost, financing, quantity):
    now_sale = sale_cash(now["price"], quantity, sell_now_cost)
    up_sale = sale_cash(up["price"], quantity, sell_later_cost)
    down_sale = sale_cash(down["price"], quantity, sell_later_cost)
    return (
        up_sale["net_cash"] - financing - now_sale["net_cash"],
        down_sale["net_cash"] - financing - now_sale["net_cash"],
    )


def perturbed_row(kind, value, now, up, down, sell_now_cost, sell_later_cost, financing, quantity, probability, mode):
    try:
        number = as_decimal(value, kind)
    except InputError as exc:
        return {"kind": kind, "changed": str(value), "error": exc.errors[0]}
    up_price = up["price"]
    later_cost = dict(sell_later_cost)
    if mode == "up":
        up_price = number
        if up_price <= down["price"]:
            return {"kind": kind, "changed": money(number), "error": "替代上涨价没有高于下跌价，这一行不计算"}
    else:
        if number < 0:
            return {"kind": kind, "changed": money(number), "error": "替代滑点不能为负"}
        later_cost["slippage_per_share"] = number
    try:
        now_sale = sale_cash(now["price"], quantity, sell_now_cost)
        up_sale = sale_cash(up_price, quantity, later_cost)
        down_sale = sale_cash(down["price"], quantity, later_cost)
    except InputError as exc:
        return {"kind": kind, "changed": money(number), "error": exc.errors[0]}
    gain_up = up_sale["net_cash"] - financing - now_sale["net_cash"]
    gain_down = down_sale["net_cash"] - financing - now_sale["net_cash"]
    threshold = breakeven(gain_up, gain_down)
    row = {
        "kind": kind,
        "changed": money(number),
        "net_increment_amount": {"up": money(gain_up), "down": money(gain_down)},
        "breakeven_probability": threshold["breakeven_probability"],
        "breakeven_status": threshold["breakeven_status"],
        "breakeven_is_probability_estimate": False,
        "note": "替代价格或费用改变的是假设。",
    }
    if probability is not None:
        expected = probability["value"] * gain_up + (Decimal(1) - probability["value"]) * gain_down
        row["conditional_expected_increment_amount"] = money(expected)
        row["conditional_probability_is_measured_win_rate"] = False
    return row


def scenarios_from(document) -> list[dict]:
    if isinstance(document, dict) and isinstance(document.get("scenarios"), list):
        return document["scenarios"]
    if isinstance(document, dict):
        return [document]
    raise InputError(["文件必须是一个情景对象，或带 scenarios 数组的对象"])


def run_document(document) -> dict:
    results = []
    errors = []
    for index, scenario in enumerate(scenarios_from(document), start=1):
        try:
            results.append(evaluate(scenario))
        except InputError as exc:
            errors.append({"index": index, "errors": exc.errors, "maps_to_hold_recommendation": False})
    return {"ok": not errors, "results": results, "errors": errors, "validates_trading_performance": False}


def text_summary(payload: dict) -> str:
    lines = ["持有与现在卖出的情景比较。通过这些数字并不表示交易方法有效。"]
    for item in payload["results"]:
        arithmetic = item["arithmetic"]
        lines.append(f"[{item['label']}] 证据：{item['evidence']}；结构：{item['structure']}；执行：{item['execution']}")
        lines.append(f"总结论：{item['overall']}")
        lines.append(
            "增量净额（金额）上涨 "
            + arithmetic["net_increment_amount"]["up"]
            + "，下跌 "
            + arithmetic["net_increment_amount"]["down"]
        )
        breakeven_value = arithmetic["breakeven"]["breakeven_probability"]
        if breakeven_value is None:
            lines.append("盈亏平衡门槛无定义：" + arithmetic["breakeven"]["note"])
        else:
            lines.append(
                "两结果门槛 p*="
                + breakeven_value
                + "（展示用百分数 "
                + arithmetic["breakeven"]["breakeven_percent_display"]
                + "%）。"
                + arithmetic["breakeven"]["note"]
            )
        conditional = arithmetic["conditional_expected_increment"]
        if conditional is None:
            lines.append("真实条件期望：无法估计。")
        else:
            lines.append(
                "条件增量金额 "
                + conditional["increment_amount"]
                + "，所用概率类别 "
                + conditional["probability_kind"]
                + "。这不是已测得胜率。"
            )
        lines.append("不会映射为继续持有指令。")
    for error in payload["errors"]:
        lines.append(f"第 {error['index']} 个情景拒绝计算：" + "；".join(error["errors"]))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="持有与现在卖出的条件增量比较。不是下单程序。")
    parser.add_argument("paths", nargs="+", help="情景 JSON 文件")
    parser.add_argument("--text", action="store_true", help="先打印中文摘要，再打印 JSON")
    parser.add_argument("--json-only", action="store_true", help="只打印 JSON")
    args = parser.parse_args(argv)
    exit_code = 0
    combined_results = []
    combined_errors = []
    for path_text in args.paths:
        path = Path(path_text)
        try:
            payload = run_document(parse_document(path.read_text(encoding="utf-8")))
        except InputError as exc:
            payload = {"ok": False, "results": [], "errors": [{"index": 0, "errors": exc.errors, "maps_to_hold_recommendation": False}], "validates_trading_performance": False}
        except OSError as exc:
            payload = {"ok": False, "results": [], "errors": [{"index": 0, "errors": [str(exc)], "maps_to_hold_recommendation": False}], "validates_trading_performance": False}
        if not payload["ok"]:
            exit_code = 2
        combined_results.extend(payload["results"])
        combined_errors.extend(payload["errors"])
    payload = {
        "ok": exit_code == 0,
        "results": combined_results,
        "errors": combined_errors,
        "validates_trading_performance": False,
    }
    if args.text and not args.json_only:
        print(text_summary(payload))
        print("--- json ---")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
