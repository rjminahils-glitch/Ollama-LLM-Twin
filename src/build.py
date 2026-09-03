"""Turn the NUML workbook into clean JSONL datasets."""

from collections import Counter
from pathlib import Path

from src.loaders import (
    WORKBOOK,
    KNOWLEDGE_REQUIRED, KNOWLEDGE_OPTIONAL,
    INSTRUCTION_REQUIRED, INSTRUCTION_OPTIONAL,
    read_tab, to_knowledge, to_instructions, save_jsonl,
)
from src.validate import (
    smoke_tests, validate_knowledge, validate_instructions, coverage,
)

# Adapted from the chapter's absolute macOS path ("Data/cleann/", note the
# typo) to this project's existing data/clean/ folder from Chapter 2.
OUT_DIR = Path("data/clean/")
LINE = "=" * 62


def report_skipped(skipped, label):
    if not skipped:
        print(f"  {label}: nothing skipped")
        return
    reasons = Counter(s[0] for s in skipped)
    print(f"  {label}: {len(skipped)} skipped -> {dict(reasons)}")
    for status, row, rid, raw in skipped[:5]:
        print(f"    row {row} ({rid}): wrote '{raw}' -> treated as {status}")
    if len(skipped) > 5:
        print(f"    ... and {len(skipped) - 5} more")


def report_problems(errors, warnings):
    print(f"  {len(errors)} errors, {len(warnings)} warnings")
    for e in errors:
        print(f"    ERROR    {e}")
    for w in warnings[:10]:
        print(f"    warning  {w}")
    if len(warnings) > 10:
        print(f"    ... and {len(warnings) - 10} more warnings")


def main():
    print(LINE)
    print("EXTRACT")
    k_rows = read_tab(WORKBOOK, "knowledge", KNOWLEDGE_REQUIRED, KNOWLEDGE_OPTIONAL)
    i_rows = read_tab(WORKBOOK, "instructions", INSTRUCTION_REQUIRED, INSTRUCTION_OPTIONAL)
    print(f"  knowledge tab: {len(k_rows)} non-empty rows")
    print(f"  instructions tab: {len(i_rows)} non-empty rows")

    print(LINE)
    print("TRANSFORM")
    knowledge, k_skipped = to_knowledge(k_rows)
    instructions, i_skipped = to_instructions(i_rows)
    print(f"  knowledge: {len(knowledge)} kept")
    report_skipped(k_skipped, "knowledge")
    print(f"  instructions: {len(instructions)} kept")
    report_skipped(i_skipped, "instructions")

    print(LINE)
    print("VALIDATE")
    fatal = smoke_tests(knowledge, instructions)
    for f in fatal:
        print(f"  FATAL: {f}")
    if fatal:
        print("  nothing written. fix the workbook and run again.")
        return

    knowledge_ids = {d["id"] for d in knowledge}
    k_err, k_warn = validate_knowledge(knowledge)
    i_err, i_warn = validate_instructions(instructions, knowledge_ids)
    errors, warnings = k_err + i_err, k_warn + i_warn
    report_problems(errors, warnings)

    print(LINE)
    print("LOAD")
    save_jsonl(knowledge, OUT_DIR / "knowledge.jsonl")
    save_jsonl(instructions, OUT_DIR / "instructions.jsonl")
    print(f"  {OUT_DIR / 'knowledge.jsonl'}: {len(knowledge)}")
    print(f"  {OUT_DIR / 'instructions.jsonl'}: {len(instructions)}")

    coverage(knowledge, instructions)

    print(LINE)
    if errors:
        print(f"DONE with {len(errors)} errors. Fix these before Chapter 11.")
    else:
        print("DONE. No errors.")


if __name__ == "__main__":
    main()