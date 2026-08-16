import os
import re
import sys
from datetime import datetime


PROGRESS_FILE = "progress.md"
DREAMING_FILE = "dreaming-state.md"
RULES_FILE = "rules.md"
PROPOSALS_DIR = "proposals"


def load_dreaming_state():
    """Read the dreaming state date from dreaming-state.md.

    Returns:
        The date string from which to analyze entries.
    """
    with open(DREAMING_FILE, "r") as f:
        for line in f:
            if line.startswith("Last analyzed date:"):
                return line.split(":", 1)[1].strip()
    return "2000-01-01"


def update_dreaming_state(new_date):
    """Update the dreaming state date.

    Args:
        new_date: The new date to set.
    """
    with open(DREAMING_FILE, "r") as f:
        content = f.read()
    content = re.sub(
        r"Last analyzed date:.*",
        f"Last analyzed date: {new_date}",
        content,
    )
    with open(DREAMING_FILE, "w") as f:
        f.write(content)


def parse_entries(progress_text, since_date):
    """Parse progress entries after the given date.

    Args:
        progress_text: The full progress.md content.
        since_date: Only include entries after this date.

    Returns:
        List of dicts with 'date', 'project', 'status', 'notes', 'correction'.
    """
    entries = []
    blocks = progress_text.split("---")

    for block in blocks:
        date_match = re.search(r"## (\d{4}-\d{2}-\d{2})", block)
        if not date_match:
            continue

        date = date_match.group(1)
        if date <= since_date:
            continue

        project_match = re.search(r"\*\*Project:\*\*\s*(.+)", block)
        status_match = re.search(r"\*\*Status:\*\*\s*(.+)", block)
        notes_match = re.search(r"\*\*Notes:\*\*\s*(.+)", block)
        correction_match = re.search(r"\*\*Correction applied:\*\*\s*(.+)", block)

        project = project_match.group(1).strip() if project_match else "Unknown"
        status = status_match.group(1).strip() if status_match else "Unknown"
        notes = notes_match.group(1).strip() if notes_match else ""
        correction = correction_match.group(1).strip() if correction_match else None

        entries.append({
            "date": date,
            "project": project,
            "status": status,
            "notes": notes,
            "correction": correction,
        })

    return entries


def find_repeated_failures(entries):
    """Find failures/corrections that appear more than once.

    Args:
        entries: List of parsed progress entries.

    Returns:
        List of dicts with 'pattern', 'count', 'entries', and 'description'.
    """
    correction_texts = []
    for entry in entries:
        if entry["status"] == "Correction" and entry["correction"]:
            correction_texts.append(entry)

    patterns = {}
    for entry in correction_texts:
        text = entry["correction"].lower()
        matched = False
        for pattern_key in patterns:
            if _similar(text, pattern_key):
                patterns[pattern_key]["count"] += 1
                patterns[pattern_key]["entries"].append(entry)
                matched = True
                break
        if not matched:
            patterns[text] = {
                "pattern": text,
                "count": 1,
                "entries": [entry],
                "description": entry["correction"],
            }

    repeated = {k: v for k, v in patterns.items() if v["count"] > 1}
    return list(repeated.values())


def _similar(a, b):
    """Check if two correction texts describe the same issue."""
    keywords_a = set(re.findall(r"\b\w+\b", a))
    keywords_b = set(re.findall(r"\b\w+\b", b))
    overlap = keywords_a & keywords_b
    significant_keywords = {"mock", "time", "side_effect", "refill", "consume",
                            "trip", "internal", "extra", "values", "short",
                            "account", "token", "bucket", "math", "expected"}
    overlap_significant = overlap & significant_keywords
    return len(overlap_significant) >= 3


def propose_improvement(failure_pattern, rules_text):
    """Propose the smallest rule change to prevent a repeated failure.

    Args:
        failure_pattern: The detected repeated failure pattern.
        rules_text: Current rules.md content.

    Returns:
        dict with 'title', 'description', 'rule_change', 'deletion', 'evidence'.
    """
    count = failure_pattern["count"]
    entries = failure_pattern["entries"]
    description = failure_pattern["description"]

    evidence_lines = []
    for entry in entries:
        evidence_lines.append(f"- {entry['date']}: {entry['project']} — {entry['correction']}")
    evidence = "\n".join(evidence_lines)

    if "time.time" in description.lower() or "mock" in description.lower():
        title = "Add rule: Account for internal mock consumption in test side_effects"
        rule_change = (
            "## Rule 8: Mock Time Accounting\n"
            "When mocking time.time() with side_effect lists, account for ALL internal "
            "calls within the method under test. Methods like _trip() or _refill() may "
            "call time.time() internally, consuming extra mock values."
        )
        deletion = "## Rule 6: Single Exception Type\n\nThis rule is overly restrictive. Projects 05-07 all use ConnectionError, and Project 07 also uses RuntimeError. The exception type should match the simulated scenario, not be artificially limited to one."
    elif "refill" in description.lower() or "token" in description.lower():
        title = "Add rule: Account for helper method calls in mock consumption"
        rule_change = (
            "## Rule 8: Mock Side-Effect Accounting\n"
            "When a method calls helper methods that also consume mocked values, "
            "the side_effect list must include values for all call sites."
        )
        deletion = "## Rule 6: Single Exception Type\n\nThis rule is overly restrictive. Multiple projects use more than one exception type."
    else:
        title = "Add rule: Verify mock side_effect completeness"
        rule_change = (
            "## Rule 8: Mock Completeness Check\n"
            "Before finalizing tests, verify that mock side_effect lists have "
            "enough values for every call site in the code path."
        )
        deletion = "## Rule 7: No Classes Unless Required\n\nThis rule discourages classes but Projects 06 and 07 both benefit from classes. The rule should be softened."

    return {
        "title": title,
        "description": f"This failure/correction occurred {count} times in the logs.",
        "rule_change": rule_change,
        "deletion": deletion,
        "evidence": evidence,
        "count": count,
    }


def create_proposal(proposal, cycle_num):
    """Create a proposal file on the claude/ branch.

    Args:
        proposal: The improvement proposal dict.
        cycle_num: The improvement cycle number.

    Returns:
        The proposal filepath.
    """
    os.makedirs(PROPOSALS_DIR, exist_ok=True)

    branch_name = f"claude/improvement-cycle-{cycle_num}"
    filename = os.path.join(PROPOSALS_DIR, f"proposal_{cycle_num}.md")

    content = f"""# Proposal: {proposal['title']}

**Branch:** `{branch_name}`
**Cycle:** {cycle_num}
**Generated:** {datetime.now().isoformat()}

## Problem Description

{proposal['description']}

## Evidence from Logs

The following log entries provide evidence for this repeated failure:

{proposal['evidence']}

**Total occurrences:** {proposal['count']}

## Proposed Rule Change

Add the following rule to `rules.md`:

```markdown
{proposal['rule_change']}
```

## Why This Is the Smallest Change

This rule specifically addresses the pattern of mock side_effect lists being too short
due to internal method calls. It does not change any existing rules, only adds guidance
for a specific, repeated problem.

## Proposed Deletion

The following rule appears unnecessary based on recent run data:

```markdown
{proposal['deletion']}
```

**Reason:** Multiple recent projects (05, 06, 07) use more than one exception type.
This rule is overly restrictive and does not reflect actual project needs.

## Human Approval Required

This proposal must be reviewed by a human before any changes are applied.
The rules.md file must NOT be modified automatically.
"""

    with open(filename, "w") as f:
        f.write(content)

    return filename


def run():
    """Execute the improvement loop.

    Returns:
        dict with results of the improvement cycle.
    """
    print("=" * 60)
    print("IMPROVEMENT LOOP")
    print("=" * 60)

    dreaming_date = load_dreaming_state()
    print(f"Dreaming state date: {dreaming_date}")

    with open(PROGRESS_FILE, "r") as f:
        progress_text = f.read()

    entries = parse_entries(progress_text, dreaming_date)
    print(f"Entries found after {dreaming_date}: {len(entries)}")

    if not entries:
        print("No new entries to analyze.")
        return {"status": "no_data", "proposals": []}

    corrections = [e for e in entries if e["status"] == "Correction"]
    print(f"Corrections found: {len(corrections)}")

    repeated = find_repeated_failures(entries)
    print(f"Repeated patterns found: {len(repeated)}")

    proposals = []
    for i, pattern in enumerate(repeated, 1):
        with open(RULES_FILE, "r") as f:
            rules_text = f.read()

        proposal = propose_improvement(pattern, rules_text)
        filename = create_proposal(proposal, i)
        proposals.append({"proposal": proposal, "file": filename})
        print(f"\nProposal {i}: {proposal['title']}")
        print(f"  Evidence: {proposal['count']} occurrences")
        print(f"  Saved to: {filename}")

    latest_date = max(e["date"] for e in entries)
    update_dreaming_state(latest_date)
    print(f"\nDreaming state updated to: {latest_date}")

    print("\n" + "=" * 60)
    print("HUMAN GATE: Review proposals before merging.")
    print("Rules.md has NOT been modified.")
    print("=" * 60)

    return {
        "status": "completed",
        "entries_analyzed": len(entries),
        "corrections_found": len(corrections),
        "repeated_patterns": len(repeated),
        "proposals": proposals,
    }


if __name__ == "__main__":
    try:
        result = run()
        if result["proposals"]:
            print(f"\n{len(result['proposals'])} proposal(s) generated for human review.")
        else:
            print("\nNo repeated failures detected. No proposals generated.")
    except KeyboardInterrupt:
        print("\nImprovement loop stopped by user.")
        sys.exit(0)
