#!/usr/bin/env python3
"""Arithmetic and contract tests for hold-versus-sell comparison.

Passing does not validate trading performance.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import hold_sell


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "docs" / "examples" / "hold-sell"


def price(value, kind="hypothetical_stress", note="合成假设，不是行情"):
    return {
        "price": value,
        "kind": kind,
        "note": note,
        "source": "不适用" if kind != "sourced_observation" else "https://example.invalid/synthetic/quote",
        "retrieved_at": "不适用" if kind != "sourced_observation" else "合成日 D 15:00 Asia/Shanghai",
        "as_of": "不适用" if kind != "sourced_observation" else "合成日 D 15:00 Asia/Shanghai",
        "session": "不适用" if kind != "sourced_observation" else "常规收盘",
        "units": "元/股",
        "adjustment": "不适用" if kind != "sourced_observation" else "不复权",
    }


def costs(mode="zero_cost_teaching", now=None, later=None, financing="0"):
    zero = {
        "commission_rate": "0",
        "commission_minimum": "0",
        "tax_rate": "0",
        "slippage_per_share": "0",
    }
    return {
        "mode": mode,
        "sell_now": now or zero,
        "sell_later": later or zero,
        "incremental_financing_interest": financing,
    }


def scenario(**overrides):
    base = {
        "label": "synthetic",
        "synthetic": True,
        "model": "two_outcome_first_hit",
        "neither_boundary_by_horizon": "unresolved",
        "both_hit_ordering": "unresolved",
        "record_id": "SYN-HS",
        "symbol": "SYN001",
        "horizon": "合成日 D 至 D+3",
        "hypothesis": "只比较现在卖出和两结果持有的增量净额",
        "evidence_cutoff": "合成日 D 15:00 Asia/Shanghai",
        "as_of": "合成日 D 15:00 Asia/Shanghai",
        "plan_snapshot_id": "v1",
        "revision_id": "append-1",
        "quantity": "100",
        "quantity_unit": "shares",
        "executable_now": price("10"),
        "up": price("12"),
        "down": price("8"),
        "probability_up": None,
        "costs": costs(),
        "constraints": {
            "sellable_quantity": "100",
            "lot_size": "100",
            "board_limit_known": True,
            "t_plus_one_blocks_sell_now": False,
            "gap_or_limit_blocks_assumed_fill": False,
        },
    }
    base.update(overrides)
    return base


def run_cli(*paths: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "hold_sell.py"), "--json-only", *[str(path) for path in paths]],
        check=False,
        capture_output=True,
        text=True,
    )


class ArithmeticTests(unittest.TestCase):
    def test_zero_cost_teaching_matches_gross_spread_and_omitted_probability(self) -> None:
        result = hold_sell.evaluate(scenario())
        self.assertTrue(result["zero_cost_teaching"])
        self.assertEqual(result["arithmetic"]["net_increment_amount"]["up"], "200")
        self.assertEqual(result["arithmetic"]["net_increment_amount"]["down"], "-200")
        self.assertEqual(result["arithmetic"]["gross_price_increment_per_share"]["up"], "2")
        self.assertEqual(result["arithmetic"]["net_increment_per_share"]["up"], "2")
        self.assertEqual(result["arithmetic"]["breakeven"]["breakeven_probability"], "0.5")
        self.assertEqual(result["arithmetic"]["breakeven"]["breakeven_percent_display"], "50.0")
        self.assertIsNone(result["arithmetic"]["conditional_expected_increment"])
        self.assertEqual(result["expectancy"], "无法估计")
        self.assertIn("检查不完整", result["overall"])
        self.assertNotIn("按现行规则可以执行所写计划", result["overall"])
        self.assertFalse(result["maps_to_hold_recommendation"])
        self.assertEqual(result["structure"], "本次未评估结构")
        self.assertEqual(result["model"]["neither_boundary_by_horizon"], "unresolved")
        self.assertFalse(result["arithmetic"]["breakeven"]["breakeven_is_probability_estimate"])

    def test_explicit_costs_do_not_double_count_or_use_buy_fees(self) -> None:
        rate = Decimal("0.0003")
        minimum = Decimal("5")
        tax_rate = Decimal("0.0005")
        financing = Decimal("1.25")
        quantity = Decimal(100)

        def net(price, slip):
            fill = price - slip
            gross = fill * quantity
            commission = max(rate * gross, minimum)
            tax = tax_rate * gross
            return gross - commission - tax

        now_net = net(Decimal("10"), Decimal("0.01"))
        up_net = net(Decimal("11"), Decimal("0.02")) - financing
        down_net = net(Decimal("9"), Decimal("0.02")) - financing
        gain_up = up_net - now_net
        gain_down = down_net - now_net
        self.assertEqual(gain_up, Decimal("97.7005"))
        self.assertEqual(gain_down, Decimal("-102.1995"))
        block = {
            "commission_rate": "0.0003",
            "commission_minimum": "5",
            "tax_rate": "0.0005",
            "slippage_per_share": "0.01",
        }
        later = dict(block, slippage_per_share="0.02")
        result = hold_sell.evaluate(
            scenario(
                costs=costs("explicit", block, later, "1.25"),
                executable_now=price("10"),
                up=price("11"),
                down=price("9"),
            )
        )
        self.assertEqual(result["arithmetic"]["net_increment_amount"]["up"], "97.7005")
        self.assertEqual(result["arithmetic"]["net_increment_amount"]["down"], "-102.1995")
        self.assertNotEqual(result["arithmetic"]["net_increment_per_share"]["up"], "1")
        threshold = Decimal(result["arithmetic"]["breakeven"]["breakeven_probability"])
        self.assertEqual(threshold, -gain_down / (gain_up - gain_down))
        self.assertEqual(result["arithmetic"]["sell_now"]["commission"], "5")
        self.assertEqual(result["arithmetic"]["hold_up"]["financing_deducted"], "1.25")
        self.assertEqual(result["arithmetic"]["sell_now"]["financing_deducted"], "0")

    def test_commission_uses_rate_once_when_above_minimum(self) -> None:
        sale = hold_sell.sale_cash(
            Decimal("10"),
            Decimal(10000),
            {
                "commission_rate": Decimal("0.0003"),
                "commission_minimum": Decimal("5"),
                "tax_rate": Decimal("0"),
                "slippage_per_share": Decimal("0"),
            },
        )
        self.assertEqual(sale["commission"], Decimal("30"))
        self.assertEqual(sale["net_cash"], Decimal("99970"))

    def test_positive_and_negative_conditional_expectation_is_not_a_decision(self) -> None:
        positive = hold_sell.evaluate(
            scenario(probability_up={"value": "0.8", "kind": "hypothetical_stress", "note": "合成假设概率"})
        )
        negative = hold_sell.evaluate(
            scenario(probability_up={"value": "0.2", "kind": "hypothetical_stress", "note": "合成假设概率"})
        )
        self.assertEqual(positive["arithmetic"]["conditional_expected_increment"]["increment_amount"], "120")
        self.assertEqual(negative["arithmetic"]["conditional_expected_increment"]["increment_amount"], "-120")
        for result in (positive, negative):
            self.assertFalse(result["maps_to_hold_recommendation"])
            self.assertFalse(result["arithmetic"]["conditional_expected_increment"]["is_measured_win_rate"])
            self.assertEqual(result["expectancy"], "无法估计")
            self.assertIn("检查不完整", result["overall"])
            self.assertEqual(result["evidence"], "检查不完整")

    def test_threshold_outside_unit_interval_is_not_clipped(self) -> None:
        always_up = hold_sell.evaluate(scenario(up=price("12"), down=price("11")))
        always_down = hold_sell.evaluate(scenario(executable_now=price("10"), up=price("9"), down=price("8")))
        self.assertEqual(always_up["arithmetic"]["breakeven"]["breakeven_probability"], "-1")
        self.assertEqual(always_up["arithmetic"]["breakeven"]["breakeven_status"], "outside_unit_interval")
        self.assertEqual(always_down["arithmetic"]["breakeven"]["breakeven_probability"], "2")
        self.assertEqual(always_down["arithmetic"]["breakeven"]["breakeven_status"], "outside_unit_interval")
        self.assertNotIn(always_up["arithmetic"]["breakeven"]["breakeven_probability"], {"0", "1"})

    def test_equal_outcomes_have_no_threshold(self) -> None:
        flat = hold_sell.evaluate(scenario(executable_now=price("10"), up=price("10.5"), down=price("10.5")))
        same = hold_sell.evaluate(scenario(executable_now=price("10"), up=price("10"), down=price("10")))
        lower = hold_sell.evaluate(scenario(executable_now=price("10"), up=price("9"), down=price("9")))
        self.assertEqual(flat["arithmetic"]["breakeven"]["breakeven_status"], "always_positive")
        self.assertIsNone(flat["arithmetic"]["breakeven"]["breakeven_probability"])
        self.assertEqual(same["arithmetic"]["breakeven"]["breakeven_status"], "indifferent")
        self.assertEqual(lower["arithmetic"]["breakeven"]["breakeven_status"], "always_negative")

    def test_worse_labeled_upside_does_not_read_as_a_win_rate(self) -> None:
        threshold = hold_sell.breakeven(Decimal("-1"), Decimal("2"))
        self.assertFalse(threshold["ev_increases_with_p"])
        self.assertIn("不会使条件增量变好", threshold["note"])
        self.assertEqual(threshold["breakeven_is_probability_estimate"], False)

    def test_missing_cost_is_not_zero(self) -> None:
        raw = scenario()
        del raw["costs"]["sell_now"]["tax_rate"]
        with self.assertRaises(hold_sell.InputError) as caught:
            hold_sell.evaluate(raw)
        self.assertIn("不会被当成 0", caught.exception.errors[0])

    def test_explicit_zero_without_teaching_flag_is_marked(self) -> None:
        result = hold_sell.evaluate(scenario(costs=costs("explicit")))
        self.assertTrue(result["explicit_zero_costs_without_teaching_flag"])
        self.assertFalse(result["zero_cost_teaching"])
        self.assertEqual(result["evidence"], "检查不完整")

    def test_invalid_numbers_and_ordering_are_rejected(self) -> None:
        rejects = [
            scenario(probability_up={"value": "1.2", "kind": "hypothetical_stress", "note": "越界"}),
            scenario(probability_up={"value": "-0.01", "kind": "hypothetical_stress", "note": "越界"}),
            scenario(probability_up={"value": "NaN", "kind": "hypothetical_stress", "note": "非数"}),
            scenario(probability_up={"value": "Infinity", "kind": "hypothetical_stress", "note": "无穷"}),
            scenario(quantity="0"),
            scenario(quantity="-100"),
            scenario(quantity="100.5"),
            scenario(up=price("8"), down=price("9")),
            scenario(executable_now=price("0")),
            scenario(costs=costs("explicit", {"commission_rate": "-0.1", "commission_minimum": "0", "tax_rate": "0", "slippage_per_share": "0"})),
        ]
        for raw in rejects:
            with self.assertRaises(hold_sell.InputError):
                hold_sell.evaluate(raw)

    def test_non_executable_sell_stays_conditional(self) -> None:
        raw = scenario(
            executable_now=price("10", "sourced_observation", "合成已观察价格"),
            constraints={
                "sellable_quantity": "100",
                "lot_size": "100",
                "board_limit_known": True,
                "t_plus_one_blocks_sell_now": True,
                "gap_or_limit_blocks_assumed_fill": False,
            },
        )
        result = hold_sell.evaluate(raw)
        self.assertEqual(result["execution"], "计划按现行规则不可执行")
        self.assertIn("计划按现行规则不可执行", result["overall"])
        self.assertNotIn("按现行规则可以执行所写计划", result["overall"])
        self.assertEqual(result["arithmetic"]["net_increment_amount"]["up"], "200")
        self.assertFalse(result["maps_to_hold_recommendation"])

    def test_odd_lot_and_unknown_board_do_not_pass_execution(self) -> None:
        odd = hold_sell.evaluate(
            scenario(
                quantity="50",
                executable_now=price("10", "sourced_observation", "合成已观察价格"),
                constraints={
                    "sellable_quantity": "50",
                    "lot_size": "100",
                    "board_limit_known": True,
                    "t_plus_one_blocks_sell_now": False,
                    "gap_or_limit_blocks_assumed_fill": False,
                },
            )
        )
        unknown_board = hold_sell.evaluate(
            scenario(
                constraints={
                    "sellable_quantity": "100",
                    "lot_size": "100",
                    "board_limit_known": False,
                    "t_plus_one_blocks_sell_now": False,
                    "gap_or_limit_blocks_assumed_fill": False,
                }
            )
        )
        self.assertEqual(odd["execution"], "计划按现行规则不可执行")
        self.assertEqual(unknown_board["execution"], "检查不完整")

    def test_sourced_sell_now_can_pass_execution_without_a_hold_decision(self) -> None:
        result = hold_sell.evaluate(scenario(executable_now=price("10", "sourced_observation", "合成已观察价格")))
        self.assertEqual(result["execution"], "按现行规则可以执行所写计划")
        self.assertEqual(result["evidence"], "检查不完整")
        self.assertNotIn("按现行规则可以执行所写计划", result["overall"])
        self.assertEqual(result["structure"], "本次未评估结构")

    def test_fully_sourced_prices_still_cannot_estimate_real_expectancy(self) -> None:
        block = {
            "commission_rate": "0.0001",
            "commission_minimum": "0",
            "tax_rate": "0.0001",
            "slippage_per_share": "0",
        }
        result = hold_sell.evaluate(
            scenario(
                executable_now=price("10", "sourced_observation", "合成观察"),
                up=price("12", "sourced_observation", "合成历史高点"),
                down=price("8", "sourced_observation", "合成历史低点"),
                costs=costs("explicit", block, block, "0"),
            )
        )
        self.assertEqual(result["evidence"], "数据足够、仍新且口径一致")
        self.assertEqual(result["expectancy"], "无法估计")
        self.assertIn("检查不完整", result["overall"])
        self.assertIn("无法估计", result["overall"])
        self.assertFalse(result["maps_to_hold_recommendation"])

    def test_missing_horizon_is_incomplete_but_arithmetic_remains_conditional(self) -> None:
        raw = scenario()
        raw["horizon"] = ""
        result = hold_sell.evaluate(raw)
        self.assertEqual(result["evidence"], "检查不完整")
        self.assertIn("缺少 horizon", result["gaps"])
        self.assertEqual(result["arithmetic"]["breakeven"]["breakeven_probability"], "0.5")

    def test_sensitivity_changes_threshold_when_target_or_cost_changes(self) -> None:
        result = hold_sell.evaluate(
            scenario(
                sensitivity={
                    "hypothetical_probabilities": ["0.25", "1.5"],
                    "alternate_up_prices": ["14", "8"],
                    "alternate_later_slippage_per_share": ["0.5"],
                }
            )
        )
        rows = result["sensitivity"]
        probability_row = rows[0]
        rejected_probability = rows[1]
        higher_target = rows[2]
        bad_target = rows[3]
        higher_slip = rows[4]
        self.assertEqual(probability_row["conditional_expected_increment_amount"], "-100")
        self.assertIn("不截断", rejected_probability["error"])
        self.assertEqual(Decimal(higher_target["breakeven_probability"]), Decimal(200) / Decimal(600))
        self.assertIn("error", bad_target)
        self.assertNotEqual(higher_slip["net_increment_amount"]["up"], "200")
        self.assertLess(Decimal(higher_slip["net_increment_amount"]["up"]), Decimal("200"))
        self.assertFalse(higher_target["breakeven_is_probability_estimate"])

    def test_historical_teaching_thresholds_round_half_up(self) -> None:
        expected = {"544": "29.1", "541": "46.8", "537": "60.1"}
        for down, percent in expected.items():
            gain_up = Decimal("553") - Decimal("546.62")
            gain_down = Decimal(down) - Decimal("546.62")
            threshold = -gain_down / (gain_up - gain_down)
            shown = (threshold * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            self.assertEqual(format(shown, "f"), percent)

    def test_historical_file_uses_discussion_price_not_later_sale(self) -> None:
        payload = hold_sell.run_document(hold_sell.parse_document((EXAMPLES / "zhongji-2026-11-12-teaching.json").read_text(encoding="utf-8")))
        self.assertTrue(payload["ok"])
        self.assertFalse(payload["validates_trading_performance"])
        by_label = {item["label"]: item for item in payload["results"]}
        self.assertEqual(by_label["zhongji-teaching-D544"]["arithmetic"]["breakeven"]["breakeven_percent_display"], "29.1")
        self.assertEqual(by_label["zhongji-teaching-D541"]["arithmetic"]["breakeven"]["breakeven_percent_display"], "46.8")
        self.assertEqual(by_label["zhongji-teaching-D537"]["arithmetic"]["breakeven"]["breakeven_percent_display"], "60.1")
        text = (EXAMPLES / "zhongji-2026-11-12-teaching.json").read_text(encoding="utf-8")
        self.assertNotIn('"price": "547.50"', text)
        self.assertNotIn('"price": "547.5"', text)
        for item in payload["results"]:
            self.assertTrue(item["retrospective_teaching"])
            self.assertTrue(item["zero_cost_teaching"])
            self.assertEqual(item["arithmetic"]["sell_now"]["quoted_price"], "546.62")
            self.assertEqual(item["arithmetic"]["net_increment_amount"]["up"], "638")
            self.assertIsNone(item["arithmetic"]["conditional_expected_increment"])
            self.assertFalse(item["maps_to_hold_recommendation"])
            self.assertEqual(item["structure"], "本次未评估结构")


class CommandTests(unittest.TestCase):
    def test_examples_run(self) -> None:
        paths = [
            EXAMPLES / "synthetic-unknown.json",
            EXAMPLES / "synthetic-positive.json",
            EXAMPLES / "synthetic-negative.json",
            EXAMPLES / "synthetic-costs-sensitivity.json",
        ]
        completed = run_cli(*paths)
        self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(len(payload["results"]), 4)
        self.assertFalse(any(item["maps_to_hold_recommendation"] for item in payload["results"]))

    def test_invalid_examples_fail(self) -> None:
        for name in ("invalid-probability.json", "invalid-nan.json", "invalid-quantity.json"):
            completed = run_cli(EXAMPLES / name)
            self.assertEqual(completed.returncode, 2, name + completed.stdout)
            payload = json.loads(completed.stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["results"], [])
            self.assertFalse(payload["validates_trading_performance"])


if __name__ == "__main__":
    unittest.main()
