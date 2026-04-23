#!/usr/bin/env python3

# Licensed under the Apache 2.0 License.
"""
Vale Render - Validate Vale JSON artifact and render a trusted markdown report.

Security boundary: this script runs in a privileged workflow (pull-requests: write)
and processes an artifact produced by an untrusted fork PR. All inputs are validated
and sanitized before being written to the PR comment.
"""

import argparse
import hashlib
import json
import os
import re
import sys

# --- constants ---------------------------------------------------------------

MAX_FILE_SIZE = 100 * 1024  # 100 KB
MAX_PATH_LEN  = 256
MAX_MSG_LEN   = 512
MAX_RULE_LEN  = 128
MAX_ISSUES    = 1000
ALLOWED_SEVERITIES = frozenset({"error", "warning", "suggestion"})
RULE_PATTERN = re.compile(r'^[A-Za-z0-9_.]+$')

REPORT_FOOTER_BASE = """
---

Vale checks documentation changes against the [Gardener style guide](https://gardener.cloud/docs/contribute/documentation/style-guide/) and the [Elastic style guide](https://github.com/elastic/vale-rules/tree/main). Please try to fix all errors and warnings.
"""

def report_footer(branch: str, groups: dict | None = None) -> str:
    if not branch:
        return REPORT_FOOTER_BASE
    if not groups or not any(groups.values()):
        return REPORT_FOOTER_BASE

    lines = ["Verify each finding against the current code and only fix it if needed.\n"]
    for sev, label in [("error", "Errors"), ("warning", "Warnings"), ("suggestion", "Suggestions")]:
        items = groups.get(sev, [])
        if not items:
            continue
        lines.append(f"{label}:")
        for item in items:
            # items are table rows: | `path` | line | rule | message |
            parts = [p.strip() for p in item.strip('|').split('|')]
            if len(parts) >= 4:
                path, line, rule, message = parts[0], parts[1], parts[2], parts[3]
                # line may be a markdown link like [28](url) — extract just the number
                line = re.sub(r'\[(\d+)\]\([^)]*\)', r'\1', line).strip()
                lines.append(f"- In {path}, line {line} ({rule}): {message}")
        lines.append("")

    prompt_body = "\n".join(lines).strip()

    return REPORT_FOOTER_BASE + f"""
<details>
<summary>AI Prompt</summary>

```
{prompt_body}
```

</details>
"""

# --- sanitization ------------------------------------------------------------

def sanitize(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)                    # strip HTML tags
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)  # [text](url) → text
    text = re.sub(r'https?://\S+', '', text)               # bare URLs
    text = re.sub(r'[<>\[\]()!]', '', text)                # injection chars
    text = text.replace('|', '\\|')                        # escape table pipes
    return text.strip()

def sanitize_path(path: str) -> str:
    path = re.sub(r'<[^>]+>', '', path)
    path = re.sub(r'[<>\[\]()!]', '', path)
    path = path.replace('|', '\\|')
    return path.strip()

# --- validation --------------------------------------------------------------

def validate(data: object) -> list:
    errors = []
    if not isinstance(data, dict):
        return ["root must be an object"]

    for path, alerts in data.items():
        if not isinstance(path, str) or len(path) > MAX_PATH_LEN:
            errors.append(f"path must be a string <= {MAX_PATH_LEN} chars: {path!r}")
        if '\x00' in path or '..' in path.split('/'):
            errors.append(f"unsafe path: {path!r}")
        if not isinstance(alerts, list):
            errors.append(f"alerts for {path!r} must be a list")
            continue
        for i, alert in enumerate(alerts):
            prefix = f"{path}[{i}]"
            if not isinstance(alert, dict):
                errors.append(f"{prefix} must be an object"); continue
            for field in ("Line", "Message", "Check", "Severity"):
                if field not in alert:
                    errors.append(f"{prefix} missing field {field!r}")
            if "Severity" in alert and alert["Severity"] not in ALLOWED_SEVERITIES:
                errors.append(f"{prefix}.Severity invalid: {alert['Severity']!r}")
            if "Check" in alert:
                if not isinstance(alert["Check"], str) or len(alert["Check"]) > MAX_RULE_LEN:
                    errors.append(f"{prefix}.Check must be string <= {MAX_RULE_LEN} chars")
                elif not RULE_PATTERN.match(alert["Check"]):
                    errors.append(f"{prefix}.Check contains invalid chars: {alert['Check']!r}")
            if "Message" in alert and (not isinstance(alert["Message"], str) or len(alert["Message"]) > MAX_MSG_LEN):
                errors.append(f"{prefix}.Message must be string <= {MAX_MSG_LEN} chars")
    return errors

# --- line range filtering ----------------------------------------------------

def load_ranges(path: str) -> dict:
    """Load line_ranges.txt → {filepath: [(start, end), ...]}"""
    ranges: dict = {}
    if not path or not os.path.exists(path):
        return ranges
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            filepath, start, count = parts
            try:
                start = int(start)
                count = int(count) if count else 1
            except ValueError:
                continue
            ranges.setdefault(filepath, []).append((start, start + count - 1))
    return ranges

def in_range(line: int, ranges: list) -> bool:
    return any(start <= line <= end for start, end in ranges)

# --- diff link ---------------------------------------------------------------

def diff_link(path: str, line: int, repo: str, pr: str) -> str:
    if repo and pr:
        h = hashlib.sha256(path.lstrip('./').encode()).hexdigest()
        url = f"https://github.com/{repo}/pull/{pr}/files#diff-{h}R{line}"
        return f"[{line}]({url})"
    return str(line)

# --- rendering ---------------------------------------------------------------

def render(data: dict, ranges: dict, repo: str, pr: str, branch: str) -> str:
    groups: dict = {"error": [], "warning": [], "suggestion": []}
    total_issues = sum(len(v) for v in data.values())
    if total_issues > MAX_ISSUES:
        return "## ⚠️ Vale Linting Check\n\nToo many issues to display.\n"

    for path, alerts in data.items():
        file_ranges = ranges.get(path, [])
        for alert in alerts:
            # If we have range data, filter to modified lines only
            if file_ranges and not in_range(alert["Line"], file_ranges):
                continue
            sev = alert["Severity"]
            line_link = diff_link(path, alert["Line"], repo, pr)
            entry = f"| `{sanitize_path(path)}` | {line_link} | {alert['Check']} | {sanitize(alert['Message'])} |"
            groups[sev].append(entry)

    errors      = groups["error"]
    warnings    = groups["warning"]
    suggestions = groups["suggestion"]
    total       = len(errors) + len(warnings) + len(suggestions)

    if total == 0:
        return "## ✅ Vale Linting Check\n\n**No issues found on modified lines.**\n" + report_footer(branch)

    parts = []
    if errors:      parts.append(f"{len(errors)} error{'s' if len(errors) != 1 else ''}")
    if warnings:    parts.append(f"{len(warnings)} warning{'s' if len(warnings) != 1 else ''}")
    if suggestions: parts.append(f"{len(suggestions)} suggestion{'s' if len(suggestions) != 1 else ''}")

    report = f"## Vale Linting Check\n\n**Summary:** {', '.join(parts)} found\n\n"
    header = "| File | Line | Rule | Message |\n|---|---|---|---|\n"

    for sev, items, label in [
        ("error",      errors,      f"❌ Errors ({len(errors)})"),
        ("warning",    warnings,    f"⚠️ Warnings ({len(warnings)})"),
        ("suggestion", suggestions, f"💡 Suggestions ({len(suggestions)})"),
    ]:
        if not items:
            continue
        report += f"<details>\n<summary>{label}</summary>\n\n"
        report += header
        report += "\n".join(items) + "\n"
        report += "\n</details>\n\n"

    report += report_footer(branch, groups)
    return report

# --- main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  required=True)
    parser.add_argument("--ranges", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo",   default="")
    parser.add_argument("--pr",     default="")
    parser.add_argument("--branch", default="")
    args = parser.parse_args()

    for path in (args.input, args.output):
        if os.path.islink(path):
            print(f"::error::Refusing to follow symlink: {path}", file=sys.stderr)
            return 1

    try:
        size = os.path.getsize(args.input)
    except OSError as e:
        print(f"::error::Cannot read input: {e}", file=sys.stderr)
        return 1

    if size > MAX_FILE_SIZE:
        print(f"::error::Input too large ({size} bytes)", file=sys.stderr)
        return 1

    try:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"::error::Failed to parse JSON: {e}", file=sys.stderr)
        return 1

    errs = validate(data)
    if errs:
        for e in errs:
            print(f"::error::Validation failed: {e}", file=sys.stderr)
        return 1

    ranges = load_ranges(args.ranges)
    report = render(data, ranges, args.repo, args.pr, args.branch)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
    except OSError as e:
        print(f"::error::Failed to write output: {e}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
