#!/usr/bin/env python3
"""Check in-repo documentation structure.

A passing run means links, fields, fixture labels, and the decimal
examples already written in the repo are consistent. It does not mean
the liquidity-repair notes are a validated trading method.

Usage, from a complete clone:

    python3 scripts/check_docs.py
"""

from __future__ import annotations

import re
import sys
import tempfile
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


PASS_OVERALL = {
    "结构尚可，可继续观察",
    "按现行规则可以执行所写计划",
}
ALLOWED_DATA = {"数据足够、仍新且口径一致", "检查不完整"}
ALLOWED_STRUCTURE = {
    "结构尚可，可继续观察",
    "结构转弱",
    "结构破坏",
    "本次未评估结构",
    "尚不可上移保护参考",
}
ALLOWED_EXECUTION = {
    "按现行规则可以执行所写计划",
    "计划按现行规则不可执行",
    "检查不完整",
}
SHARED_FIELDS = (
    "记录编号",
    "持有窗口",
    "价格假设",
    "证据截止",
    "当前可卖数量",
    "保护参考",
    "未关闭缺口",
    "规则版本",
)
EVIDENCE_FIELDS = (
    "来源 URL",
    "检索时间",
    "数据 as-of",
    "会话",
    "单位",
    "复权",
    "摘录",
    "规则版本",
)
PLAN_FIELDS = (
    "适用板块",
    "交易规则来源",
    "当前可卖数量",
    "申报约束",
    "费用口径",
    "融资利息口径",
)
README_ANCHORS = [
    "purpose",
    "naming",
    "status",
    "quick-start",
    "workflows",
    "data",
    "limitations",
    "docs",
    "public",
    "license",
]
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```")
PRIVACY_RES = (
    re.compile(r"总资金[^\n]{0,16}[0-9]"),
    re.compile(r"总市值[^\n]{0,16}[0-9]"),
    re.compile(r"总持仓[^\n]{0,16}[0-9]"),
    re.compile(r"占总(资金|持仓|仓位|组合)[^\n]{0,16}[0-9]"),
    re.compile(r"(总仓位|仓位占比|组合占比)\s*[:：]?\s*[0-9]"),
    re.compile(r"(资金账号|账户号|客户号|证券账号)[^\n]{0,8}[0-9]{4,}"),
)


def parse_scalar(raw: str):
    s = raw.strip()
    if s in ("", "~", "null", "Null", "NULL"):
        return None
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    if s == "[]":
        return []
    if s == "{}":
        return {}
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
        inner = s[1:-1]
        if s[0] == '"':
            inner = (
                inner.replace('\\"', '"')
                .replace("\\n", "\n")
                .replace("\\\\", "\\")
            )
        else:
            inner = inner.replace("''", "'")
        return inner
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _split_key(text: str) -> tuple[str, str | None]:
    if text.startswith(("'", '"')):
        raise ValueError(f"quoted key is not used here: {text}")
    colon = text.find(":")
    if colon < 0:
        raise ValueError(f"expected key: value, got {text}")
    key = text[:colon].strip()
    value = text[colon + 1 :]
    if value == "":
        return key, None
    if value[0] not in " \t":
        # A colon inside a plain scalar, not a key separator.
        raise ValueError(f"colon is not a key separator: {text}")
    return key, value.strip()


class YamlParser:
    def __init__(self, text: str) -> None:
        self.lines: list[tuple[int, str]] = []
        for raw in text.splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if raw.startswith("\t") or "\t" in raw[: len(raw) - len(raw.lstrip(" "))]:
                raise ValueError("tabs are not accepted in YAML indentation")
            indent = len(raw) - len(raw.lstrip(" "))
            self.lines.append((indent, raw.strip()))
        self.i = 0

    def peek(self) -> tuple[int, str] | None:
        if self.i >= len(self.lines):
            return None
        return self.lines[self.i]

    def parse(self):
        if self.peek() is None:
            return None
        value = self.parse_node(self.peek()[0])
        if self.peek() is not None:
            raise ValueError(f"unparsed YAML near {self.peek()[1]}")
        return value

    def parse_node(self, indent: int):
        current = self.peek()
        if current is None:
            raise ValueError("expected a YAML node")
        if current[1].startswith("- "):
            return self.parse_list(indent)
        return self.parse_map(indent)

    def parse_map(self, indent: int) -> dict:
        mapping: dict = {}
        while self.peek() and self.peek()[0] == indent and not self.peek()[1].startswith("- "):
            _, text = self.lines[self.i]
            self.i += 1
            key, raw_value = _split_key(text)
            if raw_value is None:
                nxt = self.peek()
                if nxt and nxt[0] > indent:
                    mapping[key] = self.parse_node(nxt[0])
                else:
                    mapping[key] = None
            else:
                mapping[key] = parse_scalar(raw_value)
        return mapping

    def parse_list(self, indent: int) -> list:
        items = []
        while self.peek() and self.peek()[0] == indent and self.peek()[1].startswith("- "):
            _, text = self.lines[self.i]
            rest = text[2:]
            self.i += 1
            if rest == "":
                nxt = self.peek()
                if nxt is None or nxt[0] <= indent:
                    items.append(None)
                else:
                    items.append(self.parse_node(nxt[0]))
                continue
            try:
                key, raw_value = _split_key(rest)
                keyed = True
            except ValueError:
                key, raw_value, keyed = "", None, False
            if not keyed:
                items.append(parse_scalar(rest))
                continue
            mapping: dict = {}
            if raw_value is None:
                nxt = self.peek()
                if nxt and nxt[0] > indent:
                    mapping[key] = self.parse_node(nxt[0])
                else:
                    mapping[key] = None
            else:
                mapping[key] = parse_scalar(raw_value)
            child_indent = None
            while self.peek():
                cind, ctext = self.peek()
                if cind <= indent:
                    break
                if ctext.startswith("- ") and (child_indent is None or cind == indent + 2):
                    # A nested list belongs to the previous key only when that
                    # key had no inline value. Continuation keys are handled below.
                    break
                if child_indent is None:
                    child_indent = cind
                if cind != child_indent:
                    break
                self.i += 1
                ck, cv = _split_key(ctext)
                if cv is None:
                    nxt = self.peek()
                    if nxt and nxt[0] > cind:
                        mapping[ck] = self.parse_node(nxt[0])
                    else:
                        mapping[ck] = None
                else:
                    mapping[ck] = parse_scalar(cv)
            items.append(mapping)
        return items


def load_yaml(text: str):
    return YamlParser(text).parse()


def frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
    data = load_yaml(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, text[end + 4 :]


def visible_markdown(text: str) -> str:
    out = []
    fenced = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return "\n".join(out)


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part == ".git" or part == "__pycache__" for part in path.parts):
            continue
        yield path


def check_links(root: Path) -> list[str]:
    problems = []
    count = 0
    for path in iter_files(root):
        if path.suffix.lower() not in {".md", ".txt"} and path.name != "llms.txt":
            continue
        body = visible_markdown(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(body):
            target = match.group(2).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (path.parent / path_part).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                problems.append(f"link leaves the repo: {path.relative_to(root)} -> {target}")
                continue
            if not resolved.exists():
                problems.append(f"broken link: {path.relative_to(root)} -> {target}")
            else:
                count += 1
    if count == 0 and (root / "README.md").exists():
        problems.append("no relative links were found")
    return problems


def check_yaml_and_skills(root: Path) -> list[str]:
    problems = []
    for path in iter_files(root):
        if path.suffix.lower() in {".yaml", ".yml"}:
            try:
                data = load_yaml(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001 - report parser failures as check errors
                problems.append(f"YAML did not parse: {path.relative_to(root)}: {exc}")
                continue
            if not isinstance(data, dict):
                problems.append(f"YAML root is not a mapping: {path.relative_to(root)}")
                continue
            skill_name = data.get("skill")
            if isinstance(skill_name, str):
                parents = {part for part in path.parts}
                if skill_name not in parents:
                    problems.append(
                        f"example skill field {skill_name!r} is not the directory of {path.relative_to(root)}"
                    )
        if path.name != "SKILL.md":
            continue
        try:
            data, _body = frontmatter(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"skill frontmatter did not parse: {path.relative_to(root)}: {exc}")
            continue
        if data is None:
            problems.append(f"skill has no frontmatter: {path.relative_to(root)}")
            continue
        name = data.get("name")
        if name != path.parent.name:
            problems.append(
                f"skill name {name!r} does not match directory {path.parent.name}"
            )
        linked_docs = False
        body = visible_markdown(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(body):
            target = match.group(2).strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                rel = resolved.relative_to(root.resolve())
            except ValueError:
                continue
            if rel.parts and rel.parts[0] == "docs":
                linked_docs = True
        if not linked_docs:
            problems.append(f"skill does not link into docs/: {path.relative_to(root)}")
    return problems


def last_labeled(body: str, label: str) -> str | None:
    found = None
    prefix = label
    for line in body.splitlines():
        text = line.strip()
        if text.startswith("- "):
            text = text[2:].strip()
        if text.startswith(prefix):
            found = text.split("：", 1)[1].strip()
    return found


def check_fixtures(root: Path) -> list[str]:
    problems = []
    folder = root / "docs" / "examples" / "synthetic"
    if not folder.is_dir():
        return ["missing docs/examples/synthetic"]
    files = sorted(path for path in folder.glob("*.md") if path.name != "README.md")
    if len(files) < 6:
        problems.append(f"expected at least 6 synthetic fixtures, found {len(files)}")
    for path in files:
        text = path.read_text(encoding="utf-8")
        try:
            data, body = frontmatter(text)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"fixture frontmatter did not parse: {path.name}: {exc}")
            continue
        if data is None:
            problems.append(f"fixture has no frontmatter: {path.name}")
            continue
        problems.extend(fixture_problems(path.name, data, body))
    acceptance = root / "skills" / "pre-open-overnight-risk-check" / "examples" / "acceptance"
    if acceptance.is_dir():
        for path in sorted(acceptance.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            try:
                data, _body = frontmatter(text)
            except Exception as exc:  # noqa: BLE001
                problems.append(f"acceptance frontmatter did not parse: {path.name}: {exc}")
                continue
            if data is None:
                continue
            if data.get("synthetic") is not True or data.get("real_quotes") is not False or data.get("real_news") is not False:
                problems.append(f"acceptance markers are wrong: {path.name}")
    return problems


def fixture_problems(name: str, data: dict, body: str) -> list[str]:
    problems = []
    for key in (
        "synthetic",
        "real_quotes",
        "real_news",
        "frozen_as_of",
        "rule_version",
        "expects_data",
        "expects_structure",
        "expects_execution",
        "expects_overall",
    ):
        if key not in data:
            problems.append(f"{name} is missing {key}")
    if problems:
        return problems
    if data["synthetic"] is not True or data["real_quotes"] is not False or data["real_news"] is not False:
        problems.append(f"{name} markers must be synthetic true and real quotes/news false")
    if data["expects_data"] not in ALLOWED_DATA:
        problems.append(f"{name} data label is not allowed: {data['expects_data']!r}")
    if data["expects_structure"] not in ALLOWED_STRUCTURE:
        problems.append(f"{name} structure label is not allowed: {data['expects_structure']!r}")
    if data["expects_execution"] not in ALLOWED_EXECUTION:
        problems.append(f"{name} execution label is not allowed: {data['expects_execution']!r}")
    pairs = (
        ("数据结论：", "expects_data"),
        ("结构结论：", "expects_structure"),
        ("执行结论：", "expects_execution"),
        ("总结论：", "expects_overall"),
    )
    for label, key in pairs:
        got = last_labeled(body, label)
        if got != data[key]:
            problems.append(f"{name} {label} is {got!r}, header says {data[key]!r}")
    incomplete = (
        data["expects_data"] == "检查不完整"
        or data["expects_execution"] in {"检查不完整", "计划按现行规则不可执行"}
        or data["expects_overall"] in {"检查不完整", "计划按现行规则不可执行"}
    )
    if incomplete and data["expects_overall"] in PASS_OVERALL:
        problems.append(f"{name} is incomplete or unexecutable but its overall label is a pass")
    if incomplete and "总结论：结构尚可，可继续观察" in body:
        problems.append(f"{name} incomplete text still has a structure-ok overall line")
    if incomplete and "总结论：按现行规则可以执行所写计划" in body:
        problems.append(f"{name} incomplete text still has an executable overall line")
    if data["expects_overall"] == "结构尚可，可继续观察" and "不是风险已经排除" not in body:
        problems.append(f"{name} structure-ok overall does not say risk has not been ruled out")
    return problems


def check_required_phrases(root: Path) -> list[str]:
    problems = []
    required = {
        "docs/trade-record.md": SHARED_FIELDS + EVIDENCE_FIELDS + tuple(ALLOWED_DATA | ALLOWED_STRUCTURE | ALLOWED_EXECUTION),
        "docs/evidence-contract.md": EVIDENCE_FIELDS,
        "docs/templates/trade-plan.md": PLAN_FIELDS,
        "skills/liquidity-repair/output-template.md": SHARED_FIELDS
        + ("数据：", "结构：", "执行：", "总结论", "来源 URL", "摘录", "入场或观察", "持有或退出", "复盘"),
        "skills/pre-open-overnight-risk-check/output-template.md": (
            "外部或隔夜事件观察",
            "三个问题",
            "数据：",
            "结构：",
            "执行：",
            "来源 URL",
            "检索时间",
            "必须在开盘卖出",
        ),
    }
    for rel, phrases in required.items():
        path = root / rel
        if not path.exists():
            problems.append(f"missing required page {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                problems.append(f"{rel} does not state required field or label {phrase}")
    return problems


def zhongji_cash_difference() -> Decimal:
    return (Decimal("547.5") - Decimal("511.9532")) * Decimal(100)


def zhongji_ratio_percent() -> Decimal:
    difference = zhongji_cash_difference()
    base = Decimal("511.9532") * Decimal(100)
    return (difference / base * Decimal(100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def synthetic_vwap_yuan() -> Decimal:
    amount = Decimal(200_000_000)
    shares = Decimal(40) * Decimal(10_000) * Decimal(100)
    return amount / shares


def check_decimals(root: Path) -> list[str]:
    problems = []
    difference = zhongji_cash_difference()
    if difference != Decimal("3554.68"):
        problems.append(f"Zhongji cash difference is {difference}, not 3554.68")
    ratio = zhongji_ratio_percent()
    if ratio != Decimal("6.94"):
        problems.append(f"Zhongji stated-cost ratio is {ratio}, not 6.94")
    vwap = synthetic_vwap_yuan()
    if vwap != Decimal("5"):
        problems.append(f"synthetic VWAP is {vwap}, not 5")
    case = root / "docs" / "cases" / "300308-2026-11.md"
    if case.exists():
        text = case.read_text(encoding="utf-8")
        if "3554.68" not in text or "511.9532" not in text or "547.5" not in text:
            problems.append("Zhongji case no longer states the checked cost figures")
        if "占总资金" not in text:
            problems.append("Zhongji case no longer says the ratio is not a share of total capital")
    else:
        problems.append("Zhongji case file is missing")
    indicators = root / "skills" / "liquidity-repair" / "indicators.md"
    if indicators.exists():
        text = indicators.read_text(encoding="utf-8")
        if "40,000,000" not in text or "5.00" not in text:
            problems.append("indicator dictionary no longer states the checked VWAP example")
    else:
        problems.append("indicator dictionary is missing")
    return problems


def check_privacy(root: Path) -> list[str]:
    problems = []
    for path in iter_files(root):
        if path.suffix.lower() not in {".md", ".txt", ".yaml", ".yml"} and path.name != "llms.txt":
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if any(word in line for word in ("不要", "不得", "不写", "不包括", "不包含", "不收集", "不记", "不是")):
                continue
            for pattern in PRIVACY_RES:
                if pattern.search(line):
                    problems.append(
                        f"privacy: {path.relative_to(root)}:{lineno} matches {pattern.pattern}"
                    )
    return problems


def check_bilingual(root: Path) -> list[str]:
    problems = []
    zh = root / "README.md"
    en = root / "README.en.md"
    if not zh.exists() or not en.exists():
        return ["README.md and README.en.md are both required"]
    zh_text = zh.read_text(encoding="utf-8")
    en_text = en.read_text(encoding="utf-8")
    zh_anchors = re.findall(r'<a id="([^"]+)"></a>', zh_text)
    en_anchors = re.findall(r'<a id="([^"]+)"></a>', en_text)
    if zh_anchors != en_anchors or zh_anchors != README_ANCHORS:
        problems.append(f"README anchors differ: {zh_anchors} vs {en_anchors}")
    zh_need = (
        "MIT",
        "Frank Cheng",
        "完整克隆",
        "检查不完整",
        "不会因为仓库里有这些文件就自动安装",
        "python3 scripts/check_docs.py",
        "通过这次检查并不表示交易方法有效",
        "2026-11-14.3",
    )
    en_need = (
        "MIT",
        "Frank Cheng",
        "complete clone",
        "check incomplete",
        "do not auto-install",
        "python3 scripts/check_docs.py",
        "Passing this check does not validate trading performance",
        "2026-11-14.3",
    )
    for phrase in zh_need:
        if phrase not in zh_text:
            problems.append(f"README.md is missing {phrase}")
    for phrase in en_need:
        if phrase not in en_text:
            problems.append(f"README.en.md is missing {phrase}")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8") if (root / "AGENTS.md").exists() else ""
    llms = (root / "llms.txt").read_text(encoding="utf-8") if (root / "llms.txt").exists() else ""
    for label, text in (("AGENTS.md", agents), ("llms.txt", llms)):
        for phrase in (
            "python3 scripts/check_docs.py",
            "does not validate trading performance",
            "检查不完整",
            "check incomplete",
            "MIT",
            "2026-11-14.3",
        ):
            if phrase not in text:
                problems.append(f"{label} is missing {phrase}")
    changelog = root / "CHANGELOG.md"
    if changelog.exists() and "## 2026-11-14.3" not in changelog.read_text(encoding="utf-8"):
        problems.append("CHANGELOG.md has no 2026-11-14.3 section")
    strategy = root / "docs" / "strategy.md"
    if strategy.exists() and "版本：2026-11-14.3" not in strategy.read_text(encoding="utf-8"):
        problems.append("docs/strategy.md version is not 2026-11-14.3")
    return problems


def check_tree(root: Path) -> list[str]:
    problems: list[str] = []
    problems.extend(check_links(root))
    problems.extend(check_yaml_and_skills(root))
    problems.extend(check_fixtures(root))
    problems.extend(check_required_phrases(root))
    problems.extend(check_decimals(root))
    problems.extend(check_privacy(root))
    problems.extend(check_bilingual(root))
    return problems


def _expect_problem(label: str, problems: list[str]) -> str | None:
    if problems:
        return None
    return f"self-test did not fail: {label}"


def self_test() -> list[str]:
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docs").mkdir()
        (root / "README.md").write_text("[missing](docs/no-such.md)\n", encoding="utf-8")
        found = check_links(root)
        if not any("broken link" in item for item in found):
            problems.append("self-test did not fail on a broken relative link")

    bad_fixture = fixture_problems(
        "bad-fixture",
        {
            "synthetic": True,
            "real_quotes": False,
            "real_news": False,
            "frozen_as_of": "合成日 D 15:20 Asia/Shanghai",
            "rule_version": "2026-11-14.2",
            "expects_data": "检查不完整",
            "expects_structure": "本次未评估结构",
            "expects_execution": "检查不完整",
            "expects_overall": "结构尚可，可继续观察",
        },
        "- 数据结论：检查不完整\n- 结构结论：本次未评估结构\n- 执行结论：检查不完整\n- 总结论：结构尚可，可继续观察\n",
    )
    if not any("pass" in item for item in bad_fixture):
        problems.append("self-test did not fail when an incomplete fixture claims a pass")

    missing = fixture_problems("missing-field", {"synthetic": True}, "")
    if not any("missing expects_overall" in item for item in missing):
        problems.append("self-test did not fail when a required fixture field is missing")

    wrong_vwap = Decimal(200_000_000) / (Decimal(40) * Decimal(10_000))
    if not (wrong_vwap != Decimal("5") and wrong_vwap != synthetic_vwap_yuan()):
        problems.append("self-test did not fail a wrong unit calculation")
    if zhongji_cash_difference() == Decimal("3554.67"):
        problems.append("self-test arithmetic accidentally matched the wrong cash difference")

    privacy_hit = []
    for pattern in PRIVACY_RES:
        if pattern.search("总资金：1000000"):
            privacy_hit.append(pattern.pattern)
    if not privacy_hit:
        problems.append("self-test privacy pattern missed a total-capital figure")
    if any(pattern.search("自述卖出 100 股，547.50 元，价差 3554.68") for pattern in PRIVACY_RES):
        problems.append("self-test privacy pattern rejected authorized Zhongji figures")
    if any(pattern.search("不要写入总资金或其他持仓") for pattern in PRIVACY_RES):
        problems.append("self-test privacy pattern matched a prohibition without a figure")
    return problems


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    problems = check_tree(root)
    problems.extend(self_test())
    if problems:
        for item in problems:
            print(item)
        print(f"{len(problems)} problem(s). A passing check would not validate trading performance.")
        return 1
    print("documentation check passed")
    print("command: python3 scripts/check_docs.py")
    print("negative cases failed as expected: broken link, missing field, wrong unit, incomplete fixture claiming a pass")
    print("Passing this check does not validate trading performance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
