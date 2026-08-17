# Proposal: Add rule: Account for internal mock consumption in test side_effects

**Branch:** `claude/improvement-cycle-1`
**Cycle:** 1
**Generated:** 2026-08-17T00:34:57.832205

## Problem Description

This failure/correction occurred 2 times in the logs.

## Evidence from Logs

The following log entries provide evidence for this repeated failure:

- 2026-08-17: 12 (Improvement Loop Capstone) — Added extra mock time values to account for _trip() internal calls.
- 2026-08-17: 12 (Improvement Loop Capstone) — Added extra mock time values to side_effect lists to account for _refill() internal calls.

**Total occurrences:** 2

## Proposed Rule Change

Add the following rule to `rules.md`:

```markdown
## Rule 8: Mock Time Accounting
When mocking time.time() with side_effect lists, account for ALL internal calls within the method under test. Methods like _trip() or _refill() may call time.time() internally, consuming extra mock values.
```

## Why This Is the Smallest Change

This rule specifically addresses the pattern of mock side_effect lists being too short
due to internal method calls. It does not change any existing rules, only adds guidance
for a specific, repeated problem.

## Proposed Deletion

The following rule appears unnecessary based on recent run data:

```markdown
## Rule 6: Single Exception Type

This rule is overly restrictive. Projects 05-07 all use ConnectionError, and Project 07 also uses RuntimeError. The exception type should match the simulated scenario, not be artificially limited to one.
```

**Reason:** Multiple recent projects (05, 06, 07) use more than one exception type.
This rule is overly restrictive and does not reflect actual project needs.

## Human Approval Required

This proposal must be reviewed by a human before any changes are applied.
The rules.md file must NOT be modified automatically.
