"""Quality checks. Errors must be fixed. Warnings should be fixed."""

from collections import Counter

CATEGORIES = {"admissions", "fees", "programs", "hostel",
              "transport", "scholarships", "faculty", "campus"}

MIN_KNOWLEDGE_WORDS = 40
MAX_KNOWLEDGE_WORDS = 350
MIN_ANSWER_WORDS = 40
MAX_ANSWER_WORDS = 200

FALLBACKS = {"not recorded", "unknown", "untitled"}


def smoke_tests(knowledge, instructions, min_knowledge=10, min_instructions=10):
    """Whole-dataset checks. These catch what per-row checks cannot."""
    fatal = []
    if len(knowledge) < min_knowledge:
        fatal.append(f"only {len(knowledge)} knowledge entries, expected at least {min_knowledge}")
    if len(instructions) < min_instructions:
        fatal.append(f"only {len(instructions)} instruction pairs, expected at least {min_instructions}")
    if knowledge:
        unique = len({d["text"] for d in knowledge})
        if unique < len(knowledge) * 0.9:
            fatal.append(f"only {unique} unique texts across {len(knowledge)} entries")
    return fatal


def validate_knowledge(docs):
    errors, warnings = [], []
    seen = set()

    for d in docs:
        tag = d.get("id") or f"NO ID (title: {d.get('title', '')[:30]})"

        # completeness - only fields with no fallback
        for field in ["id", "category", "text"]:
            if not d.get(field):
                errors.append(f"{tag}: '{field}' is empty")

        # uniqueness
        rid = d.get("id")
        if rid:
            if rid in seen:
                errors.append(f"{tag}: duplicate id")
            seen.add(rid)

        # validity
        if d.get("category") not in CATEGORIES:
            errors.append(f"{tag}: unknown category '{d.get('category')}'")

        words = len(d.get("text", "").split())
        if words < MIN_KNOWLEDGE_WORDS:
            errors.append(f"{tag}: text too short ({words} words)")
        elif words > MAX_KNOWLEDGE_WORDS:
            warnings.append(f"{tag}: text long ({words} words), consider splitting")

        if "?" in d.get("text", ""):
            warnings.append(f"{tag}: text contains a question mark")

        # fallback values mean the student left it blank
        for field in ["source", "written_by", "title"]:
            if str(d.get(field, "")).lower() in FALLBACKS:
                warnings.append(f"{tag}: '{field}' was not filled in")

    return errors, warnings


def validate_instructions(pairs, knowledge_ids):
    errors, warnings = [], []
    seen = set()

    for p in pairs:
        tag = p.get("id") or "NO ID"

        for field in ["id", "category", "instruction", "output"]:
            if not p.get(field):
                errors.append(f"{tag}: '{field}' is empty")

        pid = p.get("id")
        if pid:
            if pid in seen:
                errors.append(f"{tag}: duplicate id")
            seen.add(pid)

        if p.get("category") not in CATEGORIES:
            errors.append(f"{tag}: unknown category '{p.get('category')}'")

        words = len(p.get("output", "").split())
        if words < MIN_ANSWER_WORDS:
            errors.append(f"{tag}: answer too short ({words} words)")
        elif words > MAX_ANSWER_WORDS:
            warnings.append(f"{tag}: answer long ({words} words)")

        # referential integrity
        sids = p.get("source_ids", [])
        if not sids:
            warnings.append(f"{tag}: no source_ids, cannot trace this answer to a fact")
        for sid in sids:
            if sid not in knowledge_ids:
                errors.append(f"{tag}: source_id '{sid}' does not exist in knowledge")

    return errors, warnings


def coverage(docs, pairs):
    kc = Counter(d.get("category") for d in docs)
    ic = Counter(p.get("category") for p in pairs)
    print("\nCoverage by category")
    print(f"{'category':<16}{'knowledge':>10}{'instructions':>14}{'ratio':>8}")
    for cat in sorted(CATEGORIES):
        k, i = kc.get(cat, 0), ic.get(cat, 0)
        ratio = f"{i / k:.1f}" if k else "-"
        flag = "  <- thin" if k and i / k < 1.5 else ""
        print(f"{cat:<16}{k:>10}{i:>14}{ratio:>8}{flag}")
    print(f"{'TOTAL':<16}{len(docs):>10}{len(pairs):>14}")